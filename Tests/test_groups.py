from main import *

def test_glyphToKerningGroupMapping():
	result = [{'A': 'A', 'Aacute': 'A', 'Abreve': 'A', 'Acircumflex': 'A', 'Adieresis': 'A', 'Agrave': 'A', 'Amacron': 'A', 'Aogonek': 'A', 'Aring': 'A', 'Atilde': 'A', 'Abreveacute': 'A', 'Abrevedotbelow': 'A', 'Abrevegrave': 'A', 'Abrevehoi': 'A', 'Abrevetilde': 'A', 'Acircumflexacute': 'A', 'Acircumflexdotbelow': 'A', 'Acircumflexgrave': 'A', 'Acircumflexhoi': 'A', 'Acircumflextilde': 'A', 'Adotbelow': 'A', 'Ahoi': 'A', 'Aringacute': 'A', 'C': 'C', 'Cacute': 'C', 'Ccaron': 'C', 'Ccedilla': 'C', 'Ccircumflex': 'C', 'Cdotaccent': 'C', 'Cacute.pl': 'C', 'Cdotbelow': 'C', 'E': 'E', 'Eacute': 'E', 'Ebreve': 'E', 'Ecaron': 'E', 'Ecircumflex': 'E', 'Edieresis': 'E', 'Edotaccent': 'E', 'Egrave': 'E', 'Emacron': 'E', 'Eogonek': 'E', 'AE': 'E', 'OE': 'E', 'Ecircumflexacute': 'E', 'Ecircumflexdotbelow': 'E', 'Ecircumflexgrave': 'E', 'Ecircumflexhoi': 'E', 'Ecircumflextilde': 'E', 'Edotbelow': 'E', 'Ehookabove': 'E', 'Etilde': 'E', 'AEacute': 'E', 'G': 'G', 'Gbreve': 'G', 'Gcircumflex': 'G', 'Gcommaaccent': 'G', 'Gdotaccent': 'G', 'H': 'H', 'Hcircumflex': 'H', 'I': 'H', 'Iacute': 'H', 'Ibreve': 'H', 'Icircumflex': 'H', 'Idieresis': 'H', 'Idotaccent': 'H', 'Igrave': 'H', 'Imacron': 'H', 'Iogonek': 'H', 'Itilde': 'H', 'M.alt': 'H', 'N': 'H', 'Nacute': 'H', 'Ncommaaccent': 'H', 'Ntilde': 'H', 'Hbar': 'H', 'Nacute.pl': 'H', 'Eng': 'H', 'Ncaron': 'H', 'Idotbelow': 'H', 'Ihookabove': 'H', 'M': 'H', 'IJ': 'J', 'J': 'J', 'Jcircumflex': 'J', 'IJacute': 'J', 'Jacute': 'J', 'K': 'K', 'Kcommaaccent': 'K', 'L': 'L', 'Lacute': 'L', 'Lcaron': 'L', 'Lcommaaccent': 'L', 'D': 'O', 'Dcaron': 'O', 'O': 'O', 'Oacute': 'O', 'Obreve': 'O', 'Ocircumflex': 'O', 'Odieresis': 'O', 'Ograve': 'O', 'Ohungarumlaut': 'O', 'Omacron': 'O', 'Otilde': 'O', 'Eth': 'O', 'Dcroat': 'O', 'Oacute.pl': 'O', 'Oslash': 'O', 'Ocircumflexacute': 'O', 'Ocircumflexdotbelow': 'O', 'Ocircumflexgrave': 'O', 'Ocircumflexhoi': 'O', 'Ocircumflextilde': 'O', 'Odotbelow': 'O', 'Ohoi': 'O', 'Schwa': 'O', 'Oslashacute': 'O', 'Ohornacute': 'Ohorn', 'Ohorndotbelow': 'Ohorn', 'Ohorngrave': 'Ohorn', 'Ohornhoi': 'Ohorn', 'Ohorntilde': 'Ohorn', 'Ohorn': 'Ohorn', 'R': 'R', 'Racute': 'R', 'Rcaron': 'R', 'Rcommaaccent': 'R', 'S': 'S', 'Sacute': 'S', 'Sacute.pl': 'S', 'Scaron': 'S', 'Scedilla': 'S', 'Scircumflex': 'S', 'Scommaaccent': 'S', 'T': 'T', 'Tcaron': 'T', 'Tcommaaccent': 'T', 'Tbar': 'T', 'uni021A': 'T', 'U': 'U', 'Uacute': 'U', 'Ubreve': 'U', 'Ucircumflex': 'U', 'Udieresis': 'U', 'Ugrave': 'U', 'Uhungarumlaut': 'U', 'Umacron': 'U', 'Uogonek': 'U', 'Uring': 'U', 'Utilde': 'U', 'Udotbelow': 'U', 'Uhoi': 'U', 'Uhorn': 'Uhorn', 'Uhornacute': 'Uhorn', 'Uhorndotbelow': 'Uhorn', 'Uhorngrave': 'Uhorn', 'Uhornhoi': 'Uhorn', 'Uhorntilde': 'Uhorn', 'W': 'W', 'Wacute': 'W', 'Wcircumflex': 'W', 'Wdieresis': 'W', 'Wgrave': 'W', 'Y': 'Y', 'Yacute': 'Y', 'Ycircumflex': 'Y', 'Ydieresis': 'Y', 'Ygrave': 'Y', 'Ydotbelow': 'Y', 'Yhoi': 'Y', 'Ytilde': 'Y', 'Z': 'Z', 'Zacute': 'Z', 'Zcaron': 'Z', 'Zdotaccent': 'Z', 'Zacute.pl': 'Z', 'bar': 'bar', 'brokenbar': 'bar', 'bar.uc': 'bar_uc', 'brokenbar.uc': 'bar_uc', 'braceleft.uc': 'bracketlef_uc', 'bracketleft.uc': 'bracketlef_uc', 'braceleft': 'bracketleft', 'bracketleft': 'bracketleft', 'c': 'c', 'cacute': 'c', 'ccaron': 'c', 'ccedilla': 'c', 'ccircumflex': 'c', 'cdotaccent': 'c', 'cacute.pl': 'c', 'cdotbelow': 'c', 'cent.bar': 'cent', 'cent': 'cent', 'colon': 'colon', 'semicolon': 'colon', 'Pcircle': 'copyright', 'copyright': 'copyright', 'pcircle': 'copyright', 'registered': 'copyright', 'dcaron': 'dcaron', 'lcaron': 'dcaron', 'dollar': 'dollar', 'dollar.bar': 'dollar', 'oe': 'e', 'e': 'e', 'eacute': 'e', 'ebreve': 'e', 'ecaron': 'e', 'ecircumflex': 'e', 'edieresis': 'e', 'edotaccent': 'e', 'egrave': 'e', 'emacron': 'e', 'eogonek': 'e', 'ae': 'e', 'ecircumflexacute': 'e', 'ecircumflexdotbelow': 'e', 'ecircumflexgrave': 'e', 'ecircumflexhoi': 'e', 'ecircumflextilde': 'e', 'edotbelow': 'e', 'ehookabove': 'e', 'etilde': 'e', 'aeacute': 'e', 'emdash': 'endash', 'endash': 'endash', 'hyphen': 'endash', 'emdash.uc': 'endash_uc', 'endash.uc': 'endash_uc', 'hyphen.uc': 'endash_uc', 'f': 'f', 'f_f': 'f', 'f.short': 'f.short', 'f_f.short': 'f.short', 'g': 'g', 'gbreve': 'g', 'gcircumflex': 'g', 'gcommaaccent': 'g', 'gdotaccent': 'g', 'g.alt': 'g_alt', 'gbreve.alt': 'g_alt', 'gcircumflex.alt': 'g_alt', 'gcommaaccent.alt': 'g_alt', 'gdotaccent.alt': 'g_alt', 'guillemotleft': 'guillemotleft', 'guilsinglleft': 'guillemotleft', 'guilsinglleft.uc': 'guillemotleft_uc', 'guillemotleft.uc': 'guillemotleft_uc', 'guillemotright': 'guillemotright', 'guilsinglright': 'guillemotright', 'guillemotright.uc': 'guillemotright_uc', 'guilsinglright.uc': 'guillemotright_uc', 'i': 'i', 'iacute': 'i', 'ibreve': 'i', 'icircumflex': 'i', 'idieresis': 'i', 'igrave': 'i', 'imacron': 'i', 'iogonek': 'i', 'itilde': 'i', 'dotlessi': 'i', 'f_i': 'i', 'idotbelow': 'i', 'ihookabove': 'i', 'idotaccent': 'i', 'fi': 'i', 'j': 'j', 'jcircumflex': 'j', 'eng': 'j', 'ij': 'j', 'dotlessj': 'j', 'q': 'j', 'ijacute': 'j', 'jacute': 'j', 'k': 'k', 'kcommaaccent': 'k', 'l': 'l', 'lacute': 'l', 'lcommaaccent': 'l', 'd': 'l', 'dcroat': 'l', 'f_l': 'l', 'fl': 'l', 'minute': 'minute', 'second': 'minute', 'n': 'n', 'a': 'n', 'aacute': 'n', 'abreve': 'n', 'acircumflex': 'n', 'adieresis': 'n', 'agrave': 'n', 'amacron': 'n', 'aogonek': 'n', 'aring': 'n', 'atilde': 'n', 'h': 'n', 'hcircumflex': 'n', 'm': 'n', 'nacute': 'n', 'ncaron': 'n', 'ncommaaccent': 'n', 'ntilde': 'n', 'nacute.pl': 'n', 'hbar': 'n', 'abreveacute': 'n', 'abrevedotbelow': 'n', 'abrevegrave': 'n', 'abrevehoi': 'n', 'abrevetilde': 'n', 'acircumflexacute': 'n', 'acircumflexdotbelow': 'n', 'acircumflexgrave': 'n', 'acircumflexhoi': 'n', 'acircumflextilde': 'n', 'adotbelow': 'n', 'ahoi': 'n', 'aringacute': 'n', 'oacute.pl': 'o', 'oslash': 'o', 'o': 'o', 'oacute': 'o', 'obreve': 'o', 'ocircumflex': 'o', 'odieresis': 'o', 'ograve': 'o', 'ohungarumlaut': 'o', 'omacron': 'o', 'otilde': 'o', 'b': 'o', 'p': 'o', 'thorn': 'o', 'ocircumflexacute': 'o', 'ocircumflexdotbelow': 'o', 'ocircumflexgrave': 'o', 'ocircumflexhoi': 'o', 'ocircumflextilde': 'o', 'odotbelow': 'o', 'ohoi': 'o', 'schwa': 'o', 'oslashacute': 'o', 'ohorn': 'ohorn', 'ohornacute': 'ohorn', 'ohorndotbelow': 'ohorn', 'ohorngrave': 'ohorn', 'ohornhoi': 'ohorn', 'ohorntilde': 'ohorn', 'comma': 'period', 'period': 'period', 'ellipsis': 'period', 'divide': 'plus', 'minus': 'plus', 'plus': 'plus', 'quotedblbase': 'quotebase', 'quotesinglbase': 'quotebase', 'quotedblleft': 'quoteleft', 'quoteleft': 'quoteleft', 'quotedblright': 'quoteright', 'quoteright': 'quoteright', 'quotedbl': 'quotesingle', 'quotesingle': 'quotesingle', 'r': 'r', 'racute': 'r', 'rcaron': 'r', 'rcommaaccent': 'r', 'sacute.pl': 's', 's': 's', 'sacute': 's', 'scaron': 's', 'scedilla': 's', 'scircumflex': 's', 'scommaaccent': 's', 't': 't', 'tcaron': 't', 'tcommaaccent': 't', 'tbar': 't', 'uni021B': 't', 'u': 'u', 'uacute': 'u', 'ubreve': 'u', 'ucircumflex': 'u', 'udieresis': 'u', 'ugrave': 'u', 'uhungarumlaut': 'u', 'umacron': 'u', 'uogonek': 'u', 'uring': 'u', 'utilde': 'u', 'udotbelow': 'u', 'uhoi': 'u', 'uhorn': 'uhorn', 'uhornacute': 'uhorn', 'uhorndotbelow': 'uhorn', 'uhorngrave': 'uhorn', 'uhornhoi': 'uhorn', 'uhorntilde': 'uhorn', 'w': 'w', 'wacute': 'w', 'wcircumflex': 'w', 'wdieresis': 'w', 'wgrave': 'w', 'y': 'y', 'yacute': 'y', 'ycircumflex': 'y', 'ydieresis': 'y', 'ygrave': 'y', 'v': 'y', 'ydotbelow': 'y', 'yhoi': 'y', 'ytilde': 'y', 'z': 'z', 'zacute': 'z', 'zcaron': 'z', 'zdotaccent': 'z', 'zacute.pl': 'z'}, {'A': 'A', 'Aacute': 'A', 'Abreve': 'A', 'Acircumflex': 'A', 'Adieresis': 'A', 'Agrave': 'A', 'Amacron': 'A', 'Aogonek': 'A', 'Aring': 'A', 'Atilde': 'A', 'Abreveacute': 'A', 'Abrevedotbelow': 'A', 'Abrevegrave': 'A', 'Abrevehoi': 'A', 'Abrevetilde': 'A', 'Acircumflexacute': 'A', 'Acircumflexdotbelow': 'A', 'Acircumflexgrave': 'A', 'Acircumflexhoi': 'A', 'Acircumflextilde': 'A', 'Adotbelow': 'A', 'Ahoi': 'A', 'AE': 'AE', 'AEacute': 'AE', 'Dcroat': 'Eth', 'Eth': 'Eth', 'B': 'H', 'D': 'H', 'Dcaron': 'H', 'E': 'H', 'Eacute': 'H', 'Ebreve': 'H', 'Ecaron': 'H', 'Ecircumflex': 'H', 'Edieresis': 'H', 'Edotaccent': 'H', 'Egrave': 'H', 'Emacron': 'H', 'Eng': 'H', 'Eogonek': 'H', 'F': 'H', 'H': 'H', 'Hbar': 'H', 'Hcircumflex': 'H', 'I': 'H', 'IJ': 'H', 'Iacute': 'H', 'Ibreve': 'H', 'Icircumflex': 'H', 'Idieresis': 'H', 'Idotaccent': 'H', 'Igrave': 'H', 'Imacron': 'H', 'Iogonek': 'H', 'Itilde': 'H', 'K': 'H', 'Kcommaaccent': 'H', 'L': 'H', 'Lacute': 'H', 'Lcaron': 'H', 'Lcommaaccent': 'H', 'Ldot': 'H', 'M.alt': 'H', 'N': 'H', 'Nacute': 'H', 'Nacute.pl': 'H', 'Ncaron': 'H', 'Ncommaaccent': 'H', 'Ntilde': 'H', 'R': 'H', 'Racute': 'H', 'Rcaron': 'H', 'Rcommaaccent': 'H', 'P': 'H', 'Thorn': 'H', 'Ecircumflexacute': 'H', 'Ecircumflexdotbelow': 'H', 'Ecircumflexgrave': 'H', 'Ecircumflexhoi': 'H', 'Ecircumflextilde': 'H', 'Edotbelow': 'H', 'Ehookabove': 'H', 'Etilde': 'H', 'Idotbelow': 'H', 'Ihookabove': 'H', 'IJacute': 'H', 'M': 'H', 'J': 'J', 'Jcircumflex': 'J', 'Jacute': 'J', 'C': 'O', 'Cacute': 'O', 'Ccaron': 'O', 'Ccedilla': 'O', 'Ccircumflex': 'O', 'Cdotaccent': 'O', 'G': 'O', 'Gbreve': 'O', 'Gcircumflex': 'O', 'Gcommaaccent': 'O', 'Gdotaccent': 'O', 'O': 'O', 'Oacute': 'O', 'Obreve': 'O', 'Ocircumflex': 'O', 'Odieresis': 'O', 'Ograve': 'O', 'Ohungarumlaut': 'O', 'Omacron': 'O', 'Otilde': 'O', 'Q': 'O', 'Oslash': 'O', 'OE': 'O', 'Oacute.pl': 'O', 'Cacute.pl': 'O', 'Ocircumflexacute': 'O', 'Ocircumflexdotbelow': 'O', 'Ocircumflexgrave': 'O', 'Ocircumflexhoi': 'O', 'Ocircumflextilde': 'O', 'Odotbelow': 'O', 'Ohoi': 'O', 'Ohorn': 'O', 'Ohornacute': 'O', 'Ohorndotbelow': 'O', 'Ohorngrave': 'O', 'Ohornhoi': 'O', 'Ohorntilde': 'O', 'Cdotbelow': 'O', 'Oslashacute': 'O', 'S': 'S', 'Sacute': 'S', 'Scaron': 'S', 'Scedilla': 'S', 'Scircumflex': 'S', 'Scommaaccent': 'S', 'Sacute.pl': 'S', 'T': 'T', 'Tcaron': 'T', 'Tcommaaccent': 'T', 'Tbar': 'T', 'uni021A': 'T', 'U': 'U', 'Uacute': 'U', 'Ubreve': 'U', 'Ucircumflex': 'U', 'Udieresis': 'U', 'Ugrave': 'U', 'Uhungarumlaut': 'U', 'Umacron': 'U', 'Uogonek': 'U', 'Uring': 'U', 'Utilde': 'U', 'Udotbelow': 'U', 'Uhoi': 'U', 'Uhorn': 'U', 'Uhornacute': 'U', 'Uhorndotbelow': 'U', 'Uhorngrave': 'U', 'Uhornhoi': 'U', 'Uhorntilde': 'U', 'W': 'W', 'Wacute': 'W', 'Wcircumflex': 'W', 'Wdieresis': 'W', 'Wgrave': 'W', 'Y': 'Y', 'Yacute': 'Y', 'Ycircumflex': 'Y', 'Ydieresis': 'Y', 'Ygrave': 'Y', 'Ydotbelow': 'Y', 'Yhoi': 'Y', 'Ytilde': 'Y', 'Z': 'Z', 'Zacute': 'Z', 'Zacute.pl': 'Z', 'Zcaron': 'Z', 'Zdotaccent': 'Z', 'ae': 'a', 'a': 'a', 'aacute': 'a', 'abreve': 'a', 'acircumflex': 'a', 'adieresis': 'a', 'agrave': 'a', 'amacron': 'a', 'aogonek': 'a', 'aring': 'a', 'atilde': 'a', 'abreveacute': 'a', 'abrevedotbelow': 'a', 'abrevegrave': 'a', 'abrevehoi': 'a', 'abrevetilde': 'a', 'acircumflexacute': 'a', 'acircumflexdotbelow': 'a', 'acircumflexgrave': 'a', 'acircumflexhoi': 'a', 'acircumflextilde': 'a', 'adotbelow': 'a', 'ahoi': 'a', 'aeacute': 'a', 'aringacute': 'a', 'bar': 'bar', 'brokenbar': 'bar', 'bar.uc': 'bar_uc', 'brokenbar.uc': 'bar_uc', 'braceright': 'bracketright', 'bracketright': 'bracketright', 'braceright.uc': 'bracketright_uc', 'bracketright.uc': 'bracketright_uc', 'cent': 'cent', 'cent.bar': 'cent', 'colon': 'colon', 'semicolon': 'colon', 'Pcircle': 'copyright', 'copyright': 'copyright', 'pcircle': 'copyright', 'registered': 'copyright', 'dollar.bar': 'dollar', 'dollar': 'dollar', 'emdash': 'endash', 'endash': 'endash', 'hyphen': 'endash', 'emdash.uc': 'endash_uc', 'endash.uc': 'endash_uc', 'hyphen.uc': 'endash_uc', 'f': 'f', 'f_i': 'f', 'f_l': 'f', 'f.short': 'f', 'f_f': 'f', 'f_f.short': 'f', 'fi': 'f', 'fl': 'f', 'g': 'g', 'gbreve': 'g', 'gcircumflex': 'g', 'gcommaaccent': 'g', 'gdotaccent': 'g', 'g.alt': 'g_alt', 'gbreve.alt': 'g_alt', 'gcircumflex.alt': 'g_alt', 'gcommaaccent.alt': 'g_alt', 'gdotaccent.alt': 'g_alt', 'guillemotleft': 'guillemotleft', 'guilsinglleft': 'guillemotleft', 'guillemotleft.uc': 'guillemotleft_uc', 'guilsinglleft.uc': 'guillemotleft_uc', 'guillemotright': 'guillemotright', 'guilsinglright': 'guillemotright', 'guilsinglright.uc': 'guillemotright_uc', 'guillemotright.uc': 'guillemotright_uc', 'dotlessi': 'i', 'i': 'i', 'iacute': 'i', 'ibreve': 'i', 'icircumflex': 'i', 'idieresis': 'i', 'igrave': 'i', 'imacron': 'i', 'iogonek': 'i', 'itilde': 'i', 'ij': 'i', 'idotbelow': 'i', 'ihookabove': 'i', 'idotaccent': 'i', 'ijacute': 'i', 'j': 'j', 'jcircumflex': 'j', 'dotlessj': 'j', 'jacute': 'j', 'b': 'l', 'h': 'l', 'hcircumflex': 'l', 'k': 'l', 'kcommaaccent': 'l', 'l': 'l', 'lacute': 'l', 'lcaron': 'l', 'lcommaaccent': 'l', 'ldot': 'l', 'minute': 'minute', 'second': 'minute', 'm': 'n', 'n': 'n', 'nacute': 'n', 'ncaron': 'n', 'ncommaaccent': 'n', 'ntilde': 'n', 'r': 'n', 'racute': 'n', 'rcaron': 'n', 'rcommaaccent': 'n', 'eng': 'n', 'nacute.pl': 'n', 'cacute.pl': 'o', 'oacute.pl': 'o', 'dcroat': 'o', 'oe': 'o', 'o': 'o', 'oacute': 'o', 'obreve': 'o', 'ocircumflex': 'o', 'odieresis': 'o', 'ograve': 'o', 'ohungarumlaut': 'o', 'omacron': 'o', 'otilde': 'o', 'q': 'o', 'd': 'o', 'dcaron': 'o', 'e': 'o', 'eacute': 'o', 'ebreve': 'o', 'ecaron': 'o', 'ecircumflex': 'o', 'edieresis': 'o', 'edotaccent': 'o', 'egrave': 'o', 'emacron': 'o', 'eogonek': 'o', 'oslash': 'o', 'c': 'o', 'cacute': 'o', 'ccaron': 'o', 'ccedilla': 'o', 'ccircumflex': 'o', 'cdotaccent': 'o', 'ecircumflexacute': 'o', 'ecircumflexdotbelow': 'o', 'ecircumflexgrave': 'o', 'ecircumflexhoi': 'o', 'ecircumflextilde': 'o', 'edotbelow': 'o', 'ehookabove': 'o', 'etilde': 'o', 'ocircumflexacute': 'o', 'ocircumflexdotbelow': 'o', 'ocircumflexgrave': 'o', 'ocircumflexhoi': 'o', 'ocircumflextilde': 'o', 'odotbelow': 'o', 'ohoi': 'o', 'ohorn': 'o', 'ohornacute': 'o', 'ohorndotbelow': 'o', 'ohorngrave': 'o', 'ohornhoi': 'o', 'ohorntilde': 'o', 'cdotbelow': 'o', 'oslashacute': 'o', 'percent': 'percent', 'perthousand': 'percent', 'comma': 'period', 'period': 'period', 'ellipsis': 'period', 'divide': 'plus', 'minus': 'plus', 'plus': 'plus', 'quotedblbase': 'quotebase', 'quotesinglbase': 'quotebase', 'quotedblleft': 'quoteleft', 'quoteleft': 'quoteleft', 'quotedblright': 'quoteright', 'quoteright': 'quoteright', 'quotedbl': 'quotesingle', 'quotesingle': 'quotesingle', 's': 's', 'sacute': 's', 'scaron': 's', 'scedilla': 's', 'scircumflex': 's', 'scommaaccent': 's', 'sacute.pl': 's', 't': 't', 'tcaron': 't', 'tcommaaccent': 't', 'tbar': 't', 'uni021B': 't', 'u': 'u', 'uacute': 'u', 'ubreve': 'u', 'ucircumflex': 'u', 'udieresis': 'u', 'ugrave': 'u', 'uhungarumlaut': 'u', 'umacron': 'u', 'uogonek': 'u', 'uring': 'u', 'utilde': 'u', 'udotbelow': 'u', 'uhoi': 'u', 'uhorn': 'u', 'uhornacute': 'u', 'uhorndotbelow': 'u', 'uhorngrave': 'u', 'uhornhoi': 'u', 'uhorntilde': 'u', 'w': 'w', 'wacute': 'w', 'wcircumflex': 'w', 'wdieresis': 'w', 'wgrave': 'w', 'y': 'y', 'yacute': 'y', 'ycircumflex': 'y', 'ydieresis': 'y', 'ygrave': 'y', 'ydotbelow': 'y', 'yhoi': 'y', 'ytilde': 'y', 'zacute.pl': 'z', 'z': 'z', 'zacute': 'z', 'zcaron': 'z', 'zdotaccent': 'z'}]
	assert testFont1.glyphToKerningGroupMapping == result

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


