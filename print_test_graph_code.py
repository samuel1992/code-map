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


# Test
# G = GraphVisualization()
# G.add_edge("A", "B")
# G.add_edge("A", "C")
# G.add_edge("B", "C")
# G.add_edge("C", "D")
# G.visualize()


def _line_external_references(line, objects):
    found = []
    for _object in objects:
        result = re.search(fr'{_object.name}\(.*?\)|{_object.name}\(.*?', line)
        if result:
            found.append(_object)

    return found


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

        if line.parent:
            line_parent = line.parent.name
        else:
            line_parent = ""

        # print(f'=> {line.number} - {line.raw_line} (parent: {line_parent}) ==> {line_references}')

        if line_parent and line_references:
            for r in line_references:
                G.add_edge(line_parent, r.name)

    G.visualize()
