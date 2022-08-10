import pytest

from .code_object import CodeObject
from .code_line import CodeLine

from ._types import Types


class TestCodeObject:
    @pytest.fixture
    def _lines(self):
        lines = [
            CodeLine('class FirstClass:', 0),
            CodeLine('    def __init__(self, query, file):', 1),
            CodeLine('        self._query = query', 2),
            CodeLine('        self._file = file', 3),
            CodeLine('    # Some comment here', 4),
            CodeLine('    # some more comment ---> here', 5),
            CodeLine('    @property', 6),
            CodeLine('    def content(self):', 7),
            CodeLine('        return self._file.template(self._query)', 8),
            CodeLine('    def method_with_conditions(self):', 9),
            CodeLine('        if self._query:', 10),
            CodeLine('            return "query"', 11),
            CodeLine('        else:', 12),
            CodeLine('            return "no query"', 13),
            CodeLine('    def save(self):', 14),
            CodeLine('        with open(self._file.path, "w") as file:', 15),
            CodeLine('            file.write(self.content)', 16),
            CodeLine('variable_a = "something"', 17),
            CodeLine('class SecondClass:', 18),
            CodeLine('    pass', 19),
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

    def test_code_object_identification(self, _lines):
        code_object = CodeObject(indents=0)
        code_object.add_lines(_lines)
        code_object.fetch_definition()
        assert code_object.definition == Types.klass.name

    def test_code_object_add_lines(self, _lines):
        code_object = CodeObject(indents=0)
        code_object.add_lines(lines=_lines)

        assert len(code_object.lines) == 17

    def test_code_object_raises_when_try_to_add_unfetched_lines(self):
        code_object = CodeObject()
        lines = [CodeLine('def something():', 1)]

        with pytest.raises(AssertionError):
            code_object.add_lines(lines)
