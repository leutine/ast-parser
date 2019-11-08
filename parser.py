# coding: utf-8

import ast
import os


# TODO: parse elements - done
# TODO: parse views - done
# TODO: generate tokens - almost done (need some fixing)
# TODO: create files
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
    def parse(baseclass, prev_name):
        d = dict()
        assigns = []
        base_name = prev_name
        for node in baseclass.body:
            if isinstance(node, ast.Assign):
                assigns.append((node.targets[0].id, node.value.func.id))
            if isinstance(node, ast.ClassDef):
                prev_name = prev_name + '.' + node.name
                d.update({prev_name: parse(node, prev_name)})
            prev_name = base_name
            d.update({'assign': assigns})
        return d

    base_c = [node for node in ast.walk(code) if isinstance(node, ast.ClassDef)][0]

    out = dict()
    out[base_c.name] = parse(base_c, base_c.name)

    return out


# TODO: Bug! Returns duplicated elements from view!
def get_tokens_from_view(parsed_dict):
    for k, v in parsed_dict.items():
        if type(v) is dict:
            for k1, v1 in v.items():
                if k1 == 'assign':
                    for a in v[k1]:
                        yield (k, k.split('.')[-1], a[0], a[1])
                else:
                    yield from get_tokens_from_view(v)


def get_tokens_from_elements(parsed_dict):
    for k, v in parsed_dict.items():
        if type(v) is dict:
            for k1, v1 in v.items():
                yield (k1, *[a for a in v1])


# Some terrible code here...
def parse_elements(folder, main_element):
    d1 = {}
    m = list(get_tokens_from_elements(parse_element(next(source(main_element)))))

    for src in source(folder):
        if parse_element(src):
            d = parse_element(src)
            element_methods = list(get_tokens_from_elements(d))
            if element_methods == m:
                continue
            d1.update({list(d.keys())[0]: element_methods + m})
    return d1


def parse_views(folder):
    for src in source(folder):
        d = parse_view(src)
        yield tuple(t for t in get_tokens_from_view(d))


# ...and there :)
def arg_eq_arg(arg_with_value: str):
    if '=' in arg_with_value:
        arg = arg_with_value.split('=')[0]
        return arg + '=' + arg
    return arg_with_value


# ...and elsewhere
def get_tokens(view_tokens: tuple, element_tokens: dict):
    def list_of_elements_tokens(e_t, e):
        try:
            for key, val in e_t.items():
                # print(val)
                if key == e:
                    for method in val:
                        result = []
                        method_name, *args = method
                        result.append(method_name)
                        result.append(', '.join(args))
                        result.append(', '.join([arg_eq_arg(a) for a in args]))
                        # print(f'List of elements tokens of {e}: {result}')
                        yield result
        except KeyError:
            print("No such key in element tokens dict!")

    for view_t in view_tokens:
        cls_name, last_cls_name, func_name = view_t[:3]
        for m in list_of_elements_tokens(element_tokens, view_t[-1]):
            desirable_token = (cls_name, last_cls_name, func_name, *m)
            yield desirable_token


# New view tokens:
# ('ViewTwo.SecondSubView.SecondLevelOfSecondSubView', 'SecondLevelOfSecondSubView', 'tenth', 'ElementTwo')
# New element tokens:
# {'ElementTwo': {'input': ['value=None', 'length=10'], 'clear': [], 'update': []}}

# Old element parsing result:
# [{'name': 'method_name', 'args': [], 'args_in': []}]

# Desirable Token:
# ['cls_name: Full.Name.Of.Class.In.View',
# 'last_cls_name: view',
# 'func_name: element_name_in_view',
# 'action: element_method',
# 'args: arg=value',
# 'args_in: arg=arg']
if __name__ == "__main__":
    e_folder = '.\\elements'
    v_folder = '.\\views'

    v_file = '.\\views\\view_two.py'
    e_file = '.\\elements\\element_main.py'

    v = parse_views(v_file)
    e = parse_elements(e_folder, e_file)
    for vl in v:
        for t in get_tokens(vl, e):
            print(t)
