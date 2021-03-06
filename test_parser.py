from parser import get_definition


def test_class_definitions():
    class_definition = 'class SomeClass:'
    class_definition_with_inheritance = 'class SomeClass(MotherClass):'

    assert get_definition(class_definition) == 'class'
    assert get_definition(class_definition_with_inheritance) == 'class'


def test_method_definitions():
    method_definition = 'def somemethod(self, a, b, c):'
    class_method_definition = 'def somemethod(cls, a, b):'

    assert get_definition(method_definition) == 'method'
    assert get_definition(class_method_definition) == 'method'


def test_function_definitions():
    function_definition = 'def somefunction():'
    function_with_parameters_definition = 'def somefunction(a, b, c):'

    assert get_definition(function_definition) == 'function'
    assert get_definition(function_with_parameters_definition) == 'function'


def test_variable_definitions():
    variable_definition = 'some = some'
    variable_without_space_definition = 'some=some'

    assert get_definition(variable_definition) == 'variable'
    assert get_definition(variable_without_space_definition) == 'variable'


def test_operation_definition():
    pass
