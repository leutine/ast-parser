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
        self.classes = {}
        self.functions = {}
        self.selected_only = selected_only

    def visit_ClassDef(self, node):
        if self._is_parsed_element(node):
            self.classes[node.name] = [name.id for name in node.bases]
            self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if self._is_parsed_method(node):
            self.functions[node.name] = self.get_arguments(node.args)
            self.generic_visit(node)

    def get_arguments(self, node):
        args_list = [a.arg for a in node.args if 'self' not in a.arg]
        defaults_list = [self._get_default_arg_value(d) for d in node.defaults]
        len_diff = len(args_list) - len(defaults_list)
        args = args_list[:len_diff]
        for a, d in zip(args_list[len_diff:], defaults_list):
            args.append(f"{a}={d}")
        return args

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

    @staticmethod
    def _get_default_arg_value(d):
        if isinstance(d, ast.NameConstant):
            return str(d.value)
        elif isinstance(d, ast.Num):
            return str(d.n)
        elif isinstance(d, ast.Str):
            return f"'{d.s}'"


if __name__ == "__main__":
    main()
