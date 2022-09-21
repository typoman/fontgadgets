from main import *


glyphs = "lamed-hb dagesh-hb holam-hb lamed_dagesh_holam-hb".split(" ")
f = RFont()
for gn in glyphs:
	f.newGlyph(gn)
f.features.text = """
feature ccmp {
lookup ccmp_hebr_1 {
	lookupflag RightToLeft;
	sub lamed-hb dagesh-hb holam-hb by lamed_dagesh_holam-hb;
} ccmp_hebr_1;
} ccmp;
"""
print(f.features.subset(tuple("lamed_dagesh_holam-hb")))
