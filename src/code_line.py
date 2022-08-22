import re

from ._types import Types


class CodeLine:
    """
    Represent a line of code
    """
    def __init__(self, raw_line: str, number: int):
        self.raw_line = raw_line
        self.number = number
        self.parent = None
        self.indents = None
        self.dedents = None
        self.definition = None

    def fetch_definition(self) -> 'CodeLine':
        """
        Receive a line of code and fetch what that line is:
            - class
            - definition (def something())
            - variable assignment
            - operation
        """
        if self.definition is not None:
            return self

        line = self.raw_line.lstrip()

        if re.match(Types.comment.regex, line):
            self.definition = Types.comment.name

        elif re.match(Types.imports.regex, line):
            self.definition = Types.imports.name

        elif re.match(Types.klass.regex, line):
            self.definition = Types.klass.name

        elif re.match(Types.definition.regex, line):
            self.definition = Types.definition.name

        elif re.match(Types.variable.regex, line):
            self.definition = Types.variable.name

        elif re.match(Types.conditional.regex, line):
            self.definition = Types.conditional.name

        elif re.match(Types.loop.regex, line):
            self.definition = Types.loop.name

        else:
            self.definition = Types.operation.name

        return self

    def fetch_indentation(self) -> 'CodeLine':
        """
        Reads the raw code and count how many identation we have on it
        """
        indentation_groups = re.findall(r'\ \ \ \ ', self.raw_line)
        self.indents = len(indentation_groups)

        return self

    def fetch_dedentation(self, previous_code_line: 'CodeLine') -> 'CodeLine':
        """
        Reads the raw code, count the indentation and compare with the
        previous line of code
        """
        self.dedents = 0

        if previous_code_line is None:
            return self

        if self.indents is None:
            raise Exception(
                'You must fetch the indentation before the dedentation'
            )

        if (
            previous_code_line.indents is not None
            and previous_code_line.indents > self.indents
        ):
            self.dedents = previous_code_line.indents - self.indents

        return self

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
