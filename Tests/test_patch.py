from utils import *
from fontgadgets import patch

# test basic patch into a single class
def test_basic_patch():
   class MyClass1:
       pass

   @patch.method(MyClass1)
   def Patched_method_1(self, x):
       return x * 2

   my_instance_1 = MyClass1()
   assert my_instance_1.Patched_method_1(5) == 10

# test patch into multiple classes
def test_multipeclass_patch():
   class MyClass2:
       pass
   class MyClass3:
       pass

   @patch.method(MyClass2, MyClass3)
   def Patched_method_2(self, y):
       return y + 10

   my_instance_2 = MyClass2()
   my_instance_3 = MyClass3()
   assert my_instance_2.Patched_method_2(3) == 13
   assert my_instance_3.Patched_method_2(7) == 17

# test method name conflict with existing method (valueerror in normal mode)
def test_method_name_conflict():
   class MyClass5:
       def existing_method(self):
           return "Existing method"

   with pytest.raises(ValueError):
       @patch.method(MyClass5, override=False)
       def existing_method(self):  # Conflict with existing method
           return "Patched method"

# test non-conflicting patch
def test_non_conflicting_patch():
   class MyClass5:
       def existing_method(self):
           return "Existing method"

   @patch.method(MyClass5)
   def Patched_method_4(self):
       return "Non-conflicting Patched method"

   my_instance_5 = MyClass5()
   assert my_instance_5.Patched_method_4() == "Non-conflicting Patched method"

# test no target classes provided (typeerror)
def test_no_target_classes():
   with pytest.raises(TypeError):
       @patch.method() 
       def some_method(self):
           pass

# test empty list of target classes (typeerror)
def test_empty_target_classes():
   with pytest.raises(TypeError):
       @patch.method([])
       def some_method(self):
           pass

# test invalid target class (not a class) (typeerror)
def test_invalid_target_class():
   my_variable = 10
   with pytest.raises(TypeError):
       @patch.method(my_variable)
       def some_method(self):
           pass

def test_repatch_same_module():
    class MyClass4:
        pass

    @patch.method(MyClass4)
    def Patched_method_3_v1(self):
        return "Initial patch"

    @patch.method(MyClass4)
    def Patched_method_3_v2(self):  # Clearer naming
        return "Re-Patched method"

    my_instance_4 = MyClass4()
    assert my_instance_4.Patched_method_3_v2() == "Re-Patched method"

def test_debug_mode_overwrite():
    try:
        patch.DEBUG = True
        class MyClass6:
            def conflicting_method(self):
                return "Original method"

        @patch.method(MyClass6, override=False)
        def conflicting_method(self):
            return "Patched method in DEBUG mode"

        my_instance_6 = MyClass6()
        assert my_instance_6.conflicting_method() == "Patched method in DEBUG mode"
    finally:
        patch.DEBUG = False

def test_error_messages():
    class MyClass7:
        pass

    with pytest.raises(TypeError, match="Expected a class in the decorator, but got:"):
        @patch.method("not_a_class, override=False")  # Invalid type
        def some_method(self):
            pass

def test_override_method_single_class():
    class MyClass:
        def __init__(self, name):
            self.name = name

        def add_family_name(self, family_name):
            return f"{self.name} {family_name}"

    instance = MyClass("alice")
    assert instance.add_family_name("from") == "alice from"

    @patch.method(MyClass)
    def add_family_name(self, family_name, family_suffix):
        original_result = original().add_family_name(family_name)
        return f"{original_result} {family_suffix}"

    instance = MyClass("alice")
    assert instance.add_family_name("from", "wonder") == "alice from wonder"

def test_override_method_multiple_classes():
    class MyClass1:
        def __init__(self, name):
            self.name = name

        def add_family_name(self, family_name):
            return f"{self.name} {family_name}"

    class MyClass2:
        def __init__(self, name):
            self.name = name

        def add_family_name(self, family_name):
            return f"{self.name} {family_name}"

    instance1 = MyClass1("alice1")
    instance2 = MyClass2("alice2")
    assert instance1.add_family_name("from") == "alice1 from"
    assert instance2.add_family_name("from") == "alice2 from"

    @patch.method(MyClass1, MyClass2)
    def add_family_name(self, family_name, family_suffix):
        original_result = original().add_family_name(family_name)
        return f"{original_result} {family_suffix}"

    instance1 = MyClass1("alice1")
    instance2 = MyClass2("alice2")
    assert instance1.add_family_name("from", "wonder") == "alice1 from wonder"
    assert instance2.add_family_name("from", "wonder") == "alice2 from wonder"

def test_nested_override_method():
    class MyClass:
        def __init__(self, name):
            self.name = name

        def add_family_name(self, family_name):
            return f"{self.name} {family_name}"

    instance = MyClass("alice")
    assert instance.add_family_name("from") == "alice from"

    @patch.method(MyClass)
    def add_family_name(self, family_name, family_suffix):
        original_result = original().add_family_name(family_name)
        return f"{original_result} {family_suffix}"

    instance = MyClass("alice")
    assert instance.add_family_name("from", "wonder") == "alice from wonder"

    @patch.method(MyClass)
    def add_family_name(self, family_name, family_suffix, second_suffix):
        original_result = original().add_family_name(family_name, family_suffix)
        return f"{original_result} {second_suffix}"

    instance = MyClass("alice")
    assert instance.add_family_name("from", "wonder", "land") == "alice from wonder land"

def test_new_method_accesing_original():
    class MyClass:
        pass

    with pytest.raises(NameError, match="name 'original' is not defined"):
        @patch.method(MyClass)
        def non_existent_method(self):
            original_result = original()
            return "should not reach here"

        instance = MyClass()
        assert instance.non_existent_method()

def test_subclass_patch():
    class ParentClass:
        def parent_method(self):
            return "Parent"

    class ChildClass(ParentClass):
        pass

    @patch.method(ParentClass)
    def parent_method(self):
        return "Patched Parent"

    @patch.method(ChildClass)
    def parent_method(self):
        return "Patched Child"

    parent_instance = ParentClass()
    child_instance = ChildClass()

    assert parent_instance.parent_method() == "Patched Parent"
    assert child_instance.parent_method() == "Patched Child"


def test_property_getter_patch():
    class MyClass:
        def __init__(self):
            self._value = 10
        
        @property
        def value(self):
            return self._value

    @patch.property_getter(MyClass)
    def value(self):
        return original().value * 2

    instance = MyClass()
    assert instance.value == 20

def test_property_setter_patch():
    class MyClass:
        def __init__(self):
            self._value = 10
        
        @property
        def value(self):
            return self._value
        
        @value.setter
        def value(self, val):
            self._value = val

    @patch.property_setter(MyClass)
    def value(self, val):
        original().value = val * 2

    instance = MyClass()
    instance.value = 5
    assert instance.value == 10

def test_property_getter_with_name():
    class MyClass:
        def __init__(self):
            self._val = 100
        
        @property
        def my_prop(self):
            return self._val

    @patch.property_getter(MyClass, property_name="my_prop")
    def renamed_getter(self):
        return original().my_prop + 50

    instance = MyClass()
    assert instance.my_prop == 150

def test_property_setter_with_name():
    class MyClass:
        def __init__(self):
            self._val = 100
        
        @property
        def my_prop(self):
            return self._val
        
        @my_prop.setter
        def my_prop(self, val):
            self._val = val

    @patch.property_setter(MyClass, property_name="my_prop")
    def renamed_setter(self, val):
        original().my_prop = val - 20

    instance = MyClass()
    instance.my_prop = 50
    assert instance.my_prop == 30

def test_property_getter_conflict():
    class MyClass:
        @property
        def prop(self):
            return 1

    with pytest.raises(ValueError):
        @patch.property_getter(MyClass, override=False)
        def prop(self):
            return 2

def test_property_setter_conflict():
    class MyClass:
        _val = 0
        
        @property
        def prop(self):
            return self._val
        
        @prop.setter
        def prop(self, val):
            self._val = val

    with pytest.raises(ValueError):
        @patch.property_setter(MyClass, override=False)
        def prop(self, val):
            self._val = val + 1
