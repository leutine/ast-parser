# coding: utf-8

import os
import ast


# TODO: parse elements - done
# TODO: parse views - almost done
# TODO: generate tokens
# TODO: create files

# Old element parsing result:
# [{'name': 'method_name', 'args': [], 'args_in': []}]

# Desirable Token:
# ['cls_name: Full.Name.Of.Class.In.View',
# 'last_cls_name: view',
# 'func_name: element_name_in_view',
# 'action: element_method',
# 'args: arg=value',
# 'args_in: arg=arg']


def source(path):
    """
    source(path): read file or folder of files to get AST of module
    :param path: path to file or folder with .py modules to parse
    :return: yields parsed Abstract Syntax Tree
    """
    def read(filename):
        with open(filename, encoding='utf-8') as f:
            return ''.join(f.readlines())

    if os.path.isdir(path):
        for f in os.listdir(path):
            yield ast.parse(read(os.path.join(path, f)))
    else:
        yield ast.parse(read(path))


def arguments_of(node):
    args = []
    args_list = [a for a in node.args.args if 'self' not in a.arg]
    for a, v in zip(args_list, node.args.defaults):
        if isinstance(v, ast.NameConstant):
            args.append(f"{a.arg}={v.value}")
        elif isinstance(v, ast.Num):
            args.append(f"{a.arg}={v.n}")
    return args


def is_parsed_element(node):
    return any(isinstance(n, ast.Name) and n.id == 'parse' for n in node.decorator_list)


def is_parsed_method(node):
    return isinstance(node, ast.FunctionDef) and not node.name.startswith('_')


def parse_element(code):
    out = dict()

    classes = [node for node in ast.walk(code) if isinstance(node, ast.ClassDef) and is_parsed_element(node)]

    for c in classes:
        methods = {node.name: arguments_of(node) for node in ast.walk(c) if is_parsed_method(node)}
        out[c.name] = {**methods}

    return out


def parse_view(code):
    def parse(baseclass):
        d = dict()
        assigns = []
        for node in baseclass.body:
            if isinstance(node, ast.Assign):
                assigns.append((node.targets[0].id, node.value.func.id))
            if isinstance(node, ast.ClassDef):
                d.update({node.name: parse(node)})
            d.update({'assign': assigns})
        return d

    base_c = [node for node in ast.walk(code) if isinstance(node, ast.ClassDef)][0]

    out = dict()
    out[base_c.name] = parse(base_c)

    return out


# TODO: Read structure of view (parse_view) to get tokens
def get_view_tokens(d):
    def parse(di):
        for k, v in di.items():
            if type(v) is dict:
                class_names.append(k)
                parse(v)
                # break

    class_names = []
    last_cls_name = []
    func_name = []

    parse(d)
    print(class_names)

    # FOR ASSIGNMENTS
    # for k, v in d.items():
    #     if type(v) is dict:
    #         yield from parsed_to_tokens(v)
    #     else:
    #         yield (k, v)


def parse_elements(folder):
    for src in source(folder):
        if parse_element(src):
            print(parse_element(src))


def parse_views(folder):
    for src in source(folder):
        d = parse_view(src)
        print(d)
        print()
        get_view_tokens(d)


if __name__ == "__main__":
    e_folder = '.\\elements'
    v_folder = '.\\views'

    v_file = '.\\views\\view_three.py'
    e_file = '.\\elements\\element_main.py'

    parse_views(v_file)
