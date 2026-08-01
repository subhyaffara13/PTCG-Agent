
def try_except_continue(context, config):
    node = context.node
    if len(node.body) == 1:
        if (
            not config["check_typed_exception"]
            and node.type is not None
            and getattr(node.type, "id", None) != "Exception"
        ):
            return

        if isinstance(node.body[0], ast.Continue):
            return bandit.Issue(
                severity=bandit.LOW,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.IMPROPER_CHECK_OF_EXCEPT_COND,
                text=("Try, Except, Continue detected."),
            )

