from mojo.roboFont import RFont
import git

def getFontRepo(font):
    dfont = font.naked()
    dfont._repo = git.Repo(font.path, search_parent_directories=True)
    dfont._repo.fontPath = font.path
    dfont.glifPathMap = {}
    for g in font:
        dfont.glifPathMap[g.path] = g
    return dfont._repo

RFont.repo = property(lambda self: getFontRepo(self))
