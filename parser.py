import re


def get_definition(line: str) -> str:
    """ receive a line of code and return what that line is:
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
"""


for i in code.split('\n'):
    print(get_definition(i), '-->', i)
