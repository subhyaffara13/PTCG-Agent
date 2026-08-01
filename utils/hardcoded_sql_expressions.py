
def hardcoded_sql_expressions(context):
    execute_call, statement, str_replace = _evaluate_ast(context.node)
    if _check_string(statement):
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=(
                bandit.MEDIUM
                if execute_call and not str_replace
                else bandit.LOW
            ),
            cwe=issue.Cwe.SQL_INJECTION,
            text="Possible SQL injection vector through string-based "
            "query construction.",
        )

