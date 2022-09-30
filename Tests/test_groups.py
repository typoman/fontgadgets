from fontGadgets.objects.groups import *
from main import *

@pytest.fixture
def font():
	groups = {
	'public.kern1.C': ('C', 'Ccedilla'),
	'public.kern1.O': ('D', 'O', 'Ograve'),
	'public.kern1.sin': ('seen', 'sad'),
	'public.kern2.H': ('D', 'E'),
	'public.kern2.O': ('C', 'Ccedilla', 'O', 'Ograve'),
	'public.kern2.sad': ('sad', 'tah'),
	'public.kern2.sin': ('seen', 'seen.init'),
	'control': ('seen', )
	}

	cmap = {
	67: 'C',
	199: 'Ccedilla',
	68: 'D',
	69: 'E',
	79: 'O',
	210: 'Ograve',
	1587: 'seen',
	1589: 'sad',
	1591: 'tah',
	65203: 'seen.init',
	65228: 'ain.medi'
	}

	font = Font()
	font.groups.update(groups)
	for un, gn in cmap.items():
		font.newGlyph(gn).unicodes = [un]
	return font

def test_glyphToKerningGroupMapping(font):
	side1 = {
			'C': 'C',
			'Ccedilla': 'C',
			'D': 'O',
			'O': 'O',
			'Ograve': 'O',
			'seen': 'sin',
			'sad': 'sin'
			}
	side2 = {
			'D': 'H',
			'E': 'H',
			'C': 'O',
			'Ccedilla': 'O',
			'O': 'O',
			'Ograve': 'O',
			'sad': 'sad',
			'tah': 'sad',
			'seen': 'sin',
			'seen.init': 'sin'
			}
	assert font.kerningGroups.glyphToKerningGroupMapping == (side1, side2)

def test_kerningGroups(font):
	side1 = {
			'C': ('C', 'Ccedilla'),
			'O': ('D', 'O', 'Ograve'),
			'sin': ('seen', 'sad')
			}
	side2 = {
			'H':  ('D', 'E'),
			'O':   ('C', 'Ccedilla', 'O', 'Ograve'),
			'sad': ('sad', 'tah'),
			'sin': ('seen', 'seen.init')
			}
	assert font.kerningGroups.items() == (side1, side2)

@pytest.mark.parametrize("kernGroups, expected", [
	(({'H': ('D', 'E')}, {'sin': ('seen', 'sad')}),
		{'public.kern1.H': ('D', 'E'), 'public.kern2.sin': ('seen', 'sad'), 'control': ('seen', )}), # both items
	(({}, {'sad': ('sad', 'tah')}),
		{'public.kern2.sad': ('sad', 'tah'), 'control': ('seen', )}), # first item
	(({'O': ('C', 'Ccedilla', 'O', 'Ograve')}, {}),
		{'public.kern1.O': ('C', 'Ccedilla', 'O', 'Ograve'), 'control': ('seen', )}), # second item
	])
def test_setAllKerningGroups(font, kernGroups, expected):
	font.kerningGroups.set(kernGroups)
	assert font.groups == expected

def test_clearKerningGroups(font):
	expected = {
	'control': ('seen', )
	}
	font.kerningGroups.clear()
	assert font.groups == expected

@pytest.mark.parametrize("glyphName, expected", [
	('seen', True),
	('ain.medi', False)
	])
def test_isGrouped(font, glyphName, expected):
	assert font[glyphName].isGrouped is expected

@pytest.mark.parametrize("glyphName, expected", [
	('seen.init', None),
	('ain.medi', None),
	('sad', 'sin'),
	('D', 'H'),
	('tah', None),
	('C', 'O'),
	])
def test_leftSideKerningGroup(font, glyphName, expected):
	assert font[glyphName].leftSideKerningGroup == expected

@pytest.mark.parametrize("glyphName, expected", [
	('seen.init', 'sin'),
	('ain.medi', None),
	('sad', 'sad'),
	('E', None),
	('D', 'O'),
	('Ccedilla', 'C'),
	])
def test_rightSideKerningGroup(font, glyphName, expected):
	assert font[glyphName].rightSideKerningGroup == expected

@pytest.mark.parametrize("glyphName, expected", [
	('seen.init', 'test1'), # rtl
	('D', 'test2'), # ltr
	('sad', None),
	])
def test_setLeftSideKerningGroup(font, glyphName, expected):
	g = font[glyphName]
	g.setLeftSideKerningGroup(expected)
	assert g.leftSideKerningGroup == expected

@pytest.mark.parametrize("glyphName, expected", [
	('seen', 'test2'), # rtl
	('Ccedilla', 'C2'), # ltr
	('E', None),
	])
def test_setRightSideKerningGroup(font, glyphName, expected):
	g = font[glyphName]
	g.setRightSideKerningGroup(expected)
	assert g.rightSideKerningGroup == expected
