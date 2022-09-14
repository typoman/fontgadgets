from main import *

def test_glyphToKerningGroupMapping():
	result = [{'A': 'A', 'Aacute': 'A', 'Abreve': 'A', 'Acircumflex': 'A', 'Adieresis': 'A', 'Agrave': 'A', 'Amacron': 'A', 'Aogonek': 'A', 'Aring': 'A', 'Atilde': 'A', 'Abreveacute': 'A', 'Abrevedotbelow': 'A', 'Abrevegrave': 'A', 'Abrevehoi': 'A', 'Abrevetilde': 'A', 'Acircumflexacute': 'A', 'Acircumflexdotbelow': 'A', 'Acircumflexgrave': 'A', 'Acircumflexhoi': 'A', 'Acircumflextilde': 'A', 'Adotbelow': 'A', 'Ahoi': 'A', 'Aringacute': 'A', 'C': 'C', 'Cacute': 'C', 'Ccaron': 'C', 'Ccedilla': 'C', 'Ccircumflex': 'C', 'Cdotaccent': 'C', 'Cacute.pl': 'C', 'Cdotbelow': 'C', 'E': 'E', 'Eacute': 'E', 'Ebreve': 'E', 'Ecaron': 'E', 'Ecircumflex': 'E', 'Edieresis': 'E', 'Edotaccent': 'E', 'Egrave': 'E', 'Emacron': 'E', 'Eogonek': 'E', 'AE': 'E', 'OE': 'E', 'Ecircumflexacute': 'E', 'Ecircumflexdotbelow': 'E', 'Ecircumflexgrave': 'E', 'Ecircumflexhoi': 'E', 'Ecircumflextilde': 'E', 'Edotbelow': 'E', 'Ehookabove': 'E', 'Etilde': 'E', 'AEacute': 'E', 'G': 'G', 'Gbreve': 'G', 'Gcircumflex': 'G', 'Gcommaaccent': 'G', 'Gdotaccent': 'G', 'H': 'H', 'Hcircumflex': 'H', 'I': 'H', 'Iacute': 'H', 'Ibreve': 'H', 'Icircumflex': 'H', 'Idieresis': 'H', 'Idotaccent': 'H', 'Igrave': 'H', 'Imacron': 'H', 'Iogonek': 'H', 'Itilde': 'H', 'M.alt': 'H', 'N': 'H', 'Nacute': 'H', 'Ncommaaccent': 'H', 'Ntilde': 'H', 'Hbar': 'H', 'Nacute.pl': 'H', 'Eng': 'H', 'Ncaron': 'H', 'Idotbelow': 'H', 'Ihookabove': 'H', 'M': 'H', 'IJ': 'J', 'J': 'J', 'Jcircumflex': 'J', 'IJacute': 'J', 'Jacute': 'J', 'K': 'K', 'Kcommaaccent': 'K', 'L': 'L', 'Lacute': 'L', 'Lcaron': 'L', 'Lcommaaccent': 'L', 'D': 'O', 'Dcaron': 'O', 'O': 'O', 'Oacute': 'O', 'Obreve': 'O', 'Ocircumflex': 'O', 'Odieresis': 'O', 'Ograve': 'O', 'Ohungarumlaut': 'O', 'Omacron': 'O', 'Otilde': 'O', 'Eth': 'O', 'Dcroat': 'O', 'Oacute.pl': 'O', 'Oslash': 'O', 'Ocircumflexacute': 'O', 'Ocircumflexdotbelow': 'O', 'Ocircumflexgrave': 'O', 'Ocircumflexhoi': 'O', 'Ocircumflextilde': 'O', 'Odotbelow': 'O', 'Ohoi': 'O', 'Schwa': 'O', 'Oslashacute': 'O', 'Ohornacute': 'Ohorn', 'Ohorndotbelow': 'Ohorn', 'Ohorngrave': 'Ohorn', 'Ohornhoi': 'Ohorn', 'Ohorntilde': 'Ohorn', 'Ohorn': 'Ohorn', 'R': 'R', 'Racute': 'R', 'Rcaron': 'R', 'Rcommaaccent': 'R', 'S': 'S', 'Sacute': 'S', 'Sacute.pl': 'S', 'Scaron': 'S', 'Scedilla': 'S', 'Scircumflex': 'S', 'Scommaaccent': 'S', 'T': 'T', 'Tcaron': 'T', 'Tcommaaccent': 'T', 'Tbar': 'T', 'uni021A': 'T', 'U': 'U', 'Uacute': 'U', 'Ubreve': 'U', 'Ucircumflex': 'U', 'Udieresis': 'U', 'Ugrave': 'U', 'Uhungarumlaut': 'U', 'Umacron': 'U', 'Uogonek': 'U', 'Uring': 'U', 'Utilde': 'U', 'Udotbelow': 'U', 'Uhoi': 'U', 'Uhorn': 'Uhorn', 'Uhornacute': 'Uhorn', 'Uhorndotbelow': 'Uhorn', 'Uhorngrave': 'Uhorn', 'Uhornhoi': 'Uhorn', 'Uhorntilde': 'Uhorn', 'W': 'W', 'Wacute': 'W', 'Wcircumflex': 'W', 'Wdieresis': 'W', 'Wgrave': 'W', 'Y': 'Y', 'Yacute': 'Y', 'Ycircumflex': 'Y', 'Ydieresis': 'Y', 'Ygrave': 'Y', 'Ydotbelow': 'Y', 'Yhoi': 'Y', 'Ytilde': 'Y', 'Z': 'Z', 'Zacute': 'Z', 'Zcaron': 'Z', 'Zdotaccent': 'Z', 'Zacute.pl': 'Z', 'bar': 'bar', 'brokenbar': 'bar', 'bar.uc': 'bar_uc', 'brokenbar.uc': 'bar_uc', 'braceleft.uc': 'bracketlef_uc', 'bracketleft.uc': 'bracketlef_uc', 'braceleft': 'bracketleft', 'bracketleft': 'bracketleft', 'c': 'c', 'cacute': 'c', 'ccaron': 'c', 'ccedilla': 'c', 'ccircumflex': 'c', 'cdotaccent': 'c', 'cacute.pl': 'c', 'cdotbelow': 'c', 'cent.bar': 'cent', 'cent': 'cent', 'colon': 'colon', 'semicolon': 'colon', 'Pcircle': 'copyright', 'copyright': 'copyright', 'pcircle': 'copyright', 'registered': 'copyright', 'dcaron': 'dcaron', 'lcaron': 'dcaron', 'dollar': 'dollar', 'dollar.bar': 'dollar', 'oe': 'e', 'e': 'e', 'eacute': 'e', 'ebreve': 'e', 'ecaron': 'e', 'ecircumflex': 'e', 'edieresis': 'e', 'edotaccent': 'e', 'egrave': 'e', 'emacron': 'e', 'eogonek': 'e', 'ae': 'e', 'ecircumflexacute': 'e', 'ecircumflexdotbelow': 'e', 'ecircumflexgrave': 'e', 'ecircumflexhoi': 'e', 'ecircumflextilde': 'e', 'edotbelow': 'e', 'ehookabove': 'e', 'etilde': 'e', 'aeacute': 'e', 'emdash': 'endash', 'endash': 'endash', 'hyphen': 'endash', 'emdash.uc': 'endash_uc', 'endash.uc': 'endash_uc', 'hyphen.uc': 'endash_uc', 'f': 'f', 'f_f': 'f', 'f.short': 'f.short', 'f_f.short': 'f.short', 'g': 'g', 'gbreve': 'g', 'gcircumflex': 'g', 'gcommaaccent': 'g', 'gdotaccent': 'g', 'g.alt': 'g_alt', 'gbreve.alt': 'g_alt', 'gcircumflex.alt': 'g_alt', 'gcommaaccent.alt': 'g_alt', 'gdotaccent.alt': 'g_alt', 'guillemotleft': 'guillemotleft', 'guilsinglleft': 'guillemotleft', 'guilsinglleft.uc': 'guillemotleft_uc', 'guillemotleft.uc': 'guillemotleft_uc', 'guillemotright': 'guillemotright', 'guilsinglright': 'guillemotright', 'guillemotright.uc': 'guillemotright_uc', 'guilsinglright.uc': 'guillemotright_uc', 'i': 'i', 'iacute': 'i', 'ibreve': 'i', 'icircumflex': 'i', 'idieresis': 'i', 'igrave': 'i', 'imacron': 'i', 'iogonek': 'i', 'itilde': 'i', 'dotlessi': 'i', 'f_i': 'i', 'idotbelow': 'i', 'ihookabove': 'i', 'idotaccent': 'i', 'fi': 'i', 'j': 'j', 'jcircumflex': 'j', 'eng': 'j', 'ij': 'j', 'dotlessj': 'j', 'q': 'j', 'ijacute': 'j', 'jacute': 'j', 'k': 'k', 'kcommaaccent': 'k', 'l': 'l', 'lacute': 'l', 'lcommaaccent': 'l', 'd': 'l', 'dcroat': 'l', 'f_l': 'l', 'fl': 'l', 'minute': 'minute', 'second': 'minute', 'n': 'n', 'a': 'n', 'aacute': 'n', 'abreve': 'n', 'acircumflex': 'n', 'adieresis': 'n', 'agrave': 'n', 'amacron': 'n', 'aogonek': 'n', 'aring': 'n', 'atilde': 'n', 'h': 'n', 'hcircumflex': 'n', 'm': 'n', 'nacute': 'n', 'ncaron': 'n', 'ncommaaccent': 'n', 'ntilde': 'n', 'nacute.pl': 'n', 'hbar': 'n', 'abreveacute': 'n', 'abrevedotbelow': 'n', 'abrevegrave': 'n', 'abrevehoi': 'n', 'abrevetilde': 'n', 'acircumflexacute': 'n', 'acircumflexdotbelow': 'n', 'acircumflexgrave': 'n', 'acircumflexhoi': 'n', 'acircumflextilde': 'n', 'adotbelow': 'n', 'ahoi': 'n', 'aringacute': 'n', 'oacute.pl': 'o', 'oslash': 'o', 'o': 'o', 'oacute': 'o', 'obreve': 'o', 'ocircumflex': 'o', 'odieresis': 'o', 'ograve': 'o', 'ohungarumlaut': 'o', 'omacron': 'o', 'otilde': 'o', 'b': 'o', 'p': 'o', 'thorn': 'o', 'ocircumflexacute': 'o', 'ocircumflexdotbelow': 'o', 'ocircumflexgrave': 'o', 'ocircumflexhoi': 'o', 'ocircumflextilde': 'o', 'odotbelow': 'o', 'ohoi': 'o', 'schwa': 'o', 'oslashacute': 'o', 'ohorn': 'ohorn', 'ohornacute': 'ohorn', 'ohorndotbelow': 'ohorn', 'ohorngrave': 'ohorn', 'ohornhoi': 'ohorn', 'ohorntilde': 'ohorn', 'comma': 'period', 'period': 'period', 'ellipsis': 'period', 'divide': 'plus', 'minus': 'plus', 'plus': 'plus', 'quotedblbase': 'quotebase', 'quotesinglbase': 'quotebase', 'quotedblleft': 'quoteleft', 'quoteleft': 'quoteleft', 'quotedblright': 'quoteright', 'quoteright': 'quoteright', 'quotedbl': 'quotesingle', 'quotesingle': 'quotesingle', 'r': 'r', 'racute': 'r', 'rcaron': 'r', 'rcommaaccent': 'r', 'sacute.pl': 's', 's': 's', 'sacute': 's', 'scaron': 's', 'scedilla': 's', 'scircumflex': 's', 'scommaaccent': 's', 't': 't', 'tcaron': 't', 'tcommaaccent': 't', 'tbar': 't', 'uni021B': 't', 'u': 'u', 'uacute': 'u', 'ubreve': 'u', 'ucircumflex': 'u', 'udieresis': 'u', 'ugrave': 'u', 'uhungarumlaut': 'u', 'umacron': 'u', 'uogonek': 'u', 'uring': 'u', 'utilde': 'u', 'udotbelow': 'u', 'uhoi': 'u', 'uhorn': 'uhorn', 'uhornacute': 'uhorn', 'uhorndotbelow': 'uhorn', 'uhorngrave': 'uhorn', 'uhornhoi': 'uhorn', 'uhorntilde': 'uhorn', 'w': 'w', 'wacute': 'w', 'wcircumflex': 'w', 'wdieresis': 'w', 'wgrave': 'w', 'y': 'y', 'yacute': 'y', 'ycircumflex': 'y', 'ydieresis': 'y', 'ygrave': 'y', 'v': 'y', 'ydotbelow': 'y', 'yhoi': 'y', 'ytilde': 'y', 'z': 'z', 'zacute': 'z', 'zcaron': 'z', 'zdotaccent': 'z', 'zacute.pl': 'z'}, {'A': 'A', 'Aacute': 'A', 'Abreve': 'A', 'Acircumflex': 'A', 'Adieresis': 'A', 'Agrave': 'A', 'Amacron': 'A', 'Aogonek': 'A', 'Aring': 'A', 'Atilde': 'A', 'Abreveacute': 'A', 'Abrevedotbelow': 'A', 'Abrevegrave': 'A', 'Abrevehoi': 'A', 'Abrevetilde': 'A', 'Acircumflexacute': 'A', 'Acircumflexdotbelow': 'A', 'Acircumflexgrave': 'A', 'Acircumflexhoi': 'A', 'Acircumflextilde': 'A', 'Adotbelow': 'A', 'Ahoi': 'A', 'AE': 'AE', 'AEacute': 'AE', 'Dcroat': 'Eth', 'Eth': 'Eth', 'B': 'H', 'D': 'H', 'Dcaron': 'H', 'E': 'H', 'Eacute': 'H', 'Ebreve': 'H', 'Ecaron': 'H', 'Ecircumflex': 'H', 'Edieresis': 'H', 'Edotaccent': 'H', 'Egrave': 'H', 'Emacron': 'H', 'Eng': 'H', 'Eogonek': 'H', 'F': 'H', 'H': 'H', 'Hbar': 'H', 'Hcircumflex': 'H', 'I': 'H', 'IJ': 'H', 'Iacute': 'H', 'Ibreve': 'H', 'Icircumflex': 'H', 'Idieresis': 'H', 'Idotaccent': 'H', 'Igrave': 'H', 'Imacron': 'H', 'Iogonek': 'H', 'Itilde': 'H', 'K': 'H', 'Kcommaaccent': 'H', 'L': 'H', 'Lacute': 'H', 'Lcaron': 'H', 'Lcommaaccent': 'H', 'Ldot': 'H', 'M.alt': 'H', 'N': 'H', 'Nacute': 'H', 'Nacute.pl': 'H', 'Ncaron': 'H', 'Ncommaaccent': 'H', 'Ntilde': 'H', 'R': 'H', 'Racute': 'H', 'Rcaron': 'H', 'Rcommaaccent': 'H', 'P': 'H', 'Thorn': 'H', 'Ecircumflexacute': 'H', 'Ecircumflexdotbelow': 'H', 'Ecircumflexgrave': 'H', 'Ecircumflexhoi': 'H', 'Ecircumflextilde': 'H', 'Edotbelow': 'H', 'Ehookabove': 'H', 'Etilde': 'H', 'Idotbelow': 'H', 'Ihookabove': 'H', 'IJacute': 'H', 'M': 'H', 'J': 'J', 'Jcircumflex': 'J', 'Jacute': 'J', 'C': 'O', 'Cacute': 'O', 'Ccaron': 'O', 'Ccedilla': 'O', 'Ccircumflex': 'O', 'Cdotaccent': 'O', 'G': 'O', 'Gbreve': 'O', 'Gcircumflex': 'O', 'Gcommaaccent': 'O', 'Gdotaccent': 'O', 'O': 'O', 'Oacute': 'O', 'Obreve': 'O', 'Ocircumflex': 'O', 'Odieresis': 'O', 'Ograve': 'O', 'Ohungarumlaut': 'O', 'Omacron': 'O', 'Otilde': 'O', 'Q': 'O', 'Oslash': 'O', 'OE': 'O', 'Oacute.pl': 'O', 'Cacute.pl': 'O', 'Ocircumflexacute': 'O', 'Ocircumflexdotbelow': 'O', 'Ocircumflexgrave': 'O', 'Ocircumflexhoi': 'O', 'Ocircumflextilde': 'O', 'Odotbelow': 'O', 'Ohoi': 'O', 'Ohorn': 'O', 'Ohornacute': 'O', 'Ohorndotbelow': 'O', 'Ohorngrave': 'O', 'Ohornhoi': 'O', 'Ohorntilde': 'O', 'Cdotbelow': 'O', 'Oslashacute': 'O', 'S': 'S', 'Sacute': 'S', 'Scaron': 'S', 'Scedilla': 'S', 'Scircumflex': 'S', 'Scommaaccent': 'S', 'Sacute.pl': 'S', 'T': 'T', 'Tcaron': 'T', 'Tcommaaccent': 'T', 'Tbar': 'T', 'uni021A': 'T', 'U': 'U', 'Uacute': 'U', 'Ubreve': 'U', 'Ucircumflex': 'U', 'Udieresis': 'U', 'Ugrave': 'U', 'Uhungarumlaut': 'U', 'Umacron': 'U', 'Uogonek': 'U', 'Uring': 'U', 'Utilde': 'U', 'Udotbelow': 'U', 'Uhoi': 'U', 'Uhorn': 'U', 'Uhornacute': 'U', 'Uhorndotbelow': 'U', 'Uhorngrave': 'U', 'Uhornhoi': 'U', 'Uhorntilde': 'U', 'W': 'W', 'Wacute': 'W', 'Wcircumflex': 'W', 'Wdieresis': 'W', 'Wgrave': 'W', 'Y': 'Y', 'Yacute': 'Y', 'Ycircumflex': 'Y', 'Ydieresis': 'Y', 'Ygrave': 'Y', 'Ydotbelow': 'Y', 'Yhoi': 'Y', 'Ytilde': 'Y', 'Z': 'Z', 'Zacute': 'Z', 'Zacute.pl': 'Z', 'Zcaron': 'Z', 'Zdotaccent': 'Z', 'ae': 'a', 'a': 'a', 'aacute': 'a', 'abreve': 'a', 'acircumflex': 'a', 'adieresis': 'a', 'agrave': 'a', 'amacron': 'a', 'aogonek': 'a', 'aring': 'a', 'atilde': 'a', 'abreveacute': 'a', 'abrevedotbelow': 'a', 'abrevegrave': 'a', 'abrevehoi': 'a', 'abrevetilde': 'a', 'acircumflexacute': 'a', 'acircumflexdotbelow': 'a', 'acircumflexgrave': 'a', 'acircumflexhoi': 'a', 'acircumflextilde': 'a', 'adotbelow': 'a', 'ahoi': 'a', 'aeacute': 'a', 'aringacute': 'a', 'bar': 'bar', 'brokenbar': 'bar', 'bar.uc': 'bar_uc', 'brokenbar.uc': 'bar_uc', 'braceright': 'bracketright', 'bracketright': 'bracketright', 'braceright.uc': 'bracketright_uc', 'bracketright.uc': 'bracketright_uc', 'cent': 'cent', 'cent.bar': 'cent', 'colon': 'colon', 'semicolon': 'colon', 'Pcircle': 'copyright', 'copyright': 'copyright', 'pcircle': 'copyright', 'registered': 'copyright', 'dollar.bar': 'dollar', 'dollar': 'dollar', 'emdash': 'endash', 'endash': 'endash', 'hyphen': 'endash', 'emdash.uc': 'endash_uc', 'endash.uc': 'endash_uc', 'hyphen.uc': 'endash_uc', 'f': 'f', 'f_i': 'f', 'f_l': 'f', 'f.short': 'f', 'f_f': 'f', 'f_f.short': 'f', 'fi': 'f', 'fl': 'f', 'g': 'g', 'gbreve': 'g', 'gcircumflex': 'g', 'gcommaaccent': 'g', 'gdotaccent': 'g', 'g.alt': 'g_alt', 'gbreve.alt': 'g_alt', 'gcircumflex.alt': 'g_alt', 'gcommaaccent.alt': 'g_alt', 'gdotaccent.alt': 'g_alt', 'guillemotleft': 'guillemotleft', 'guilsinglleft': 'guillemotleft', 'guillemotleft.uc': 'guillemotleft_uc', 'guilsinglleft.uc': 'guillemotleft_uc', 'guillemotright': 'guillemotright', 'guilsinglright': 'guillemotright', 'guilsinglright.uc': 'guillemotright_uc', 'guillemotright.uc': 'guillemotright_uc', 'dotlessi': 'i', 'i': 'i', 'iacute': 'i', 'ibreve': 'i', 'icircumflex': 'i', 'idieresis': 'i', 'igrave': 'i', 'imacron': 'i', 'iogonek': 'i', 'itilde': 'i', 'ij': 'i', 'idotbelow': 'i', 'ihookabove': 'i', 'idotaccent': 'i', 'ijacute': 'i', 'j': 'j', 'jcircumflex': 'j', 'dotlessj': 'j', 'jacute': 'j', 'b': 'l', 'h': 'l', 'hcircumflex': 'l', 'k': 'l', 'kcommaaccent': 'l', 'l': 'l', 'lacute': 'l', 'lcaron': 'l', 'lcommaaccent': 'l', 'ldot': 'l', 'minute': 'minute', 'second': 'minute', 'm': 'n', 'n': 'n', 'nacute': 'n', 'ncaron': 'n', 'ncommaaccent': 'n', 'ntilde': 'n', 'r': 'n', 'racute': 'n', 'rcaron': 'n', 'rcommaaccent': 'n', 'eng': 'n', 'nacute.pl': 'n', 'cacute.pl': 'o', 'oacute.pl': 'o', 'dcroat': 'o', 'oe': 'o', 'o': 'o', 'oacute': 'o', 'obreve': 'o', 'ocircumflex': 'o', 'odieresis': 'o', 'ograve': 'o', 'ohungarumlaut': 'o', 'omacron': 'o', 'otilde': 'o', 'q': 'o', 'd': 'o', 'dcaron': 'o', 'e': 'o', 'eacute': 'o', 'ebreve': 'o', 'ecaron': 'o', 'ecircumflex': 'o', 'edieresis': 'o', 'edotaccent': 'o', 'egrave': 'o', 'emacron': 'o', 'eogonek': 'o', 'oslash': 'o', 'c': 'o', 'cacute': 'o', 'ccaron': 'o', 'ccedilla': 'o', 'ccircumflex': 'o', 'cdotaccent': 'o', 'ecircumflexacute': 'o', 'ecircumflexdotbelow': 'o', 'ecircumflexgrave': 'o', 'ecircumflexhoi': 'o', 'ecircumflextilde': 'o', 'edotbelow': 'o', 'ehookabove': 'o', 'etilde': 'o', 'ocircumflexacute': 'o', 'ocircumflexdotbelow': 'o', 'ocircumflexgrave': 'o', 'ocircumflexhoi': 'o', 'ocircumflextilde': 'o', 'odotbelow': 'o', 'ohoi': 'o', 'ohorn': 'o', 'ohornacute': 'o', 'ohorndotbelow': 'o', 'ohorngrave': 'o', 'ohornhoi': 'o', 'ohorntilde': 'o', 'cdotbelow': 'o', 'oslashacute': 'o', 'percent': 'percent', 'perthousand': 'percent', 'comma': 'period', 'period': 'period', 'ellipsis': 'period', 'divide': 'plus', 'minus': 'plus', 'plus': 'plus', 'quotedblbase': 'quotebase', 'quotesinglbase': 'quotebase', 'quotedblleft': 'quoteleft', 'quoteleft': 'quoteleft', 'quotedblright': 'quoteright', 'quoteright': 'quoteright', 'quotedbl': 'quotesingle', 'quotesingle': 'quotesingle', 's': 's', 'sacute': 's', 'scaron': 's', 'scedilla': 's', 'scircumflex': 's', 'scommaaccent': 's', 'sacute.pl': 's', 't': 't', 'tcaron': 't', 'tcommaaccent': 't', 'tbar': 't', 'uni021B': 't', 'u': 'u', 'uacute': 'u', 'ubreve': 'u', 'ucircumflex': 'u', 'udieresis': 'u', 'ugrave': 'u', 'uhungarumlaut': 'u', 'umacron': 'u', 'uogonek': 'u', 'uring': 'u', 'utilde': 'u', 'udotbelow': 'u', 'uhoi': 'u', 'uhorn': 'u', 'uhornacute': 'u', 'uhorndotbelow': 'u', 'uhorngrave': 'u', 'uhornhoi': 'u', 'uhorntilde': 'u', 'w': 'w', 'wacute': 'w', 'wcircumflex': 'w', 'wdieresis': 'w', 'wgrave': 'w', 'y': 'y', 'yacute': 'y', 'ycircumflex': 'y', 'ydieresis': 'y', 'ygrave': 'y', 'ydotbelow': 'y', 'yhoi': 'y', 'ytilde': 'y', 'zacute.pl': 'z', 'z': 'z', 'zacute': 'z', 'zcaron': 'z', 'zdotaccent': 'z'}]
	assert testFont1.glyphToKerningGroupMapping == result