from fontTools.feaLib.parser import Parser
from fontTools.feaLib.ast import *
from warnings import warn
from copy import deepcopy
from pathlib import PurePath
from ufo2ft.featureCompiler import FeatureCompiler
from collections import OrderedDict
from fontGadgets.tools import fontMethod, fontCachedMethod
import os
from io import StringIO

"""
- add sctipt and language tags to the rules and glyphs
"""

class GlyphFeautres():

    def __init__(self, glyph):
        self._glyph = glyph
        self.sourceGlyphs = {}  # g.name: AlternateSubstStatement...
        self.targetGlyphs = {}  # g.name: AlternateSubstStatement...

    @property
    def featureTags(self):
        """
        returns a set of tags
        """
        tags = set()
        for gs, sublist in self._glyph.features.sourceGlyphs.items():
            for sub in sublist:
                tags.update(sub.features)
        return tags

    def _getLookups(self):
        # fetch lookups objects from the statements
        pass

    def _getLanguages(self):
        pass

    def _getScripts(slef):
        pass

    @property
    def glyph(self):
        return self._glyph

@fontMethod
def features(glyph):
    return glyph.font.features.parser[glyph.name]

class ParsedFeatureFile():

    gsubGlyphsAttrs = {
        # one to one, alternate shapes of a glyph
        AlternateSubstStatement: ('glyph', 'replacement'),
        # one to many, decomposing one glyph to many glyphs
        MultipleSubstStatement: ('glyph', 'replacement'),
        # many to one, ligatures
        LigatureSubstStatement: ('glyphs', 'replacement'),
        # one to one, alternate shapes of a glyph
        SingleSubstStatement: ('glyphs', 'replacements'),
        # one to one, alternate shapes of a glyph
        ReverseChainSingleSubstStatement: ('glyphs', 'replacements'),
    }

    gposGlyphsAttrs = {
        CursivePosStatement: ('glyphs', ),
        MarkBasePosStatement: ('base', ),
        MarkLigPosStatement: ('ligatures', ),
        MarkMarkPosStatement: ('baseMarks', ),
        PairPosStatement: ('glyphs1', 'glyphs2', ),
        SinglePosStatement: ('pos', ),
    }

    rules = list(gsubGlyphsAttrs.keys())
    rules.extend(gposGlyphsAttrs)
    rules = tuple(rules)

    def __init__(self, font):
        featuresRawText = StringIO(font.features.text)
        self._font = font
        featuresRawText.name = self._font.path
        parser = Parser(featuresRawText)
        self.featureFile = parser.parse()
        self.lookups = {}  # lookupName: astLookupBlock
        self.classes = {}  # className: astGlyphClassDefinition
        self.features = {}  # featureTag: [astFeatureBlock, ]
        self.languagesReferences = {}  # languageTag: ast
        self.scriptReferences = {}  # scriptTag: ast
        self._rules = {}  # statementType: [astObject,...]
        self._currentFeatureTag = None
        self._currentLookup = None
        self._currentLanguageTag = None
        self._currentScriptTag = None
        self._glyphFeatures = {}
        self._currentElement = self.featureFile
        self._parseStatements()
        self._currentElement = None

    def _parseElement(self, element):
        self._currentElement = element
        if isinstance(element, FeatureBlock):
            self._currentFeatureTag = element.name
            self.features.setdefault(self._currentFeatureTag, []).append(element)
            self._parseStatements()
            self._currentFeatureTag = None
        elif isinstance(element, LookupBlock):
            self.lookups[element.name] = element
            self._currentLookup = element
            element.features = set()
            self._parseStatements()
            if self._currentFeatureTag is not None:
                element.features.add(self._currentFeatureTag)
        elif isinstance(element, LookupReferenceStatement):
            if self._currentFeatureTag is not None:
                element.lookup.features.add(self._currentFeatureTag)
        elif isinstance(element, GlyphClassDefinition):
            self.classes[element.name] = element
        elif isinstance(element, self.rules):
            self._rules.setdefault(type(element), []).append(element)
            element.features = set()
            if self._currentFeatureTag is not None:
                element.features.add(self._currentFeatureTag)
            element.lookup = None
            if self._currentLookup is not None:
                element.lookup = self._currentLookup
            self._parseStatementAttributes()
        elif isinstance(element, LanguageStatement):
            self.languagesReferences.setdefault(element.language, []).append(element)
            self._currentLanguageTag = element.language
        elif isinstance(element, ScriptStatement):
            self.scriptReferences.setdefault(element.script, []).append(element)
            self._currentScriptTag = element.script

    def __getitem__(self, glyphName):
        if glyphName in self._glyphFeatures:
            return self._glyphFeatures[glyphName]
        try:
            self._glyphFeatures[glyphName] = GlyphFeautres(self._font[glyphName])
        except KeyError:
            warn(f"Ignoring the missing glyph `{glyphName}` in the features, statement:\n{str(self._currentElement)}")
            return
        return self._glyphFeatures[glyphName]

    def _parseStatements(self):
        for element in self._currentElement.statements:
            self._parseElement(element)
        self._currentLookup = None
        self._currentLanguageTag = None
        self._currentScriptTag = None

    def _parseStatementAttributes(self):
        # add nested features, lookups, classes, statements attr to RGlyph objects
        statement = self._currentElement
        if type(statement) in self.gsubGlyphsAttrs:
            source, target = self._getGsubStatementGlyphs()
            if isinstance(statement, (AlternateSubstStatement, SingleSubstStatement, ReverseChainSingleSubstStatement)):
                for sg, tg in zip(source, target):
                    self._addGsubAttributesToGlyph([sg], [tg])
            elif isinstance(statement, (LigatureSubstStatement, MultipleSubstStatement)):
                self._addGsubAttributesToGlyph(source, target)

    def _addGsubAttributesToGlyph(self, sourceGlyphs, targetGlyphs):
        statement = self._currentElement
        sourceGlyphs, targetGlyphs = tuple(sourceGlyphs), tuple(targetGlyphs)
        for gn in targetGlyphs:
            glyphFeatures = self[gn]
            if glyphFeatures is not None:
                glyphFeatures.sourceGlyphs.setdefault(sourceGlyphs, []).append(statement)
        for gn in sourceGlyphs:
            glyphFeatures = self[gn]
            if glyphFeatures is not None:
                glyphFeatures.targetGlyphs.setdefault(targetGlyphs, []).append(statement)

    def _getGsubStatementGlyphs(self):
        statement = self._currentElement
        return [_convertToListOfGlyphNames(getattr(statement, a)) for a in self.gsubGlyphsAttrs[type(statement)]]

    def statementsByType(self, elementType, featureTags=set()):
        """
        Get all the elements by type from the feature file. If you provide a featureTags argument,
        then only the statements within those features will be reutrned.
        """
        result = []
        featureTags = self._featureTags(featureTags)
        for element in self._rules.get(elementType, []):
            if element.features & featureTags:
                result.append(element)
        return result

    def _featureTags(self, featureTags):
        if not featureTags:
            return self.features.keys()
        else:
            return set(featureTags)

def _convertToListOfGlyphNames(e):
    # we need to make all the glyph statement consistent because feaLib parser
    # somtimes creates ast objects and sometimes string.
    if isinstance(e, str):
        return [e, ]
    if isinstance(e, GlyphName):
        return [e.glyph, ]
    if isinstance(e, list):
        result = []
        for e2 in e:
            result.extend(_convertToListOfGlyphNames(e2))
        return result
    if isinstance(e, GlyphClassName):
        return _convertToListOfGlyphNames(e.glyphclass.glyphs)
    if isinstance(e, GlyphClass):
        return _convertToListOfGlyphNames(e.glyphs)


def _renameGlyphNames(e, trasnlateMap):
    if isinstance(e, str):
        return trasnlateMap.get(e, e)
    elif isinstance(e, GlyphName):
        e = deepcopy(e)
        e.glyph = trasnlateMap.get(e.glyph, e.glyph)
    elif isinstance(e, GlyphClass):
        e.glyphs = _renameGlyphNames(e.glyphs, trasnlateMap)
    elif isinstance(e, list):
        for e2 in e:
            _renameGlyphNames(e2, trasnlateMap)
    return e

@fontCachedMethod("Features.Changed")
def parser(features):
    return ParsedFeatureFile(features.font)

#  subsetting
"""
Todo:
KNOWN BUGS:
- If these objects are not referenced, they should be removed:
    Classes, LanguageSystemStatement, FeatureReferenceStatement
"""

def _isRule(statement):
    if isinstance(statement,
        (AlternateSubstStatement,
        ChainContextPosStatement,
        ChainContextSubstStatement,
        CursivePosStatement,
        LigatureSubstStatement,
        LookupReferenceStatement,
        LookupBlock,
        MarkBasePosStatement,
        MarkLigPosStatement,
        MarkMarkPosStatement,
        LigatureCaretByIndexStatement,
        LigatureCaretByPosStatement,
        MultipleSubstStatement,
        PairPosStatement,
        ReverseChainSingleSubstStatement,
        SingleSubstStatement,
        SinglePosStatement,
        FeatureReferenceStatement,
        )):
        return True
    return False

def _subsetGlyphs(listOfGlyphSets, glyphsToKeep, appendToResult=True):
    result = []
    for glyphs in listOfGlyphSets:
        if isinstance(glyphs, (list, tuple)):
            result.append(_subsetGlyphs(glyphs, glyphsToKeep, appendToResult=False))
        elif isinstance(glyphs, str):
            if glyphs in glyphsToKeep:
                result.append(glyphs)
            else:
                result.append(None)
        elif glyphs:
            subsetGlyphSet = glyphs.subset(glyphsToKeep)
            if subsetGlyphSet:
                result.append(subsetGlyphSet)
            elif appendToResult:
                result.append([])
        elif appendToResult:
            result.append([])
    return result

def _subsetStatements(statementList, glyphsToKeep):
    result = []
    for statement in statementList:
        if statement.subset(glyphsToKeep):
            result.append(statement)
    return result

def elementSubset(self, glyphsToKeep):
    return self

def glyphNameSubset(self, glyphsToKeep):
    if self.glyph in glyphsToKeep:
        return self

def glyphClassSubset(self, glyphsToKeep):
    remainedGlyphs = []
    for g in self.glyphs:
        if hasattr(g, 'subset'):
            if g.subset(glyphsToKeep):
                remainedGlyphs.append(g)
        elif g in glyphsToKeep:
            remainedGlyphs.append(g)
    self.glyphs = remainedGlyphs
    if self.glyphs:
        return self

def glyphClassNameSubset(self, glyphsToKeep):
    self.glyphclass = self.glyphclass.subset(glyphsToKeep)
    if self.glyphclass:
        return self

def glyphClassDefinitionSubset(self, glyphsToKeep):
    if self.glyphs:
        self.glyphs = self.glyphs.subset(glyphsToKeep)
        if self.glyphs:
            return self

def markClassSubset(self, glyphsToKeep):
    remainedGlyphs = {}
    for glyph, mark in self.glyphs.items():
        result = _subsetGlyphs([glyph], glyphsToKeep)
        if result:
            remainedGlyphs[glyph] = mark
    self.glyphs = remainedGlyphs
    if self.glyphs:
        return self

def markClassNameSubset(self, glyphsToKeep):
    self.markClass = self.markClass.subset(glyphsToKeep)
    if self.markClass:
        return self

def markClassDefinitionSubset(self, glyphsToKeep):
    self.glyphs, self.markClass = _subsetGlyphs([
    self.glyphs, self.markClass], glyphsToKeep)
    if self.glyphs and self.markClass:
        return self

def blockSubset(self, glyphsToKeep):
    self.statements = _subsetStatements(self.statements, glyphsToKeep)

def glyphClassDefStatementSubset(self, glyphsToKeep):
    self.baseGlyphs, self.markGlyphs, self.ligatureGlyphs, self.componentGlyphs = _subsetGlyphs([
    self.baseGlyphs, self.markGlyphs, self.ligatureGlyphs, self.componentGlyphs], glyphsToKeep, appendToResult=True)
    if self.baseGlyphs or self.markGlyphs or self.ligatureGlyphs or self.componentGlyphs:
        return self

def alternateSubstStatementSubset(self, glyphsToKeep):
    self.prefix, self.glyph, self.suffix, self.replacement = _subsetGlyphs([
    self.prefix, self.glyph, self.suffix, self.replacement], glyphsToKeep)
    if self.glyph and self.replacement:
        return self

def numInputGlyphs(self):
    if hasattr(self, 'glyphs'):
        return len(self.glyphs)
    return len(self.glyph)

def chainContextStatementSubset(self, glyphsToKeep):
    self.prefix, self.glyphs, self.suffix = _subsetGlyphs([
    self.prefix, self.glyphs, self.suffix], glyphsToKeep)
    if self.glyphs:
        remainedLookups = []
        numInputGlyphs = len(self.glyphs.glyphSet())
        for lookup in self.lookups:
            if lookup.subset(glyphsToKeep):
                lookupStatements = []
                for s in lookup.statements:
                    if hasattr(s, 'numInputGlyphs'):
                        if s.numInputGlyphs() != numInputGlyphs:
                            continue
                    lookupStatements.append(s)
                lookup.statements = lookupStatements
            if not lookup.isEmpty():
                self.lookups.append(remainedLookups)
        if self.lookups:
            return self

def ignoreStatementsSubset(self, glyphsToKeep):
    self.chainContexts = _subsetGlyphs(self.chainContexts, glyphsToKeep)
    prefix, glyphs, suffix = self.chainContexts[0]
    if glyphs and (prefix or suffix):
        return self

def ligatureSubstStatementSubset(self, glyphsToKeep):
    numComponents = self.numInputGlyphs()
    self.prefix, self.glyphs, self.suffix, self.replacement = _subsetGlyphs([
    self.prefix, self.glyphs, self.suffix, self.replacement
    ], glyphsToKeep)
    if self.glyphs and self.replacement and self.numInputGlyphs() == numComponents:
        return self

def lookupFlagStatementSubset(self, glyphsToKeep):
    if self.markAttachment is not None:
        self.markAttachment = self.markAttachment.subset(glyphsToKeep)
    if self.markFilteringSet is not None:
        self.markFilteringSet = self.markFilteringSet.subset(glyphsToKeep)
    if self.value or self.markAttachment or self.markFilteringSet:
        return self

def lookupReferenceStatementSubset(self, glyphsToKeep):
    self.lookup = self.lookup.subset(glyphsToKeep)
    if self.lookup:
        return self

def subsetMarks(self, glyphsToKeep):
    remainedMarks = {}
    for anchor, mark in dict(self.marks).items():
        if isinstance(mark, tuple):
            continue
        subsetMarkClass = mark.subset(glyphsToKeep)
        if subsetMarkClass:
            remainedMarks[anchor] = subsetMarkClass
    self.marks = remainedMarks.items()
    if self.marks:
        return self

def markBasePosStatementSubset(self, glyphsToKeep):
    self.base = self.base.subset(glyphsToKeep)
    if self.base:
        return self.subsetMarks(glyphsToKeep)

def markLigPosStatementSubset(self, glyphsToKeep):
    self.ligatures = self.ligatures.subset(glyphsToKeep)
    if self.ligatures:
        return self.subsetMarks(glyphsToKeep)

def markMarkPosStatementSubset(self, glyphsToKeep):
    self.baseMarks = self.baseMarks.subset(glyphsToKeep)
    if self.baseMarks:
        return self.subsetMarks(glyphsToKeep)

def multipleSubstStatementSubset(self, glyphsToKeep):
    if hasattr(self.glyph, 'glyphSet'):
        if self.glyph.subset(glyphsToKeep):
            return
    else:
        if self.glyph not in glyphsToKeep:
            return
    numTargetGlyphs = len(self.replacement.glyphSet())
    self.replacement, self.prefix, self.suffix = _subsetGlyphs([
    self.replacement, self.prefix, self.suffix
    ], glyphsToKeep)
    if len(self.replacement.glyphSet()) == numTargetGlyphs:
        return self

def pairPosStatementSubset(self, glyphsToKeep):
    self.glyphs1, self.glyphs2 = _subsetGlyphs([
    self.glyphs1, self.glyphs2], glyphsToKeep)
    if self.glyphs1 and self.glyphs2:
        return self

def singleSubstStatementSubset(self, glyphsToKeep):
    self.prefix, self.suffix, self.glyphs, self.replacements = _subsetGlyphs([
    self.prefix, self.suffix, self.glyphs, self.replacements], glyphsToKeep)
    if self.glyphs and self.replacements:
        if len(self.glyphs[0].glyphSet()) == len(self.replacements[0].glyphSet()):
            return self
        elif len(self.replacements[0].glyphSet()) == 1 and len(self.glyphs[0].glyphSet()) != 0:
            return self

def reverseSingleSubstStatementSubset(self, glyphsToKeep):
    self.old_prefix, self.old_suffix, self.glyphs, self.replacements = _subsetGlyphs([
    self.old_prefix, self.old_suffix, self.glyphs, self.replacements], glyphsToKeep)
    if self.glyphs and self.replacements:
        if len(self.glyphs[0].glyphSet()) == len(self.replacements[0].glyphSet()):
            return self
        elif len(self.replacements[0].glyphSet()) == 1 and len(self.glyphs[0].glyphSet()) != 0:
            return self

def singlePosStatementSubset(self, glyphsToKeep):
    inputGlyphSubset = self.pos[0][0].subset(glyphsToKeep)
    self.pos = [(inputGlyphSubset, self.pos[0][-1])]
    if inputGlyphSubset:
        return self

def dropInSubset(self, glyphsToKeep):
    return

def blockRulesSubset(self, glyphsToKeep):
    self.statements = _subsetStatements(self.statements, glyphsToKeep)
    if not self.isEmpty():
        return self

def blockIsEmpty(self):
    for s in self.statements:
        if _isRule(s):
            return False
    return True

LookupBlock.isEmpty = blockIsEmpty
FeatureBlock.isEmpty = blockIsEmpty
Element.subset = elementSubset
GlyphName.subset = glyphNameSubset
GlyphClass.subset = glyphClassSubset
Block.subset = blockSubset
AttachStatement.subset = glyphClassSubset
LigatureCaretByIndexStatement.subset = glyphClassSubset
LigatureCaretByPosStatement.subset = glyphClassSubset
GlyphClassDefinition.subset = glyphClassDefinitionSubset
GlyphClassName.subset = glyphClassNameSubset
MarkClass.subset = markClassSubset
MarkClassName.subset = markClassNameSubset
MarkClassDefinition.subset = markClassDefinitionSubset
GlyphClassDefStatement.subset = glyphClassDefStatementSubset
AlternateSubstStatement.subset = alternateSubstStatementSubset
ChainContextPosStatement.subset = chainContextStatementSubset
ChainContextSubstStatement.subset = chainContextStatementSubset
CursivePosStatement.subset = glyphClassNameSubset
IgnoreSubstStatement.subset = ignoreStatementsSubset
IgnorePosStatement.subset = ignoreStatementsSubset
LigatureSubstStatement.subset = ligatureSubstStatementSubset
LookupFlagStatement.subset = lookupFlagStatementSubset
LookupReferenceStatement.subset = lookupReferenceStatementSubset
MarkBasePosStatement.subset = markBasePosStatementSubset
MarkLigPosStatement.subset = markLigPosStatementSubset
MarkMarkPosStatement.subset = markMarkPosStatementSubset
MarkBasePosStatement.subsetMarks = subsetMarks
MarkLigPosStatement.subsetMarks = subsetMarks
MarkMarkPosStatement.subsetMarks = subsetMarks
LigatureCaretByIndexStatement.subset = glyphClassSubset
LigatureCaretByPosStatement.subset = glyphClassSubset
MultipleSubstStatement.subset = multipleSubstStatementSubset
PairPosStatement.subset = pairPosStatementSubset
ReverseChainSingleSubstStatement.subset = reverseSingleSubstStatementSubset
SingleSubstStatement.subset = singleSubstStatementSubset
SinglePosStatement.subset = singlePosStatementSubset
SubtableStatement.subset = dropInSubset
LookupBlock.subset = blockRulesSubset
FeatureBlock.subset = blockRulesSubset
AlternateSubstStatement.numInputGlyphs = numInputGlyphs
LigatureSubstStatement.numInputGlyphs = numInputGlyphs
CursivePosStatement.numInputGlyphs = numInputGlyphs
MarkBasePosStatement.numInputGlyphs = numInputGlyphs
MarkLigPosStatement.numInputGlyphs = numInputGlyphs
MarkMarkPosStatement.numInputGlyphs = numInputGlyphs
MultipleSubstStatement.numInputGlyphs = numInputGlyphs
PairPosStatement.numInputGlyphs = numInputGlyphs
SingleSubstStatement.numInputGlyphs = numInputGlyphs
SinglePosStatement.numInputGlyphs = numInputGlyphs

@fontCachedMethod("Features.Changed")
def subset(features, glyphsToKeep=None):
    """
    Return a new features text file with features limited to the glyphsToKeep
    """
    if glyphsToKeep is None:
        glyphsToKeep = features.font.keys()
    featureFile = features.parser.featureFile
    featureFile.subset(glyphsToKeep)
    return featureFile

@fontCachedMethod("Features.Changed")
def getIncludedFilesPaths(features, absolutePaths=True):
    """
    Returns paths of included feature files.
    If absoulutePaths is True, the abs path of the included files will be returned.
    """
    font = features.font
    ufoPath = features.font.path
    ufoName = PurePath(ufoPath).stem
    ufoRoot = PurePath(ufoPath).parent
    featxt = features.text or ""
    buf = StringIO(featxt)
    buf.name = os.path.join(ufoPath, "features.fea")
    parser = Parser(buf, set(font.keys()), followIncludes=False)
    includeFiles = set()
    for s in parser.parse().statements:
        if isinstance(s, IncludeStatement):
            path = os.path.join(ufoRoot, s.filename)
            normalPath = os.path.normpath(path)
            if os.path.exists(normalPath):
                if absolutePaths:
                    includeFiles.add(normalPath)
                else:
                    includeFiles.add(s.filename)
            else:
                print(f"{ufoName} | Feature file doesn't exist in:\n{normalPath}")
    return includeFiles

class GPOSCompiler(FeatureCompiler):
    """
    overrides ufo2ft to exclude ufo existing features in the generated GPOS.
    """

    def setupFeatures(self):
        featureFile = FeatureFile()
        for writer in self.featureWriters:
            writer.write(self.ufo, featureFile, compiler=self)
        self.features = featureFile.asFea()

@fontCachedMethod("Glyph.AnchorsChanged", "Groups.Changed", "Kerning.Changed", "Layer.GlyphAdded", "Layer.GlyphDeleted")
def GPOS(font):
    """
    Generates mark, kern features using ufo2ft.
    """
    skipExport = font.lib.get("public.skipExportGlyphs", [])
    glyphOrder = (gn for gn in font.glyphOrder if gn not in skipExport)
    featureCompiler = GPOSCompiler(font)
    featureCompiler.glyphSet = OrderedDict((gn, font[gn]) for gn in glyphOrder)
    featureCompiler.compile()
    return featureCompiler.features
