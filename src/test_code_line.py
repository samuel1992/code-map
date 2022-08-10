import pytest

from .code_line import CodeLine

from ._types import Types


class TestCodeLine:
    def test_fetch_indentation(self):
        line = '    return "bla bla"'
        code_line = CodeLine(line, 1)
        code_line.fetch_indentation()

        assert code_line.indents == 1

    def test_fetch_multiple_indentation(self):
        line = '            return "bla bla"'
        code_line = CodeLine(line, 1)
        code_line.fetch_indentation()

        assert code_line.indents == 3

    def test_fetch_dedentation(self):
        line_before = '        return "bla"'
        line = '    else:'

        previous_code_line = CodeLine(line_before, 1)
        previous_code_line.fetch_indentation()

        code_line = CodeLine(line, 1)
        code_line.fetch_indentation()
        code_line.fetch_dedentation(previous_code_line)

        assert code_line.indents == 1
        assert code_line.dedents == 1

    def test_fetch_multiple_dedentation(self):
        line_before = '    return "bla"'
        line = 'class Something:'

        previous_code_line = CodeLine(line_before, 1)
        previous_code_line.fetch_indentation()

        code_line = CodeLine(line, 1)
        code_line.fetch_indentation()
        code_line.fetch_dedentation(previous_code_line)

        assert code_line.indents == 0
        assert code_line.dedents == 1

    def test_fetch_dedentation_raises_not_indents_error(self):
        line_before = '    return "bla"'
        line = 'class Something:'

        previous_code_line = CodeLine(line_before, 1)
        previous_code_line.fetch_indentation()

        code_line = CodeLine(line, 1)

        with pytest.raises(Exception):
            code_line.fetch_dedentation(previous_code_line)

    def test_class_definition(self):
        class_definition = 'class SomeClass:'

        code_line = CodeLine(class_definition, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.klass.name

    def test_class_with_inheritance_definition(self):
        class_definition_with_inheritance = 'class SomeClass(MotherClass):'

        code_line = CodeLine(class_definition_with_inheritance, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.klass.name

    def test_function_or_method_definition(self):
        definition = 'def somefunction_or_method():'

        code_line = CodeLine(definition, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.definition.name

    def test_function_or_method_definition_with_parameters(self):
        definition_with_parameters_definition = 'def somefunction(a, b, c):'

        code_line = CodeLine(definition_with_parameters_definition, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.definition.name

    def test_variable_definition(self):
        variable_definition = 'some = some'

        code_line = CodeLine(variable_definition, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.variable.name

    def test_variable_definition_without_space(self):
        variable_without_space_definition = 'some=some'

        code_line = CodeLine(variable_without_space_definition, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.variable.name

    def test_loop_definition(self):
        loop = 'for i in range(1,2):'

        code_line = CodeLine(loop, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.loop.name

    def test_conditional_definition(self):
        conditional = 'if something and another:'

        code_line = CodeLine(conditional, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.conditional.name

    def test_operation_definition(self):
        operation = '1 + a / SomeClass()'

        code_line = CodeLine(operation, 1)
        code_line.fetch_definition()

        assert code_line.definition == Types.operation.name
