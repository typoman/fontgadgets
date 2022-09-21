import defcon
import fontParts.world
import time
import sys
import importlib
from types import ModuleType
import logging
import inspect

logger = logging.getLogger(__name__)

def deepReload(m: ModuleType):
    name = m.__name__  # get the name that is used in sys.modules
    name_ext = name + '.'  # support finding sub modules or packages

    def compare(loaded: str):
        return (loaded == name) or loaded.startswith(name_ext)

    all_mods = tuple(sys.modules)  # prevent changing iterable while iterating over it
    sub_mods = filter(compare, all_mods)

    for pkg in sub_mods:
        p = importlib.import_module(pkg)
        importlib.reload(p)

def timeit(method):
    """
    A decorator that makes it possible to time functions.
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logger.debug('%r  %2.2f ms' %(method.__name__, (te - ts) * 1000))
        return result
    return timed

def _destroyRepresentationsForNotification(self, notification):
    notificationName = notification.name
    for name, dataDict in self.representationFactories.items():
        if notificationName in dataDict["destructiveNotifications"]:
            self.destroyRepresentation(name)
    # Overrids the defcon default behavior to make it possible for a child object
    # to destroy relevant representations on the parent. For example it would be
    # possible to make use of 'Kerning.Changed' destructive notification on the
    # 'Font' object:
    # https://github.com/robotools/defcon/issues/287
    try:
        p = self.getParent()
    except NotImplementedError:
        return
    p._destroyRepresentationsForNotification(notification)

defcon.objects.base.BaseObject._destroyRepresentationsForNotification = _destroyRepresentationsForNotification

def _getFontMethodParameters(funct):
    funcSign = inspect.signature(funct)
    args = [p.name for p in funcSign.parameters.values()]
    funcSign = ", ".join([str(p) for p in funcSign.parameters.values()])
    funcName = funct.__name__
    return args, funcName, funcSign

# This might be hacky, but it works for now!

class FontMethodsRegistrar():

    def __init__(self, funct):
        self.funct = funct
        self.funcSignature = inspect.signature(funct)
        self.args = [p.name for p in self.funcSignature.parameters.values()]
        self.objectName = self.args[0].capitalize()
        self.funcName = funct.__name__

    @property
    def fontPartsObject(self):
        try:
            return getattr(fontParts.fontshell, "R"+self.objectName)
        except AttributeError:
            logger.exception(f"R{self.objectName} is not a fontParts object. "
                            f"First argument in your function should be a "
                            f"defcon object name:\nFunction: {self.funcName}\n Argument:{self.args[0]}"
                            )

    @property
    def defconObject(self):
        try:
            return getattr(defcon, self.objectName)
        except AttributeError:
            logger.exception(f"{self.objectName} is not a defcon object. "
                            f"First argument in your function should be a "
                            f"defcon object name:\nFunction: {self.funcName}\n Argument:{self.args[0]}"
                            )

    def registerAsFontMethod(self):
        if self.args[1:]:
            setattr(self.defconObject, self.funcName, self.funct)
            funcName = f"fp{self.funcName}"
            code = [f"def {funcName}{self.funcSignature}:"]
            code.append(f"\treturn {self.args[0]}.naked().{self.funcName}({', '.join(self.args[1:])})")
            code.append(f"fontParts.fontshell.{self.args[0]}.{'R'+self.objectName}.{self.funcName} = {funcName}")
            exec("\n".join(code))
        else:
            # register the function as property
            setattr(self.fontPartsObject, self.funcName, property(lambda o: self.funct(o)))
            setattr(self.defconObject, self.funcName, property(lambda o: self.funct(o)))

    def _createPresentationMethodWtihArgs(self, isDefconMethod=False):
        nakedCode = ''
        funcName = self.funcName.capitalize()
        if isDefconMethod:
            funcName = 'defcon' + self.funcName
        else:
            nakedCode = '.naked()'
        code = [f"def {funcName}{self.funcSignature}:"]
        if self.funct.__doc__ is not None:
            code.append(f"\t\"\"\"\n\t{self.funct.__doc__.strip()}\n\t\"\"\"")
        code.append(f"\treturn {self.args[0]}{nakedCode}.getRepresentation('{self.funcRepresentationKey}', {', '.join([f'{v}={v}' for v in self.args[1:]])})")
        if isDefconMethod:
            code.append(f"defcon.{self.objectName}.{self.funcName} = {funcName}")
        else:
            code.append(f"fontParts.fontshell.{self.args[0]}.{'R'+self.objectName}.{self.funcName} = {funcName}")
        exec("\n".join(code))

    def registerAsFontCachedMethod(self, *destructiveNotifications):
        self.funcRepresentationKey = f"{self.funcName}.representation"
        defobjc = self.defconObject
        defcon.registerRepresentationFactory(defobjc, self.funcRepresentationKey, self.funct, destructiveNotifications=destructiveNotifications)
        if self.args[1:]:
            self._createPresentationMethodWtihArgs()
            self._createPresentationMethodWtihArgs(True)
        else:
            # register the function as property
            setattr(defobjc, self.funcName, property(lambda o: o.getRepresentation(self.funcRepresentationKey)))
            setattr(self.fontPartsObject, self.funcName, property(lambda o: o.naked().getRepresentation(self.funcRepresentationKey)))

def fontCachedMethod(*destructiveNotifications):
    """
    This is a decorator that makes it possible to convert self standing functions to
    methods on the fontParts and defcon objects. The results will be cached using
    defcon representations according to the destructiveNotifications. Note that if
    the function only has one argument then it will become a property.
    """
    def wrapper(funct):
        registrar = FontMethodsRegistrar(funct)
        registrar.registerAsFontCachedMethod(*destructiveNotifications)
    return wrapper

def fontMethod(funct):
    """
    This is a decorator that makes it possible to convert self standing functions to
    methods on the fontParts objects. If the function only has one argument then
    it will become a property.
    """
    registrar = FontMethodsRegistrar(funct)
    registrar.registerAsFontMethod()
