# coding: utf-8

from ..views import {{filename}}View


class {{filename}}Action:{% if tokens %}{% for token in tokens %}
    @staticmethod
    def {{token.element_method}}_{{token.last_level_view}}_{{token.element}}({{token.args_def}}):
        return {{token.view}}.{{token.element}}.{{token.element_method}}({{token.args_impl}})
    {% endfor %}
    {% else %}
    ...
    {% endif %}