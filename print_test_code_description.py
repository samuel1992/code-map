from src.parser import Parser

from fixtures.sample_code import code


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
