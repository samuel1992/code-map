import re

from .types import Types


class CodeLine:
    """
    Represent a line of code
    """
    def __init__(self, raw_line: str, parent: 'CodeLine' = None):
        self.raw_line = raw_line
        self.parent = parent
        self.indents = None
        self.dedents = None
        self.definition = None

    def fetch_definition(self) -> str:
        """
        Receive a line of code and fetch what that line is:
            - class
            - method
            - function
            - variable assignment
            - operation
        """
        line = self.raw_line.lstrip()

        if re.match(Types.comment.regex, line):
            self.definition = Types.comment.name

        elif re.match(Types.klass.regex, line):
            self.definition = Types.klass.name

        elif re.match(Types.method.regex, line):
            self.definition = Types.method.name

        elif re.match(Types.function.regex, line):
            self.definition = Types.function.name

        elif re.match(Types.variable.regex, line):
            self.definition = Types.variable.name

        elif re.match(Types.conditional.regex, line):
            self.definition = Types.conditional.name

        elif re.match(Types.loop.regex, line):
            self.definition = Types.loop.name

        else:
            self.definition = Types.operation.name

    def fetch_indentation(self):
        """
        Reads the raw code and count how many identation we have on it
        """
        indentation_groups = re.findall(r'\ \ \ \ ', self.raw_line)
        self.indents = len(indentation_groups)

    def fetch_dedentation(self, previous_code_line: 'CodeLine' = None):
        """
        Reads the raw code, count the indentation and compare with the
        previous line of code
        """
        self.dedents = 0

        if previous_code_line is None:
            return

        if self.indents is None:
            raise Exception(
                'You must fetch the indentation before the dedentation'
            )

        if (
            previous_code_line.indents is not None
            and previous_code_line.indents > self.indents
        ):
            self.dedents = previous_code_line.indents - self.indents

    def __str__(self):
        """
        Logict to pretty print the code and the indentation and dedentation
        """
        break_line = ''
        if self.indents == 0 or (self.indents == self.dedents):
            break_line = '\n'

        return (
            f'{break_line}'
            f'{self.raw_line} ==> '
            f'(indents: {self.indents or 0}, '
            f'dedents: {self.dedents or 0}, '
            f'definition: {self.definition})'
        )


class CodeBlock:
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
        Types.method.name,
        Types.function.name,
    ]

    def __init__(
        self, definition: str, indents: int = None, dedents: int = None
    ):
        assert definition in self.types, (
            f'CodeBlock definition {definition} is not valid'
        )

        self.definition = definition
        self.indents = indents
        self.dedents = dedents
        self.lines = []

    @property
    def name(self):
        pass

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


class Parser:
    def __init__(self, raw_code: str):
        self.raw_code = raw_code
        self.lines = []
        self.blocks = []

    def fetch_lines(self):
        raw_lines = [i for i in self.raw_code.split('\n') if i]

        for i, line in enumerate(raw_lines):
            previous_line = None
            if i != 0:
                previous_line = self.lines[i - 1]

            code_line = CodeLine(line)
            code_line.fetch_indentation()
            code_line.fetch_dedentation(previous_line)
            code_line.fetch_definition()

            self.lines.append(code_line)

    def fetch_blocks(self):
        if not self.lines:
            raise Exception(
               'You must fetch all the lines before fetch the blocks'
            )

        for i, line in enumerate(self.lines):
            if line.definition in CodeBlock.types:
                code_block = CodeBlock(line.indents, line.dedents)
                code_block.add_lines(self.lines[i:])
                self.blocks.append(code_block)

    def call(self):
        self.fetch_lines()
        self.fetch_blocks()


code = """
import os

from collections import namedtuple

from .config import MyConfiguration


class FirstClass:
    def __init__(self, query, file):
        self._query = query
        self._file = file

    # Some comment here
    # some more comment ---> here
    @property
    def content(self):
        return self._file.template.render(query=self._query)

    def method_with_conditions(self):
        if self._query:
            return 'query'
        else:
            return 'no query'

    def save(self):
        with open(self._file.path, 'w') as file:
            file.write(self.content)

variable_a = 'something'

class SecondClass:
    @staticmethod
    def generate(type, query):
        assert type in MY_TYPES

        file = MY_TYPES[type]

        return FirstClass(
            query=query, file=file
        )

    def _private_method(self):
        a = 1
        b = 2
        a + b
        a += b
        return a
"""
