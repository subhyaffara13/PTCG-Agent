
def django_rawsql_used(context):
    """**B611: Potential SQL injection on RawSQL function**

    :Example:

    .. code-block:: none

        >> Issue: [B611:django_rawsql_used] Use of RawSQL potential SQL attack vector.
           Severity: Medium Confidence: Medium
           CWE: CWE-89 (https://cwe.mitre.org/data/definitions/89.html)
           Location: examples/django_sql_injection_raw.py:11:26
           More Info: https://bandit.readthedocs.io/en/latest/plugins/b611_django_rawsql_used.html
        10        ' WHERE "username"="admin" OR 1=%s --'
        11  User.objects.annotate(val=RawSQL(raw, [0]))

    .. seealso::

     - https://docs.djangoproject.com/en/dev/topics/security/\
#sql-injection-protection
     - https://cwe.mitre.org/data/definitions/89.html

    .. versionadded:: 1.5.0

    .. versionchanged:: 1.7.3
        CWE information added

    """  # noqa: E501
    description = "Use of RawSQL potential SQL attack vector."
    if context.is_module_imported_like("django.db.models"):
        if context.call_function_name == "RawSQL":
            if context.node.args:
                sql = context.node.args[0]
            else:
                kwargs = keywords2dict(context.node.keywords)
                sql = kwargs["sql"]

            if not (
                isinstance(sql, ast.Constant) and isinstance(sql.value, str)
            ):
                return bandit.Issue(
                    severity=bandit.MEDIUM,
                    confidence=bandit.MEDIUM,
                    cwe=issue.Cwe.SQL_INJECTION,
                    text=description,
                )

