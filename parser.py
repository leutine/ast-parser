# coding: utf-8

import ast
import os

from jinja2 import Environment, FileSystemLoader


class Token:
    def __init__(self, view_class, last_level_view, element, element_method, args_def, args_impl):
        self.view_class = view_class
        self.last_level_view = last_level_view
        self.element = element
        self.element_method = element_method
        self.args_def = args_def
        self.args_impl = args_impl

        # print('Token: ', self.__dict__)


def source(path):
    """
    source(path): read file or folder of files to get AST of module
    :param path: path to file or folder with .py modules to parse
    :return: yields parsed Abstract Syntax Tree
    """

    def read(filename):
        with open(filename, encoding='utf-8') as file:
            return ''.join(file.readlines())

    def asted_code(filename):
        code = read(filename)
        if code:
            yield ast.parse(code)

    if os.path.isdir(path):
        for f in os.listdir(path):
            if '__' not in f:
                yield from asted_code(os.path.join(path, f))
    else:
        yield from asted_code(path)


def get_default_arg_value(d):
    if isinstance(d, ast.NameConstant):
        return str(d.value)
    elif isinstance(d, ast.Num):
        return str(d.n)
    elif isinstance(d, ast.Str):
        return f"'{d.s}'"


def arguments_of(node):
    arguments = node.args
    args_list = [a.arg for a in arguments.args if 'self' not in a.arg]
    defaults_list = [get_default_arg_value(d) for d in arguments.defaults]
    len_diff = len(args_list) - len(defaults_list)
    args = args_list[:len_diff]
    for a, d in zip(args_list[len_diff:], defaults_list):
        args.append(f"{a}={d}")
    return args


def is_parsed_element(node):
    return any(isinstance(n, ast.Name) and n.id == 'parse' for n in node.decorator_list)


def is_parsed_method(node):
    return isinstance(node, ast.FunctionDef) and not node.name.startswith('_')


def parse_element(code):
    out = {}

    classes = [node for node in ast.walk(code) if isinstance(node, ast.ClassDef) and is_parsed_element(node)]

    for c in classes:
        methods = {node.name: arguments_of(node) for node in ast.walk(c) if is_parsed_method(node)}
        out[c.name] = {**methods}

    return out


def parse_view(code):
    def parse(baseclass, prev_name):
        d = {}
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
    out = {base_c.name: parse(base_c, base_c.name)}

    return out


def get_tokens_from_view(parsed_dict):
    for key, value in parsed_dict.items():
        if type(value) is dict:
            for k1, v1 in value.items():
                if type(v1) is list:
                    for assign in v1:
                        yield (key, key.split('.')[-1], assign[0], assign[1])
                elif type(v1) is dict:
                    yield from get_tokens_from_view(v1)


def get_tokens_from_elements(parsed_dict):
    for key, value in parsed_dict.items():
        if type(value) is dict:
            for key1, value1 in value.items():
                yield (key1, *value1)


# Some terrible code here...
def parse_elements(folder, main_el):
    d1 = {}
    m = list(get_tokens_from_elements(parse_element(next(source(main_el)))))

    for src in source(folder):
        if src is not None:
            if parse_element(src):
                d = parse_element(src)
                element_methods = list(get_tokens_from_elements(d))
                if element_methods == m:
                    continue
                d1.update({list(d.keys())[0]: element_methods + m})
    return d1


def parse_views(folder):
    for src in source(folder):
        if src is not None:
            d = parse_view(src)
            yield tuple(get_tokens_from_view(d))


# ...and here :)
def arg_eq_arg(arg_with_value: str):
    if '=' in arg_with_value:
        arg = arg_with_value.split('=')[0]
        return arg + '=' + arg
    return arg_with_value


# ...but mostly HERE
def get_tokens(view_tokens: tuple, element_tokens: dict):
    def get_element_method_and_args(element_token, element_name):
        try:
            for key, val in element_token.items():
                if key == element_name:
                    for method in val:
                        result = []
                        method_name, *args = method
                        result.append(method_name)
                        result.append(', '.join(args))
                        result.append(', '.join([arg_eq_arg(a) for a in args]))
                        # print(f"Method of {element_name}: {result}")
                        yield result
        except KeyError:
            print("No such key in element tokens dict!")

    for view_t in view_tokens:
        cls_name, last_cls_name, func_name = view_t[:3]
        for m in get_element_method_and_args(element_tokens, view_t[-1]):
            desired_token = (cls_name, last_cls_name, func_name, *m)
            yield desired_token


def run():
    list_tokens = []
    for vl in v:
        for t in get_tokens(vl, e):
            name = t[0].split('.')[0]
            list_tokens.append(Token(*t))

            output_from_parsed_template = template.render(**{'tokens': list_tokens, 'view_class': name})

            # print(output_from_parsed_template)

            with open(f"{a_folder}/{name}Action.py", "w+", encoding='utf-8') as action_file:
                action_file.write(output_from_parsed_template)

        list_tokens.clear()
    print("Parsing complete!")


if __name__ == "__main__":
    e_folder = '.\\elements'
    v_folder = '.\\views'
    a_folder = '.\\actions'
    t_folder = '.\\templates'

    main_element = '.\\elements\\element_main.py'

    v = parse_views(v_folder)
    e = parse_elements(e_folder, main_element)

    env = Environment(loader=FileSystemLoader(t_folder))
    template = env.get_template('default.tpl')

    run()
