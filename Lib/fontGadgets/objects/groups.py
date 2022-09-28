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
