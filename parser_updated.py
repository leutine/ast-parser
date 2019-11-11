# coding: utf-8

import ast
import os


def analyze(module):
    with open(module, "r") as source:
        tree = ast.parse(source.read())
        analyzer = Analyzer()
        analyzer.visit(tree)
        analyzer.report(module)


def main():
    e_folder = '.\\elements'
    v_folder = '.\\views'

    for module in os.listdir(e_folder):
        if '__init__' not in module:
            analyze(os.path.join(e_folder, module))


class Analyzer(ast.NodeVisitor):
    def __init__(self, selected_only=True):
        self.classes = []
        self.functions = []
        self.selected_only = selected_only

    def visit_ClassDef(self, node):
        if self._is_parsed_element(node):
            self.classes.append(node.name)
            self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if self._is_parsed_method(node):
            self.functions.append(node.name)
            self.generic_visit(node)

    def report(self, module):
        print(f'Module: {module}:')
        print('Classes:', self.classes)
        print('Methods:', self.functions)
        print()

    def _is_parsed_element(self, node):
        return any(
            isinstance(n, ast.Name) and n.id == 'parse' for n in node.decorator_list) if self.selected_only else True

    @staticmethod
    def _is_parsed_method(node):
        return not node.name.startswith('_')


if __name__ == "__main__":
    main()
