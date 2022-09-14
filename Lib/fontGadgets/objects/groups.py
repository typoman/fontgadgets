from fontGadgets.tools import fontCachedMethod, fontMethod
import re
from warnings import warn

RE_GROUP_TAG = re.compile(r'public.kern\d\.')
GROUP_SIDE_TAG = ("public.kern1.", "public.kern2.")

def _isKerningGroup(entry):
	"""
	Return True if the given entry is a kerning group name starting either with
	`public.kern1.` or `public.kern2.`
	"""
	if re.match(RE_GROUP_TAG, entry) is None:
		return False
	return True

@fontCachedMethod("Groups.Changed", "Layer.GlyphAdded", "Layer.GlyphDeleted")
def glyphToKerningGroupMapping(font):
	"""
	GlyphName to raw kerning group name mapping
	"""
	result = [{}, {}]
	for group, members in font.groups.items():
		if _isKerningGroup(group):
			for glyphName in members:
				side, name = _getSideAndRawGroupName(group)
				result[side][glyphName] = name
	return result

@fontCachedMethod("Groups.Changed")
def kerningGroups(font):
	"""
	Kerning groups is a list with two members. First member is left side kerning
	groups and second member is right side groups.
	"""
	result = [{}, {}]
	for group, members in font.groups.items():
		if _isKerningGroup(group):
			side, name = _getSideAndRawGroupName(group)
			result[side][name] = members
	return result

@fontMethod
def setKerningGroups(font, kerningGroups, update=True):
	"""
	Sets the kerning groups to the given one. If update is set to True,
	the old groups will be extended instead of getting removed or reset.
	"""
	fontGroups = dict(font.groups)
	glyphToKerningGroupMapping = font.glyphToKerningGroupMapping

	for side, kernGroups in enumerate(kerningGroups):
		for kernGroupName, newMembers in kernGroups.items():
			for glyphName in newMembers:
				# remove old memberships
				prevKernGroupName = glyphToKerningGroupMapping[side].get(glyphName, None)
				print(prevKernGroupName)
				if prevKernGroupName is not None:
					prevGroupName = convertToKerningGroupName(prevKernGroupName, side)
					prevMembers = list(fontGroups[prevGroupName])
					if prevMembers:
						prevMembers.remove(glyphName)
						if len(prevMembers) > 0:
							fontGroups[prevGroupName] = prevMembers
						else:
							del fontGroups[prevGroupName]
			newGroupName = convertToKerningGroupName(kernGroupName, side)
			if update:
				members = list(fontGroups.get(newGroupName, []))
				members.extend([g for g in newMembers if g not in members])
				fontGroups[newGroupName] = members
			else:
				if newMembers:
					fontGroups[newGroupName] = newMembers
				else:
					del fontGroups[newGroupName]
	if not update:
		for kernGroup in font.kerningGroups.items():
			if kernGroup not in kerningGroups:
				groupName = convertToKerningGroupName(kernGroup)
				del fontGroups[groupName]
	font.groups.clear()
	font.groups.update(fontGroups)
	font.groups.changed()

@fontMethod
def kerningGroupSide(glyph, side):
	"""
	`0` is left side, `1` is right side.
	"""
	if glyph.isRTL:
		side = abs(side - 1)
	return glyph.font.glyphToKerningGroupMapping[side].get(glyph.name, None)

@fontMethod
def _setKerningGroupSide(glyph, kernGroupName, side):
	result = [{}, {}]
	if glyph.isRTL:
		side = abs(side - 1)
	result[side] = {kernGroupName: [glyph.name, ]}
	glyph.font.setKerningGroups(result, update=True)

@fontMethod
def leftSideKerningGroup(glyph):
	return glyph.kerningGroupSide(0)

@fontMethod
def rightSideKerningGroup(glyph):
	return glyph.kerningGroupSide(1)

@fontMethod
def setLeftSideKerningGroup(glyph, kernGroupName):
	glyph._setKerningGroupSide(kernGroupName, 0)

@fontMethod
def setRightSideKerningGroup(glyph, kernGroupName):
	glyph._setKerningGroupSide(kernGroupName, 1)

@fontMethod
def isGrouped(glyph):
	"""
	Returns True if glyph has a kerning group.
	"""
	return glyph.kerningGroupSide(0) is not None or glyph.kerningGroupSide(1) is not None

def _getSideAndRawGroupName(group_name):
	"""
	"""
	match = re.match(RE_GROUP_TAG, group_name)
	if match is not None:
		side = match.group(0)
		return GROUP_SIDE_TAG.index(side), re.split(RE_GROUP_TAG, group_name)[-1]

def getKerningGroupRawName(name):
	"""
	Remvoes the kerning group side tag from the group name.
	"""
	if name is not None and _isKerningGroup(name):
		return name[13:]

def convertToKerningGroupName(name, side):
	"""
	Converts the group name to kerning group name
	"""
	assert side in (0, 1)
	prefix = GROUP_SIDE_TAG[side]
	if _isKerningGroup(name):
		warn(f"Kerning group name already starts with a prefix, it will be removed:\n{name}")
		name = name[13:]
	return f"{prefix}{name}"

def _tests():
	"""
	>>> testFont["twoArabic"].isGrouped
	True

	>>> testFont["twoArabic"].rightSideKerningGroup

	>>> testFont["alef"].leftSideKerningGroup
	"""

"""
	>>> convertToKerningGroupName('A', 0)
	'public.kern1.A'
	>>> convertToKerningGroupName('ae', 1)
	'public.kern2.ae'

	>>> getKerningGroupRawName('public.kern1.A')
	'A'
	>>> getKerningGroupRawName('public.kern2.ae')
	'ae'
	>>> getKerningGroupRawName('a') is None
	True

	>>> _getSideAndRawGroupName('public.kern1.A')
	(0, 'A')
	>>> _getSideAndRawGroupName('public.kern2.B')
	(1, 'B')
	>>> _getSideAndRawGroupName('a') is None
	True
py
	>>> _isKerningGroup('public.kern1.A')
	True
	>>> _isKerningGroup('public.kern2.AE')
	True
	>>> _isKerningGroup('a')
	False

	>>> testFont.glyphToKerningGroupMapping
	[{'alef': 'alef', 'alef.fina': 'alef', 'alef.short': 'alef', 'alef.fina.short': 'alef', 'alefMadda': 'alefA', 'alefMadda.fina': 'alefA', 'alefHamzaabove': 'alefHA', 'alefHamzaabove.fina': 'alefHA', 'alefWasla': 'alefHA', 'alefWasla.fina': 'alefHA', 'alefHamzabelow': 'alefHB', 'alefHamzabelow.fina': 'alefHB', 'behDotless': 'be', 'behDotless.fina': 'be', 'fehDotless': 'be', 'fehDotless.fina': 'be', 'kaf.fina': 'be', 'keheh': 'be', 'keheh.fina': 'be', 'veh': 'be', 'teh.fina': 'be', 'beh': 'be', 'gaf.fina': 'be', 'peh.fina': 'be', 'teh': 'be', 'theh': 'be', 'peh': 'be', 'theh.fina': 'be', 'beh.fina': 'be', 'feh.fina': 'be', 'feh': 'be', 'tteh.fina': 'be', 'veh.fina': 'be', 'tteh': 'be', 'dal': 'dal', 'dal.fina': 'dal', 'thal.fina': 'dal', 'ddal': 'dal', 'ddal.fina': 'dal', 'thal': 'dal', 'twoArabic': 'do', 'twoPersian': 'do', 'qafDotless': 'ghaf', 'qafDotless.fina': 'ghaf', 'qaf': 'ghaf', 'qaf.fina': 'ghaf', 'sevenPersian': 'haft', 'sevenArabic': 'haft', 'eightPersian': 'hasht', 'eightArabic': 'hasht', 'hehgoal': 'he', 'hehgoalHamzaabove': 'he', 'tehMarbutagoal': 'he', 'aeArabic': 'he', 'tehMarbuta': 'he', 'heh': 'he', 'aeArabic.fina': 'he.f', 'heh.fina': 'he.f', 'jeem': 'jim', 'jeem.fina': 'jim', 'hah': 'jim', 'hah.fina': 'jim', 'khah': 'jim', 'khah.fina': 'jim', 'tcheh': 'jim', 'tcheh.fina': 'jim', 'ain': 'jim', 'ain.fina': 'jim', 'ghain.fina': 'jim', 'lam.init_jeem.fina.liga': 'jim', 'lam.init_hah.fina.liga': 'jim', 'lam.init_khah.fina.liga': 'jim', 'lam.init_tcheh.fina.liga': 'jim', 'lam.medi_alef.fina': 'lam_alef.fina', 'lam.medi_alefWasla.fina': 'lam_alef.fina', 'lam.medi_alefHamzaabove.fina': 'lam_alef.fina', 'lam.medi_alefMadda.fina': 'lam_alef.fina', 'lam.medi_alefHamzabelow.fina': 'lam_alef.fina', 'lam.init_alefWasla.fina': 'lam_alefar', 'lam.init_alefMadda.fina': 'lam_alefar', 'lam.init_alefHamzaabove.fina': 'lam_alefar', 'lam.init_alefHamzabelow.fina': 'lam_alefar', 'lam.init_alef.fina': 'lam_alefar', 'meem': 'mim.fina', 'meem.fina': 'mim.fina', 'lam.init_meem.fina.liga': 'mim.fina', 'ninePersian': 'noh', 'nineArabic': 'noh', 'reh': 're', 'reh.fina': 're', 'zain': 're', 'zain.fina': 're', 'yehHamzaabove.medi_reh.fina.liga': 're', 'yehHamzaabove.medi_zain.fina.liga': 're', 'beh.medi_reh.fina.liga': 're', 'beh.medi_zain.fina.liga': 're', 'teh.medi_reh.fina.liga': 're', 'teh.medi_zain.fina.liga': 're', 'theh.medi_reh.fina.liga': 're', 'theh.medi_zain.fina.liga': 're', 'noon.medi_reh.fina.liga': 're', 'noon.medi_zain.fina.liga': 're', 'yeh.medi_reh.fina.liga': 're', 'yeh.medi_zain.fina.liga': 're', 'sheen.init_reh.fina.liga': 're', 'seen.init_reh.fina.liga': 're', 'sad.init_reh.fina.liga': 're', 'dad.init_reh.fina.liga': 're', 'sheen.medi_reh.fina.liga': 're', 'seen.medi_reh.fina.liga': 're', 'sad.medi_reh.fina.liga': 're', 'dad.medi_reh.fina.liga': 're', 'seen.init_zain.fina.liga': 're', 'seen.medi_zain.fina.liga': 're', 'sheen.init_zain.fina.liga': 're', 'sheen.medi_zain.fina.liga': 're', 'sad.init_zain.fina.liga': 're', 'sad.medi_zain.fina.liga': 're', 'dad.init_zain.fina.liga': 're', 'dad.medi_zain.fina.liga': 're', 'alefMaksura_reh.fina': 're', 'alefMaksura_zain.fina': 're', 'yehPersian.medi_zain.fina.liga': 're', 'yehPersian.medi_reh.fina.liga': 're', 'peh.medi_reh.fina.liga': 're', 'peh.medi_zain.fina.liga': 're', 'zeroArabic': 'sefr', 'zeroPersian': 'sefr', 'seen': 'sin', 'seen.fina': 'sin', 'sheen': 'sin', 'sheen.fina': 'sin', 'sad': 'sin', 'sad.fina': 'sin', 'dad': 'sin', 'dad.fina': 'sin', 'lam': 'sin', 'lam.fina': 'sin', 'noonghunna': 'sin', 'noonghunna.fina': 'sin', 'noon': 'sin', 'noon.fina': 'sin', 'yehHamzaabove.medi_noon.fina.liga': 'sin', 'beh.medi_noon.fina.liga': 'sin', 'teh.medi_noon.fina.liga': 'sin', 'theh.medi_noon.fina.liga': 'sin', 'noon.medi_noon.fina.liga': 'sin', 'yeh.medi_noon.fina.liga': 'sin', 'alefMaksura_noon.fina': 'sin', 'alefMaksura_noonghunna': 'sin', 'peh.medi_noon.fina.liga': 'sin', 'yehPersian.medi_noon.fina.liga': 'sin', 'fourPersian': 'threear', 'threeArabic': 'threear', 'threePersian': 'threear', 'wawHamzaabove': 'wawar', 'waw': 'wawar', 'wawHamzaabove.fina': 'wawar', 'waw.fina': 'wawar', 'yehPersian': 'ye', 'yehPersian.fina': 'ye', 'alefMaksura': 'ye', 'alefMaksura.fina': 'ye', 'yeh': 'ye', 'yeh.fina': 'ye', 'yehHamzaabove': 'ye', 'yehHamzaabove.fina': 'ye', 'yeh.init_yehPersian.fina.liga': 'ye', 'yehHamzaabove.init_yehHamzaabove.fina.liga': 'ye', 'yehHamzaabove.medi_yehHamzaabove.fina.liga': 'ye', 'beh.init_yehHamzaabove.fina.liga': 'ye', 'beh.medi_yehHamzaabove.fina.liga': 'ye', 'teh.init_yehHamzaabove.fina.liga': 'ye', 'teh.medi_yehHamzaabove.fina.liga': 'ye', 'theh.init_yehHamzaabove.fina.liga': 'ye', 'theh.medi_yehHamzaabove.fina.liga': 'ye', 'jeem.init_yehHamzaabove.fina.liga': 'ye', 'jeem.medi_yehHamzaabove.fina.liga': 'ye', 'hah.init_yehHamzaabove.fina.liga': 'ye', 'hah.medi_yehHamzaabove.fina.liga': 'ye', 'khah.init_yehHamzaabove.fina.liga': 'ye', 'khah.medi_yehHamzaabove.fina.liga': 'ye', 'yehHamzaabove.init_alefMaksura.fina.liga': 'ye', 'yehHamzaabove.init_yeh.fina.liga': 'ye', 'beh.init_alefMaksura.fina.liga': 'ye', 'beh.init_yeh.fina.liga': 'ye', 'teh.init_alefMaksura.fina.liga': 'ye', 'teh.init_yeh.fina.liga': 'ye', 'theh.init_alefMaksura.fina.liga': 'ye', 'theh.init_yeh.fina.liga': 'ye', 'feh.init_alefMaksura.fina.liga': 'ye', 'feh.init_yeh.fina.liga': 'ye', 'qaf.init_alefMaksura.fina.liga': 'ye', 'qaf.init_yeh.fina.liga': 'ye', 'kaf.init_alefMaksura.fina.liga': 'ye', 'kaf.init_yeh.fina.liga': 'ye', 'lam.init_alefMaksura.fina': 'ye', 'lam.init_yeh.fina.liga': 'ye', 'noon.init_alefMaksura.fina.liga': 'ye', 'noon.init_yeh.fina.liga': 'ye', 'heh.init_alefMaksura.fina.liga': 'ye', 'heh.init_yeh.fina.liga': 'ye', 'yeh.init_alefMaksura.fina.liga': 'ye', 'yeh.init_yeh.fina.liga': 'ye', 'yehHamzaabove.medi_alefMaksura.fina.liga': 'ye', 'yehHamzaabove.medi_yeh.fina.liga': 'ye', 'beh.medi_alefMaksura.fina.liga': 'ye', 'beh.medi_yeh.fina.liga': 'ye', 'teh.medi_alefMaksura.fina.liga': 'ye', 'teh.medi_yeh.fina.liga': 'ye', 'theh.medi_alefMaksura.fina.liga': 'ye', 'theh.medi_yeh.fina.liga': 'ye', 'kaf.medi_alefMaksura.fina.liga': 'ye', 'kaf.medi_yeh.fina.liga': 'ye', 'lam.medi_alefMaksura.fina': 'ye', 'lam.medi_yeh.fina.liga': 'ye', 'noon.medi_alefMaksura.fina.liga': 'ye', 'noon.medi_yeh.fina.liga': 'ye', 'yeh.medi_alefMaksura.fina.liga': 'ye', 'yeh.medi_yeh.fina.liga': 'ye', 'ain.init_alefMaksura.fina.liga': 'ye', 'ain.init_yeh.fina.liga': 'ye', 'ghain.init_alefMaksura.fina.liga': 'ye', 'ghain.init_yeh.fina.liga': 'ye', 'seen.init_alefMaksura.fina.liga': 'ye', 'seen.init_yeh.fina.liga': 'ye', 'sheen.init_alefMaksura.fina.liga': 'ye', 'sheen.init_yeh.fina.liga': 'ye', 'hah.init_alefMaksura.fina.liga': 'ye', 'hah.init_yeh.fina.liga': 'ye', 'jeem.init_alefMaksura.fina.liga': 'ye', 'jeem.init_yeh.fina.liga': 'ye', 'khah.init_alefMaksura.fina.liga': 'ye', 'khah.init_yeh.fina.liga': 'ye', 'sad.init_alefMaksura.fina.liga': 'ye', 'sad.init_yeh.fina.liga': 'ye', 'dad.init_alefMaksura.fina.liga': 'ye', 'dad.init_yeh.fina.liga': 'ye', 'ain.medi_alefMaksura.fina.liga': 'ye', 'ain.medi_yeh.fina.liga': 'ye', 'ghain.medi_alefMaksura.fina.liga': 'ye', 'ghain.medi_yeh.fina.liga': 'ye', 'seen.medi_alefMaksura.fina.liga': 'ye', 'seen.medi_yeh.fina.liga': 'ye', 'sheen.medi_alefMaksura.fina.liga': 'ye', 'sheen.medi_yeh.fina.liga': 'ye', 'hah.medi_alefMaksura.fina.liga': 'ye', 'hah.medi_yeh.fina.liga': 'ye', 'jeem.medi_alefMaksura.fina.liga': 'ye', 'jeem.medi_yeh.fina.liga': 'ye', 'khah.medi_alefMaksura.fina.liga': 'ye', 'khah.medi_yeh.fina.liga': 'ye', 'sad.medi_alefMaksura.fina.liga': 'ye', 'sad.medi_yeh.fina.liga': 'ye', 'dad.medi_alefMaksura.fina.liga': 'ye', 'dad.medi_yeh.fina.liga': 'ye', 'seen.init_yehHamzaabove.fina.liga': 'ye', 'seen.medi_yehHamzaabove.fina.liga': 'ye', 'sheen.init_yehHamzaabove.fina.liga': 'ye', 'sheen.medi_yehHamzaabove.fina.liga': 'ye', 'sad.init_yehHamzaabove.fina.liga': 'ye', 'sad.medi_yehHamzaabove.fina.liga': 'ye', 'dad.init_yehHamzaabove.fina.liga': 'ye', 'dad.medi_yehHamzaabove.fina.liga': 'ye', 'ain.init_yehHamzaabove.fina.liga': 'ye', 'ain.medi_yehHamzaabove.fina.liga': 'ye', 'ghain.init_yehHamzaabove.fina.liga': 'ye', 'ghain.medi_yehHamzaabove.fina.liga': 'ye', 'feh.init_yehHamzaabove.fina.liga': 'ye', 'qaf.init_yehHamzaabove.fina.liga': 'ye', 'kaf.init_yehHamzaabove.fina.liga': 'ye', 'kaf.medi_yehHamzaabove.fina.liga': 'ye', 'lam.init_yehHamzaabove.fina.liga': 'ye', 'lam.medi_yehHamzaabove.fina.liga': 'ye', 'noon.init_yehHamzaabove.fina.liga': 'ye', 'noon.medi_yehHamzaabove.fina.liga': 'ye', 'heh.init_yehHamzaabove.fina.liga': 'ye', 'yeh.init_yehHamzaabove.fina.liga': 'ye', 'yeh.medi_yehHamzaabove.fina.liga': 'ye', 'behDotless.init_alefMaksura.fina.liga': 'ye', 'behDotless.medi_alefMaksura.fina.liga': 'ye', 'peh.init_yehHamzaabove.fina.liga': 'ye', 'peh.medi_yehHamzaabove.fina.liga': 'ye', 'peh.init_alefMaksura.fina.liga': 'ye', 'peh.medi_alefMaksura.fina.liga': 'ye', 'peh.init_yeh.fina.liga': 'ye', 'peh.medi_yeh.fina.liga': 'ye', 'tcheh.init_yehHamzaabove.fina.liga': 'ye', 'tcheh.medi_yehHamzaabove.fina.liga': 'ye', 'tcheh.init_alefMaksura.fina.liga': 'ye', 'tcheh.medi_alefMaksura.fina.liga': 'ye', 'tcheh.init_yeh.fina.liga': 'ye', 'tcheh.medi_yeh.fina.liga': 'ye', 'fehDotless.init_alefMaksura.fina.liga': 'ye', 'veh.init_yehHamzaabove.fina.liga': 'ye', 'veh.init_alefMaksura.fina.liga': 'ye', 'veh.init_yeh.fina.liga': 'ye', 'keheh.init_yeh.fina.liga': 'ye', 'gaf.init_yehHamzaabove.fina.liga': 'ye', 'gaf.medi_yehHamzaabove.fina.liga': 'ye', 'gaf.init_alefMaksura.fina.liga': 'ye', 'gaf.medi_alefMaksura.fina.liga': 'ye', 'gaf.init_yeh.fina.liga': 'ye', 'gaf.medi_yeh.fina.liga': 'ye', 'ain.init_yehPersian.fina.liga': 'ye', 'ain.medi_yehPersian.fina.liga': 'ye', 'beh.init_yehPersian.fina.liga': 'ye', 'peh.init_yehPersian.fina.liga': 'ye', 'teh.init_yehPersian.fina.liga': 'ye', 'noon.init_yehPersian.fina.liga': 'ye', 'theh.init_yehPersian.fina.liga': 'ye', 'yehPersian.init_yehPersian.fina.liga': 'ye', 'yehHamzaabove.init_yehPersian.fina.liga': 'ye', 'beh.medi_yehPersian.fina.liga': 'ye', 'peh.medi_yehPersian.fina.liga': 'ye', 'teh.medi_yehPersian.fina.liga': 'ye', 'noon.medi_yehPersian.fina.liga': 'ye', 'theh.medi_yehPersian.fina.liga': 'ye', 'yeh.medi_yehPersian.fina.liga': 'ye', 'yehHamzaabove.medi_yehPersian.fina.liga': 'ye', 'sad.init_yehPersian.fina.liga': 'ye', 'sad.medi_yehPersian.fina.liga': 'ye', 'dad.init_yehPersian.fina.liga': 'ye', 'dad.medi_yehPersian.fina.liga': 'ye', 'fehDotless.init_yehPersian.fina.liga': 'ye', 'feh.init_yehPersian.fina.liga': 'ye', 'qaf.init_yehPersian.fina.liga': 'ye', 'gaf.init_yehPersian.fina.liga': 'ye', 'gaf.medi_yehPersian.fina.liga': 'ye', 'ghain.init_yehPersian.fina.liga': 'ye', 'ghain.medi_yehPersian.fina.liga': 'ye', 'hah.init_yehPersian.fina.liga': 'ye', 'hah.medi_yehPersian.fina.liga': 'ye', 'heh.init_yehPersian.fina.liga': 'ye', 'jeem.init_yehPersian.fina.liga': 'ye', 'jeem.medi_yehPersian.fina.liga': 'ye', 'keheh.init_yehPersian.fina.liga': 'ye', 'keheh.medi_yehPersian.fina.liga': 'ye', 'khah.init_yehPersian.fina.liga': 'ye', 'khah.medi_yehPersian.fina.liga': 'ye', 'lam.init_yehPersian.fina.liga': 'ye', 'lam.medi_yehPersian.fina.liga': 'ye', 'seen.init_yehPersian.fina.liga': 'ye', 'seen.medi_yehPersian.fina.liga': 'ye', 'sheen.init_yehPersian.fina.liga': 'ye', 'sheen.medi_yehPersian.fina.liga': 'ye', 'yehbarree': 'yebar', 'yehbarreeHamzaabove': 'yebar', 'yehbarree.fina': 'yebar2', 'yehbarreeHamzaabove.fina': 'yebar2', 'oneArabic': 'yek', 'onePersian': 'yek', 'jeh': 'zhe', 'jeh.fina': 'zhe', 'rreh': 'zhe', 'rreh.fina': 'zhe'}, {'ghain': 'ainar', 'alef': 'alef', 'alef.short': 'alef', 'kaf': 'alef', 'lam.init': 'alef', 'alefMadda': 'alefHA', 'alefHamzaabove': 'alefHA', 'alefWasla': 'alefHA', 'behDotless': 'be', 'behDotless.init': 'be', 'beh': 'be', 'peh': 'be', 'teh': 'be', 'theh': 'be', 'tteh': 'be', 'beh.init': 'be.init', 'yeh.init_yehPersian.fina.liga': 'bePe', 'behDotless.init_alefMaksura.fina.liga': 'beYeh', 'beh.init_yeh.fina.liga': 'beYeh', 'beh.init_yehHamzaabove.fina.liga': 'beYeh', 'beh.init_yehPersian.fina.liga': 'beYeh', 'beh.init_alefMaksura.fina.liga': 'beYeh', 'dal': 'dal', 'ddal': 'dal', 'thal': 'dal', 'ain': 'eyn', 'ain.init': 'eyn.i', 'ain.init_yehPersian.fina.liga': 'eyn.i', 'ghain.init': 'eyn.i', 'ghain.init_alefMaksura.fina.liga': 'eyn.i', 'ain.init_alefMaksura.fina.liga': 'eyn.i', 'ghain.init_yehPersian.fina.liga': 'eyn.i', 'ghain.init_yehHamzaabove.fina.liga': 'eyn.i', 'ghain.init_yeh.fina.liga': 'eyn.i', 'ain.init_yeh.fina.liga': 'eyn.i', 'ain.init_yehHamzaabove.fina.liga': 'eyn.i', 'fehDotless': 'fe', 'fehDotless.init': 'fe', 'veh': 'fe', 'qaf.init': 'fe', 'feh.init': 'fe', 'feh': 'fe', 'veh.init': 'fe', 'feh.init_alefMaksura.fina.liga': 'feYe', 'feh.init_yeh.fina.liga': 'feYe', 'qaf.init_alefMaksura.fina.liga': 'feYe', 'qaf.init_yeh.fina.liga': 'feYe', 'feh.init_yehHamzaabove.fina.liga': 'feYe', 'qaf.init_yehHamzaabove.fina.liga': 'feYe', 'fehDotless.init_alefMaksura.fina.liga': 'feYe', 'veh.init_yehHamzaabove.fina.liga': 'feYe', 'veh.init_alefMaksura.fina.liga': 'feYe', 'veh.init_yeh.fina.liga': 'feYe', 'fehDotless.init_yehPersian.fina.liga': 'feYe', 'feh.init_yehPersian.fina.liga': 'feYe', 'qaf.init_yehPersian.fina.liga': 'feYe', 'qafDotless': 'ghaf', 'qaf': 'ghaf', 'waw': 'ghaf', 'wawHamzaabove': 'ghaf', 'sevenPersian': 'haft', 'sevenArabic': 'haft', 'eightPersian': 'hasht', 'eightArabic': 'hasht', 'jeem.init': 'jim', 'hah.init': 'jim', 'khah.init': 'jim', 'tcheh.init': 'jim', 'jeem.init_yehHamzaabove.fina.liga': 'jim', 'hah.init_yehHamzaabove.fina.liga': 'jim', 'khah.init_yehHamzaabove.fina.liga': 'jim', 'hah.init_alefMaksura.fina.liga': 'jim', 'hah.init_yeh.fina.liga': 'jim', 'jeem.init_alefMaksura.fina.liga': 'jim', 'jeem.init_yeh.fina.liga': 'jim', 'khah.init_alefMaksura.fina.liga': 'jim', 'khah.init_yeh.fina.liga': 'jim', 'tcheh.init_yehHamzaabove.fina.liga': 'jim', 'tcheh.init_alefMaksura.fina.liga': 'jim', 'tcheh.init_yeh.fina.liga': 'jim', 'hah.init_yehPersian.fina.liga': 'jim', 'jeem.init_yehPersian.fina.liga': 'jim', 'khah.init_yehPersian.fina.liga': 'jim', 'jeem': 'jim.isol', 'hah': 'jim.isol', 'khah': 'jim.isol', 'tcheh': 'jim.isol', 'kaf.init': 'kaf', 'keheh': 'kaf', 'keheh.init': 'kaf', 'gaf.init': 'kaf', 'kaf.init_alefMaksura.fina.liga': 'kafYe', 'kaf.init_yeh.fina.liga': 'kafYe', 'kaf.init_yehHamzaabove.fina.liga': 'kafYe', 'keheh.init_yeh.fina.liga': 'kafYe', 'gaf.init_yehHamzaabove.fina.liga': 'kafYe', 'gaf.init_alefMaksura.fina.liga': 'kafYe', 'gaf.init_yeh.fina.liga': 'kafYe', 'gaf.init_yehPersian.fina.liga': 'kafYe', 'keheh.init_yehPersian.fina.liga': 'kafYe', 'gaf': 'kafar.init', 'lam.init_hah.medi.liga': 'lamJim', 'lam.init_khah.medi.liga': 'lamJim', 'lam.init_jeem.medi.liga': 'lamJim', 'lam.init_tcheh.medi.liga': 'lamJim', 'lam.init_meem.fina.liga': 'lamMim', 'lam.init_meem.medi.liga': 'lamMim', 'lam.init_alefMaksura.fina': 'lamYe', 'lam.init_yeh.fina.liga': 'lamYe', 'lam.init_yehHamzaabove.fina.liga': 'lamYe', 'lam.init_yehPersian.fina.liga': 'lamYe', 'lam.init_alef.fina': 'lam_alefar', 'lam.init_alefMadda.fina': 'lam_alefar', 'lam.init_alefHamzaabove.fina': 'lam_alefar', 'lam.init_alefHamzabelow.fina': 'lam_alefar', 'lam.init_alefWasla.fina': 'lam_alefar', 'meem': 'mim', 'meem.init': 'mim', 'hehgoal': 'mim', 'hehDoachashmee': 'mim', 'hehDoachashmee.init': 'mim', 'hehgoalHamzaabove': 'mim', 'tehMarbutagoal': 'mim', 'aeArabic': 'mim', 'tehMarbuta': 'mim', 'heh': 'mim', 'heh.isol': 'mim', 'heh.init': 'mim', 'heh.init_alefMaksura.fina.liga': 'mim', 'heh.init_yeh.fina.liga': 'mim', 'heh.init_yehHamzaabove.fina.liga': 'mim', 'heh.init_yehPersian.fina.liga': 'mim', 'noon.init_alefMaksura.fina.liga': 'neYe', 'noon.init_yeh.fina.liga': 'neYe', 'noon.init_yehHamzaabove.fina.liga': 'neYe', 'noon.init_yehPersian.fina.liga': 'neYe', 'peh.init': 'pe', 'yehPersian.init': 'pe', 'yeh.init': 'pe', 'yeh.init_alefMaksura.fina.liga': 'peYeh', 'yeh.init_yeh.fina.liga': 'peYeh', 'yeh.init_yehHamzaabove.fina.liga': 'peYeh', 'peh.init_yehHamzaabove.fina.liga': 'peYeh', 'peh.init_alefMaksura.fina.liga': 'peYeh', 'peh.init_yeh.fina.liga': 'peYeh', 'peh.init_yehPersian.fina.liga': 'peYeh', 'yehPersian.init_yehPersian.fina.liga': 'peYeh', 'reh': 're', 'zain': 're', 'sad': 'sad', 'sad.init': 'sad', 'dad': 'sad', 'dad.init': 'sad', 'tah': 'sad', 'tah.init': 'sad', 'zah': 'sad', 'zah.init': 'sad', 'sad.init_alefMaksura.fina.liga': 'sad', 'sad.init_yeh.fina.liga': 'sad', 'dad.init_alefMaksura.fina.liga': 'sad', 'dad.init_yeh.fina.liga': 'sad', 'sad.init_reh.fina.liga': 'sad', 'sad.init_yehHamzaabove.fina.liga': 'sad', 'sad.init_zain.fina.liga': 'sad', 'dad.init_yehHamzaabove.fina.liga': 'sad', 'sad.init_yehPersian.fina.liga': 'sad', 'dad.init_yehPersian.fina.liga': 'sad', 'zeroArabic': 'sefr', 'zeroPersian': 'sefr', 'seen': 'sin', 'seen.init': 'sin', 'seen.init_alefMaksura.fina.liga': 'sin', 'seen.init_reh.fina.liga': 'sin', 'sheen.init': 'sin', 'sheen.init_yeh.fina.liga': 'sin', 'sheen.init_alefMaksura.fina.liga': 'sin', 'seen.init_yehPersian.fina.liga': 'sin', 'sheen': 'sin', 'sheen.init_yehHamzaabove.fina.liga': 'sin', 'sheen.init_yehPersian.fina.liga': 'sin', 'seen.init_yehHamzaabove.fina.liga': 'sin', 'seen.init_yeh.fina.liga': 'sin', 'teh.init': 'the', 'theh.init': 'the', 'tteh.init': 'the', 'noon.init': 'the', 'yehHamzaabove.init': 'the', 'yehHamzaabove.init_yehHamzaabove.fina.liga': 'theYe', 'teh.init_yehHamzaabove.fina.liga': 'theYe', 'theh.init_yehHamzaabove.fina.liga': 'theYe', 'yehHamzaabove.init_alefMaksura.fina.liga': 'theYe', 'yehHamzaabove.init_yeh.fina.liga': 'theYe', 'teh.init_alefMaksura.fina.liga': 'theYe', 'teh.init_yeh.fina.liga': 'theYe', 'theh.init_alefMaksura.fina.liga': 'theYe', 'theh.init_yeh.fina.liga': 'theYe', 'teh.init_yehPersian.fina.liga': 'theYe', 'theh.init_yehPersian.fina.liga': 'theYe', 'yehHamzaabove.init_yehPersian.fina.liga': 'theYe', 'yehPersian': 'ye', 'alefMaksura': 'ye', 'yeh': 'ye', 'yehHamzaabove': 'ye', 'yehbarree': 'yebar', 'yehbarreeHamzaabove': 'yebar', 'oneArabic': 'yek', 'twoArabic': 'yek', 'threeArabic': 'yek', 'onePersian': 'yek', 'twoPersian': 'yek', 'threePersian': 'yek', 'fourPersian': 'yek', 'fourPersian.urdu': 'yek', 'jeh': 'zhe', 'rreh': 'zhe'}]

	>>> testFont["A"].isGrouped
	False

	>>> testFont["A"].rightSideKerningGroup
	>>> testFont["A"].leftSideKerningGroup
	'A'

	>>> testFont["A"].setRightSideKerningGroup("A")
	None
	>>> testFont.glyphToKerningGroupMapping
	[{'A': 'A', 'Aacute': 'A', 'Acircumflex': 'A'}, {'t': 't', 'tcaron': 't', 'A': 'A'}]
	>>> testFont["A"].rightSideKerningGroup
	'A'
"""


