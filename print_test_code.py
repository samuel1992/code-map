from src.parser import Parser


code = """
import os
import sys

from collections import namedtuple

from .config import MyConfiguration


def some_function():
    return a + b


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


if __name__ == '__main__':
    parser = Parser(code)
    parser.fetch_lines()
    parser.fetch_imports()
    parser.fetch_classes()
    parser.fetch_methods_or_functions()

    print("\nIMPORTS:")

    for i in parser.imports:
        print(i)

    print("\nOBJECTS:")

    for i in parser.objects:
        print(i)

    print("\n")
