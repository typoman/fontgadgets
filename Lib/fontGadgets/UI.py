# only for RF
try:
	import mojo.UI
	from mojo.roboFont import CurrentFont, CurrentGlyph
	import AppKit

	def _getCurrentSelectedGlyphNames():
		"""
		Returns the selected glyph names based on what window is active.
		"""
		cw = mojo.UI.CurrentWindow().doodleWindowName
		f = CurrentFont()
		selection = []
		if cw == 'FontWindow':
			s = f.templateSelectedGlyphNames
			for gn in s:
				selection.append(gn)
		elif cw == 'GlyphWindow':
			g = CurrentGlyph()
			if g is not None:
				selection.append(g.name)
		elif cw == 'SpaceCenter':
			s = mojo.UI.CurrentSpaceCenter().glyphLineView.getSelectedGlyphRecord()
			if s:
				selection.append(s.glyph.name)
		return selection

	mojo.UI.CurrentSelectedGlyphNames = _getCurrentSelectedGlyphNames

	def _enableDarkMode():
		dark = AppKit.NSAppearance.appearanceNamed_(AppKit.NSAppearanceNameDarkAqua)
		AppKit.NSApp().setAppearance_(dark)

	mojo.UI.enableDarkMode = _enableDarkMode

	def _limitFontViewToGlyphSet(glyph_set):
		queryText = 'Name in {"%s"}' % '", "'.join(glyph_set)
		query = AppKit.NSPredicate.predicateWithFormat_(queryText)
		mojo.UI.CurrentFontWindow().getGlyphCollection().setQuery(query)

	mojo.UI.limitFontViewToGlyphSet = _limitFontViewToGlyphSet

except ModuleNotFoundError:
	pass
