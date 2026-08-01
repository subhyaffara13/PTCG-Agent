
def django_mark_safe(context):
    """**B703: Potential XSS on mark_safe function**

    :Example:

    .. code-block:: none

        >> Issue: [B703:django_mark_safe] Potential XSS on mark_safe function.
           Severity: Medium Confidence: High
           CWE: CWE-80 (https://cwe.mitre.org/data/definitions/80.html)
           Location: examples/mark_safe_insecure.py:159:4
           More Info: https://bandit.readthedocs.io/en/latest/plugins/b703_django_mark_safe.html
        158         str_arg = 'could be insecure'
        159     safestring.mark_safe(str_arg)

    .. seealso::

     - https://docs.djangoproject.com/en/dev/topics/security/\
#cross-site-scripting-xss-protection
     - https://docs.djangoproject.com/en/dev/ref/utils/\
#module-django.utils.safestring
     - https://docs.djangoproject.com/en/dev/ref/utils/\
#django.utils.html.format_html
     - https://cwe.mitre.org/data/definitions/80.html

    .. versionadded:: 1.5.0

    .. versionchanged:: 1.7.3
        CWE information added

    """  # noqa: E501
    if context.is_module_imported_like("django.utils.safestring"):
        affected_functions = [
            "mark_safe",
            "SafeText",
            "SafeUnicode",
            "SafeString",
            "SafeBytes",
        ]
        if context.call_function_name in affected_functions:
            xss = context.node.args[0]
            if not (
                isinstance(xss, ast.Constant) and isinstance(xss.value, str)
            ):
                return check_risk(context.node)

