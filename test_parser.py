import pytest

from parser import get_definition, CodeLine


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


class TestCodeLine:
    def test_fetch_indentation(self):
        line = '    return "bla bla"'
        code_line = CodeLine(line)
        code_line.fetch_indentation()

        assert code_line.indents == 1

    def test_fetch_multiple_indentation(self):
        line = '            return "bla bla"'
        code_line = CodeLine(line)
        code_line.fetch_indentation()

        assert code_line.indents == 3

    def test_fetch_dedentation(self):
        line_before = '        return "bla"'
        line = '    else:'

        previous_code_line = CodeLine(line_before)
        previous_code_line.fetch_indentation()

        code_line = CodeLine(line)
        code_line.fetch_indentation()
        code_line.fetch_dedentation(previous_code_line)

        assert code_line.indents == 1
        assert code_line.dedents == 1

    def test_fetch_multiple_dedentation(self):
        line_before = '    return "bla"'
        line = 'class Something:'

        previous_code_line = CodeLine(line_before)
        previous_code_line.fetch_indentation()

        code_line = CodeLine(line)
        code_line.fetch_indentation()
        code_line.fetch_dedentation(previous_code_line)

        assert code_line.indents == 0
        assert code_line.dedents == 1

    def test_fetch_dedentation_raises_not_indents_error(self):
        line_before = '    return "bla"'
        line = 'class Something:'

        previous_code_line = CodeLine(line_before)
        previous_code_line.fetch_indentation()

        code_line = CodeLine(line)

        with pytest.raises(Exception):
            code_line.fetch_dedentation(previous_code_line)
