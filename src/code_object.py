import re

from ._types import Types

from .code_line import CodeLine


class CodeObject:
    """
    Python blocks of code that represents an 'object':
        - classes
        - methods
        - functions

    ex of a block:
        ```
        def something():
            # part of the block
            return 'bla'
        ````
    The code blocks type are defined in this class on a constant
    """
    types = [
        Types.klass.name,
        Types.definition.name,
    ]

    def __init__(self, indents: int = None, dedents: int = None):
        self.indents = indents
        self.dedents = dedents
        self.lines = []
        self.parent = None
        self.definition = None

    def fetch_definition(self):
        assert self.lines, 'CodeObject must have lines to fetch its definition'
        self.definition = self.lines[0].definition

    @property
    def raw_line(self):
        return self.lines[0].raw_line

    @property
    def name(self):
        first_line = self.lines[0].raw_line
        result = re.search(r'[def|class]+\ +[a-z|A-Z|0-9|_]+', first_line)
        return result.group(0).strip().split(' ')[-1]

    def _add(self, line: CodeLine):
        assert line.indents is not None
        assert line.dedents is not None
        assert line.definition is not None
        self.lines.append(line)

    def add_lines(self, lines: list):
        assert self.indents is not None

        self._add(lines[0])

        for line in lines[1:]:
            if line.indents > self.indents:
                self._add(line)

            # We stop the iteration if the line indentation is out of the block
            # indentation range
            if line.indents == self.indents or line.indents < self.indents:
                break

    def __str__(self):
        return f'\n{self.name} (definition: {self.definition})'

    def __repr__(self):
        return f'<object {self.name}>'
