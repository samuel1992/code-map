from typing import Optional

from .code_object import CodeObject
from .code_line import CodeLine
from ._types import Types


class Parser:
    def __init__(self, raw_code: str):
        self.raw_code = raw_code
        self.lines = []
        self.objects = []
        self.imports = []

    def _lines_set_parent(self, lines: list, parent: Optional[CodeObject]):
        for line in lines:
            if line.parent is None:
                line.parent = parent

    def fetch_lines(self):
        raw_lines = [i for i in self.raw_code.split('\n') if i]

        for number, line in enumerate(raw_lines):
            previous_line = None
            if number != 0:
                previous_line = self.lines[number - 1]

            code_line = CodeLine(line, number)
            code_line.fetch_indentation()
            code_line.fetch_dedentation(previous_line)
            code_line.fetch_definition()

            self.lines.append(code_line)

    def fetch_imports(self):
        for line in self.lines:
            if line.definition == Types.imports.name:
                self.imports.append(line)

    def fetch_classes(self):
        for line in self.lines:
            if line.definition == Types.klass.name:
                code_object = CodeObject(line.indents, line.dedents)
                code_object.add_lines(self.lines[line.number:])
                code_object.fetch_definition()

                self.objects.append(code_object)

                self._lines_set_parent(code_object.lines, code_object)

    def fetch_methods_or_functions(self):
        # TODO: add methods as objects
        for line in self.lines:
            if line.definition == Types.definition.name:
                if (
                    line.parent is not None
                    and line.parent.definition == Types.klass.name
                ):
                    line.definition = Types.method.name
                else:
                    line.definition = Types.function.name

                code_object = CodeObject(line.indents, line.dedents)
                code_object.add_lines(self.lines[line.number:])
                code_object.fetch_definition()

                self.objects.append(code_object)

                self._lines_set_parent(code_object.lines[1:], code_object)
