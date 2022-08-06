import re


class CodeLine:
    """
    Represent a line of code
    """
    def __init__(self, raw_line: str):
        self.raw_line = raw_line
        self.indents = None
        self.dedents = None

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
            f'(indents: {self.indents or 0}, dedents: {self.dedents or 0})'
        )


class Parser:
    def __init__(self, raw_code: str):
        self.raw_code = raw_code

    @property
    def lines(self):
        lines = []
        raw_lines = [i for i in self.raw_code.split('\n') if i]

        for i, line in enumerate(raw_lines):
            if i == 0:
                code_line = CodeLine(line)
                code_line.fetch_indentation()
            else:
                code_line = CodeLine(line)
                code_line.fetch_indentation()
                code_line.fetch_dedentation(lines[i - 1])

            lines.append(code_line)

        return lines


def get_definition(line: str) -> str:
    """
    Receive a line of code and return what that line is:
        - class
        - method
        - function
        - variable assignment
        - operation
    """
    line = line.lstrip()

    if re.match(r'^class\ .*', line):
        return 'class'

    if re.match(r'^def\ .*\([self|cls].*', line):
        return 'method'

    if re.match(r'^def\ .*\(?\)', line):
        return 'function'

    if re.match(r'.*\=.*', line):
        return 'variable'

    return 'operation'


code = """
import os

from collections import namedtuple

from .config import ASTERISK_FILES


class AsteriskFile:
    def __init__(self, query, file):
        self._query = query
        self._file = file

    # TODO: I let the content accessible if we want to run some test on it
    # we could validade the content with a more 'integration test' like
    @property
    def content(self):
        return self._file.template.render(query=self._query)

    def save(self):
        with open(self._file.path, 'w') as file:
            file.write(self.content)


class Writer:
    @staticmethod
    def generate(type, query):
        assert type in ASTERISK_FILES

        file = ASTERISK_FILES[type]

        return AsteriskFile(query=query, file=file)
"""


parser = Parser(code)
for i in parser.lines:
    print(i)
