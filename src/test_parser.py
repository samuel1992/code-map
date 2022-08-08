import pytest

from .parser import CodeLine, CodeBlock

from .types import Types


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

        assert code_line.definition == 'CLASS'

    def test_class_with_inheritance_definition(self):
        class_definition_with_inheritance = 'class SomeClass(MotherClass):'

        code_line = CodeLine(class_definition_with_inheritance)
        code_line.fetch_definition()

        assert code_line.definition == 'CLASS'

    def test_method_definition(self):
        method_definition = 'def somemethod(self, a, b, c):'

        code_line = CodeLine(method_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'METHOD'

    def test_method_definition_class_method(self):
        class_method_definition = 'def somemethod(cls, a, b):'

        code_line = CodeLine(class_method_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'METHOD'

    def test_function_definition(self):
        function_definition = 'def somefunction():'

        code_line = CodeLine(function_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'FUNCTION'

    def test_function_definition_with_parameters(self):
        function_with_parameters_definition = 'def somefunction(a, b, c):'

        code_line = CodeLine(function_with_parameters_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'FUNCTION'

    def test_variable_definition(self):
        variable_definition = 'some = some'

        code_line = CodeLine(variable_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'VARIABLE'

    def test_variable_definition_without_space(self):
        variable_without_space_definition = 'some=some'

        code_line = CodeLine(variable_without_space_definition)
        code_line.fetch_definition()

        assert code_line.definition == 'VARIABLE'

    def test_operation_definition(self):
        pass


class TestCodeBlock:
    @pytest.fixture
    def _lines(self):
        lines = [
            CodeLine('class FirstClass:'),
            CodeLine('    def __init__(self, query, file):'),
            CodeLine('        self._query = query'),
            CodeLine('        self._file = file'),
            CodeLine('    # Some comment here'),
            CodeLine('    # some more comment ---> here'),
            CodeLine('    @property'),
            CodeLine('    def content(self):'),
            CodeLine('        return self._file.template.render(self._query)'),
            CodeLine('    def method_with_conditions(self):'),
            CodeLine('        if self._query:'),
            CodeLine('            return "query"'),
            CodeLine('        else:'),
            CodeLine('            return "no query"'),
            CodeLine('    def save(self):'),
            CodeLine('        with open(self._file.path, "w") as file:'),
            CodeLine('            file.write(self.content)'),
            CodeLine('variable_a = "something"'),
            CodeLine('class SecondClass:'),
            CodeLine('    pass'),
        ]
        for i, line in enumerate(lines):
            previous_line = None
            if i != 0:
                previous_line = lines[i - 1]

            line.fetch_indentation()
            line.fetch_dedentation(previous_line)
            line.fetch_definition()
            lines[i] = line

        return lines

    def test_code_block_identification(self, _lines):
        code_block = CodeBlock(definition=Types.klass)
        assert code_block.definition == Types.klass

    def test_code_block_add_lines(self, _lines):
        code_block = CodeBlock(Types.klass, indents=0)
        code_block.add_lines(lines=_lines)

        assert len(code_block.lines) == 17

    def test_code_block_raises_when_try_to_add_unfetched_lines(self):
        code_block = CodeBlock(Types.function)
        lines = [CodeLine('def something():')]

        with pytest.raises(AssertionError):
            code_block.add_lines(lines)

    def test_code_block_raises_when_try_invalid_definition(self):
        with pytest.raises(AssertionError):
            CodeBlock('')
