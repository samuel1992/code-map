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

        if previous_code_line.indents > self.indents:
            self.dedents = previous_code_line.indents - self.indents


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
def test_function():
    return 'bla'

class Z:
    pass

class A(Z):
    def b(self, a):
        return a + 1

    @classmethod
    def _c(cls):
        pass

    def somemethod_with_conditions(self):
        if True:
            return 'SOMETHING'
        else:
            return 'ANOTHER'

        return 'SOMETHING ELSE'
"""


for i in code.split('\n'):
    print(get_definition(i), '-->', i)
