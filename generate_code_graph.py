import re

import networkx as nx
import matplotlib.pyplot as plt

from src.parser import Parser

from fixtures.sample_code import code


class GraphVisualization:
    def __init__(self):
        self.visual = []

    def add_edge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()


def _line_external_references(line, objects):
    found = []
    for _object in objects:
        result = re.search(fr'{_object.name}\(.*?\)|{_object.name}\(.*?', line)
        if result and line != _object.raw_line:
            found.append(_object)

    return found


def _get_max_parent(parent):
    if parent.parent is None:
        return parent

    _get_max_parent(parent.parent)


if __name__ == '__main__':
    parser = Parser(code)
    parser.fetch_lines()
    parser.fetch_imports()
    parser.fetch_classes()
    parser.fetch_methods_or_functions()

    G = GraphVisualization()

    for line in parser.lines:
        line_references = _line_external_references(line.raw_line,
                                                    parser.objects)

        if line.parent and line_references:
            for ref in line_references:
                line_parent = _get_max_parent(line.parent)
                G.add_edge(f'<{line_parent.definition} {line_parent.name}>',
                           f'<{ref.definition} {ref.name}>')

    G.visualize()
