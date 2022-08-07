import pytest

from parser import CodeLine


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

    def test_class_definition(self):
        class_definition = 'class SomeClass:'

        code_line = CodeLine(class_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'class'

    def test_class_with_inheritance_definition(self):
        class_definition_with_inheritance = 'class SomeClass(MotherClass):'

        code_line = CodeLine(class_definition_with_inheritance)
        code_line.fetch_definition()

        assert code_line.definition == 'class'

    def test_method_definition(self):
        method_definition = 'def somemethod(self, a, b, c):'

        code_line = CodeLine(method_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'method'

    def test_method_definition_class_method(self):
        class_method_definition = 'def somemethod(cls, a, b):'

        code_line = CodeLine(class_method_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'method'

    def test_function_definition(self):
        function_definition = 'def somefunction():'

        code_line = CodeLine(function_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'function'

    def test_function_definition_with_parameters(self):
        function_with_parameters_definition = 'def somefunction(a, b, c):'

        code_line = CodeLine(function_with_parameters_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'function'

    def test_variable_definition(self):
        variable_definition = 'some = some'

        code_line = CodeLine(variable_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'variable'

    def test_variable_definition_without_space(self):
        variable_without_space_definition = 'some=some'

        code_line = CodeLine(variable_without_space_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'variable'

    def test_operation_definition(self):
        pass
