# coding: utf-8

from ..views import {{view_class}}


class {{view_class}}Action:{% if tokens %}{% for token in tokens %}
    @staticmethod
    def {{token.element_method}}_{{token.last_level_view}}_{{token.element}}({{token.args_def}}):
        return {{token.view_class}}.{{token.element}}.{{token.element_method}}({{token.args_impl}})
    {% endfor %}
    {% else %}
    ...
    {% endif %}