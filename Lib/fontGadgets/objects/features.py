from fontParts.fontshell.features import RFeatures
from fontTools.feaLib.parser import Parser
from fontTools.feaLib.ast import *
from io import StringIO


class ParseFeatureFile():

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

    statementTypes = list(gsubGlyphsAttrs.keys())
    statementTypes.extend(gposGlyphsAttrs)
    statementTypes = tuple(statementTypes)

    def __init__(self, font):
        featuresRawText = StringIO(font.features.text)
        self._font = font
        featuresRawText.name = self._font.path
        parser = Parser(featuresRawText, font.keys())
        self.featureFile = parser.parse()
        self.lookups = {}  # lookupName: astLookupBlock
        self.classes = {}  # className: astGlyphClassDefinition
        self.features = {}  # featureTag: [astFeatureBlock, ]
        self._statements = {}  # statementType: [astObject,...]
        self._currentFeatureTag = None
        self._currentLookup = None
        self._currentElement = self.featureFile
        self._parseStatements()

    def _parseElement(self, element):
        self._currentElement = element
        if isinstance(element, FeatureBlock):
            self.features.setdefault(element.name, []).append(element)
            self._currentFeatureTag = element.name
            self._parseStatements()
            self._currentFeatureTag = None
        elif isinstance(element, LookupBlock):
            self.lookups[element.name] = element
            self._currentLookup = element
            element.features = set()
            self._parseStatements()
            self._currentLookup = None
            if self._currentFeatureTag is not None:
                element.features.add(self._currentFeatureTag)
        elif isinstance(element, LookupReferenceStatement):
            if self._currentFeatureTag is not None:
                element.lookup.features.add(self._currentFeatureTag)
        elif isinstance(element, GlyphClassDefinition):
            self.classes[element.name] = element
        elif isinstance(element, self.statementTypes):
            self._statements.setdefault(type(element), []).append(element)
            element.features = set()
            if self._currentFeatureTag is not None:
                element.features.add(self._currentFeatureTag)
            element.lookup = None
            if self._currentLookup is not None:
                element.lookup = self._currentLookup

    def _parseStatements(self):
        currentElement = self._currentElement
        for element in currentElement.statements:
            self._parseElement(element)
        self._currentElement = currentElement

    def _iterStatementAttrs(self):
        # add nested features, lookups, classes, statements attr to RGlyph objects
        pass

    def statementsByType(self, elementType, featureTags=set()):
        """
        Get all the elements by type from the feature file. If you provide a featureTags argument,
        then only the statements within those features will be reutrned.
        """
        result = []
        featureTags = self._featureTags(featureTags)
        for element in self._statements.get(elementType, []):
            if element.features & featureTags:
                result.append(element)
        return result

    def _featureTags(self, featureTags):
        if not featureTags:
            return self.features.keys()
        else:
            return set(featureTags)

    def glyphSetAlternates(self, glyphs, featureTags=set()):
        """
        Recursively fetch all the given glyphs alternates. Returns a dictionary:
        alternateGlyph: set({featureTag1, featureTag1})
        If you provide a featureTags argument, then only the statements within those
        features will be reutrned.
        """

        alternates = {}
        glyphSet = set(glyphs)
        featureTags = self._featureTags(featureTags)
        while True:
            numAlternates = len(alternates)
            glyphSet = glyphSet | alternates.keys()
            for elementType, attributes in self.gsubGlyphsAttrs.items():
                sourceGlyphsAttr, targetGlyphsAttr = attributes
                for element in self._statements.get(elementType, []):
                    sourceGlyphs = getattr(element, sourceGlyphsAttr)
                    if set(_convertToListOfGlyphNames(sourceGlyphs)) & glyphSet:
                        alternateGlyphs = _convertToListOfGlyphNames(
                            getattr(element, targetGlyphsAttr))
                        for g in alternateGlyphs:
                            features = element.features
                            if element.lookup is not None:
                                features.update(element.lookup.features)
                            alternates.setdefault(
                                g, set()).update(element.features)
            if len(alternates) == numAlternates:
                break
        for g, features in list(alternates.items()):
            if not featureTags & features:
                del alternates[g]
        return alternates


def _convertToListOfGlyphNames(e):
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


def parse(self):
    """
    Returns a feature parser object.
    """
    parsed = ParseFeatureFile(self.font)
    return parsed

RFeatures.parse = parse

def glyphSetAlternates(features, glyphSet, featureTags=set()):
    """
    Recursively fetch all the given glyphs alternates. Returns a dictionary:
    Returns: dict(alternateGlyph = set({featureTag1, featureTag1}))
    If you provide a featureTags argument, then only the statements within those
    features will be reutrned.

    glyphSet: glyph names as an iterable
    featureTags: feature tag names as an iterable
    """
    featureParser = features.parse()
    return featureParser.glyphSetAlternates(glyphSet, featureTags)

RFeatures.glyphSetAlternates = glyphSetAlternates

#  subsetting
"""
Todo:
KNOWN BUGS:
- Feature aalt doesn't get subset if the referenced features are non existent.
    This is because the FeatureReferenceStatement don't point to the FeatureBlock
    to check if they subset or not.
- LanguageSystemStatement don't get subset because they don't belong to glyphs.
- How to subset these objects:
    FeatureReferenceStatement --> FeatureBlock.subset is None
    LanguageSystemStatement --> Block.subset that contains relevant
                        LanguageStatement, ScriptStatement is None
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
                lookups.append(remainedLookups)
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
    if hastattr(self.glyph, 'glyphSet'):
        if self.glyph.subset(glyphsToKeep):
            return
    else:
        if self.glyph not in glyphsToKeep:
            return
    numTargetGlyphs = len(self.replacement.glyphSet())
    self.replacement, self.prefix, self.suffix = _subsetGlyphSet([
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

def subset(features, glyphsToKeep):
    """
    Return a new features text file with features limited to the glyphsToKeep
    """
    featureParser = features.parse()
    featureParser.featureFile.subset(glyphsToKeep)
    return featureParser.featureFile

RFeatures.subset = subset
