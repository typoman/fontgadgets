import functools
from warnings import warn
from typing import Optional, Callable

DEBUG = False  # Global flag for debug mode


def _register_and_check_patch(
    cls, target_name, module_name, override, is_existing, type_desc="Method"
):
    """
    Handles the logic for checking conflicts, warnings, and updating the
    __patched_methods__ registry.
    """
    if not hasattr(cls, "__patched_methods__"):
        setattr(cls, "__patched_methods__", {})
    patched_methods = cls.__patched_methods__

    if is_existing:
        if override is False:
            if target_name in patched_methods:
                existing_module = patched_methods[target_name]
                if existing_module == module_name:
                    warn(
                        f"Overriding already patched {type_desc.lower()} '{target_name}'.",
                        Warning,
                    )
                else:
                    msg = f"{type_desc} '{target_name}' in {cls.__name__} was patched from module '{existing_module}'. Conflict from '{module_name}'."
                    if not DEBUG:
                        raise ValueError(msg)
                    else:
                        warn(f"DEBUG: {msg}", Warning)
            else:
                msg = f"{type_desc} '{target_name}' already exists in {cls.__name__} and was not patched."
                if not DEBUG:
                    raise ValueError(msg)
                else:
                    warn(f"DEBUG: {msg}", Warning)
        else:
            # override is true, existing is present.
            # valid replacement scenario.
            pass
    else:
        # attribute does not exist.
        # if override is true (default), we simply add it.
        # if override is false, we also simply add it (no conflict).
        pass

    # register the patch
    patched_methods[target_name] = module_name


def _create_wrapper_with_original(new_func, orig_callable, target_cls, attr_name, is_property=False):
    @functools.wraps(new_func)
    def wrapper(self, *args, **kwargs):
        bound_original = None
        if orig_callable:
            bound_original = orig_callable.__get__(self, target_cls)
        module_globals = new_func.__globals__
        original_in_module = module_globals.get('original', None)

        def original_factory():
            if bound_original is None:
                raise AttributeError(f"No original implementation for '{attr_name}' found.")
            
            if is_property:
                # For properties, create a property descriptor that calls the original
                if len(args) > 0 or len(kwargs) > 0:
                    # This is a setter case
                    prop = property(fset=lambda _, val: bound_original(val))
                else:
                    # This is a getter case
                    prop = property(fget=lambda _: bound_original())
                return type('_OriginalWrapper', (), {attr_name: prop})()
            else:
                # Regular method case
                return type('_OriginalWrapper', (), {attr_name: bound_original})()

        module_globals['original'] = original_factory
        try:
            result = new_func(self, *args, **kwargs)
        finally:
            if original_in_module is not None:
                module_globals['original'] = original_in_module
            else:
                del module_globals['original']
        return result
    return wrapper


# --- decorators ---

def method(*target_classes: type, override: bool = True) -> Callable:
    """
    Decorator to add or replace a method on one or more classes.

    This decorator can either add a new method or replace an existing one on
    the given classes. When `override` is True (default), it replaces the
    existing method and provides access to the original via `original()`.
    When `override` is False, it adds the method with conflict checks.

    Example usage:
        @method(MyClass, override=True)
        def my_target_method(self, arg):
            '''New implementation with access to original.'''
            # original() returns a proxy object containing the previous implementation.
            # You must call the method by its name on this proxy.
            result = original().my_target_method(arg)
            return result

    Args:
        *target_classes: One or more class objects to patch.
        override: If True (default), replace existing methods and provide
            access to original via `original()`. If False, only add the
            method if it doesn't exist, raising an error on conflicts.

    Returns:
        A decorator function that patches the target classes.

    Raises:
        TypeError: If no target classes are provided or if any argument is
            not a class.
        ValueError: If `override` is False and a conflict is detected
            (unless DEBUG mode is enabled).
    """

    def decorator(func):
        if not target_classes:
            raise TypeError("No target classes provided to the decorator.")

        method_name = func.__name__
        module_name = func.__module__

        for cls in target_classes:
            if not isinstance(cls, type):
                raise TypeError(
                    f"Expected a class in the decorator, but got:\n{type(cls)}"
                )

            original_method = cls.__dict__.get(method_name, None)
            is_existing = original_method is not None
            _register_and_check_patch(
                cls, method_name, module_name, override, is_existing, type_desc="Method"
            )

            # prepare wrapper
            if is_existing and override:
                # if overriding, we wrap to provide original()
                # explicitly delete logic preserved from original implementation
                if method_name in cls.__dict__:
                    delattr(cls, method_name)
                wrapper = _create_wrapper_with_original(
                    func, original_method, cls, method_name
                )
            else:
                # if adding new (override=false or override=true but new), just use the function
                wrapper = func

            setattr(cls, method_name, wrapper)

        return func

    return decorator



def _patch_property(target_classes, property_name, is_setter, override):
    def decorator(func):
        if not target_classes:
            raise TypeError('No target classes provided to the decorator.')
        prop_name = property_name or func.__name__
        module_name = func.__module__
        for cls in target_classes:
            if not isinstance(cls, type):
                raise TypeError(f'Expected a class in the decorator, but got:\n{type(cls)}')
            old_prop = cls.__dict__.get(prop_name, None)
            is_existing = old_prop is not None
            _register_and_check_patch(cls, prop_name, module_name, override, is_existing, type_desc='Attribute')
            fget, fset, fdel, doc = (None, None, None, None)
            if isinstance(old_prop, property):
                fget, fset, fdel, doc = (old_prop.fget, old_prop.fset, old_prop.fdel, old_prop.__doc__)
            if is_setter:
                if fset and override:
                    wrapper = _create_wrapper_with_original(func, fset, cls, prop_name, is_property=True)
                else:
                    wrapper = func
                fset = wrapper
            else:
                if fget and override:
                    wrapper = _create_wrapper_with_original(func, fget, cls, prop_name, is_property=True)
                else:
                    wrapper = func
                fget = wrapper
                if doc is None:
                    doc = func.__doc__
            setattr(cls, prop_name, property(fget, fset, fdel, doc))
        return func
    return decorator



def property_getter(
    *target_classes: type, property_name: Optional[str] = None, override: bool = True
) -> Callable:
    """
    Decorator to patch a property getter on one or more classes.

    This decorator replaces or adds a property getter on the given classes.
    When `override` is True (default), it replaces the existing getter and
    provides access to the original via `original().property_name`. When
    `override` is False, it only adds the getter if it doesn't exist.

    Example usage:
        @property_getter(MyClass, property_name='value', override=True)
        def get_value(self):
            '''New getter with access to original.'''
            # Access original property value via original()
            original_val = original().value
            return original_val * 2

    Args:
        *target_classes: One or more class objects to patch.
        property_name: Name of the property to patch. If None, uses the
            decorated function's name.
        override: If True (default), replace existing getter and provide
            access to original via `original().property_name`. If False,
            only add the getter if it doesn't exist.

    Returns:
        A decorator function that patches the property getter.

    Raises:
        TypeError: If no target classes are provided or if any argument is
            not a class.
        ValueError: If `override` is False and a conflict is detected
            (unless DEBUG mode is enabled).
    """
    return _patch_property(
        target_classes, property_name, is_setter=False, override=override
    )


def property_setter(
    *target_classes: type, property_name: Optional[str] = None, override: bool = True
) -> Callable:
    """
    Decorator to patch a property setter on one or more classes.

    This decorator replaces or adds a property setter on the given classes.
    When `override` is True (default), it replaces the existing setter and
    provides access to the original via `original().property_name = value`.
    When `override` is False, it only adds the setter if it doesn't exist.

    Example usage:
        @property_setter(MyClass, property_name='value', override=True)
        def set_value(self, new_val):
            '''New setter with access to original.'''
            # Access original setter via original()
            original().value = new_val * 0.5  # Modify before setting

    Args:
        *target_classes: One or more class objects to patch.
        property_name: Name of the property to patch. If None, uses the
            decorated function's name.
        override: If True (default), replace existing setter and provide
            access to original via `original().property_name = value`.
            If False, only add the setter if it doesn't exist.

    Returns:
        A decorator function that patches the property setter.

    Raises:
        TypeError: If no target classes are provided or if any argument is
            not a class.
        ValueError: If `override` is False and a conflict is detected
            (unless DEBUG mode is enabled).
    """
    return _patch_property(
        target_classes, property_name, is_setter=True, override=override
    )


def doc(**kwargs):
    """
    A decorator to format the docstring of a function or class.

    It takes keyword arguments and uses them to format the docstring
    of the decorated object using `str.format()`.

    Example:
        @doc(version="1.0")
        def my_function():
            \"\"\"My function, version {version}.\"\"\"
            pass
    """

    def decorator(obj):
        if obj.__doc__:
            obj.__doc__ = obj.__doc__.format(**kwargs)
        return obj

    return decorator
