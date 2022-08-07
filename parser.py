import re


class CodeLine:
    """
    Represent a line of code
    """
    def __init__(self, raw_line: str):
        self.raw_line = raw_line
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

        if re.match(r'^class\ .*', line):
            self.definition = 'class'

        elif re.match(r'^def\ .*\([self|cls].*', line):
            self.definition = 'method'

        elif re.match(r'^def\ .*\(?\)', line):
            self.definition = 'function'

        elif re.match(r'.*\=.*', line):
            self.definition = 'variable'

        else:
            self.definition = 'operation'

    def fetch_indentation(self):
        """
        Reads the raw code and count how many identation we have on it
        """
        indentation_groups = re.findall(r'\ \ \ \ ', self.raw_line)
        self.indents = len(indentation_groups)

    def fetch_dedentation(self, previous_code_line: 'CodeLine'):
        """
        Reads the raw code, count the indentation and compare with the
        previous line of code
        """
        if self.indents is None:
            raise Exception(
                "You must fetch the indentation before the dedentation"
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


class Parser:
    def __init__(self, raw_code: str):
        self.raw_code = raw_code

    @property
    def lines(self):
        lines = []
        raw_lines = [i for i in self.raw_code.split('\n') if i]

        for i, line in enumerate(raw_lines):
            code_line = CodeLine(line)
            code_line.fetch_indentation()
            code_line.fetch_definition()

            if i != 0:
                code_line.fetch_dedentation(lines[i - 1])

            lines.append(code_line)

        return lines


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

    def save(self):
        with open(self._file.path, 'w') as file:
            file.write(self.content)


class SecondClass:
    @staticmethod
    def generate(type, query):
        assert type in MY_TYPES

        file = MY_TYPES[type]

        return FirstClass(query=query, file=file)

    def _private_method(self):
        a = 1
        b = 2
        a + b
        a += b
        return a
"""


parser = Parser(code)
for i in parser.lines:
    print(i)
