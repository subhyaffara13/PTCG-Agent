
def _hashlib_func(context, func):
    keywords = context.call_keywords

    if func in WEAK_HASHES:
        if keywords.get("usedforsecurity", "True") == "True":
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.BROKEN_CRYPTO,
                text=f"Use of weak {func.upper()} hash for security. "
                "Consider usedforsecurity=False",
                lineno=context.node.lineno,
            )
    elif func == "new":
        args = context.call_args
        name = args[0] if args else keywords.get("name", None)
        if isinstance(name, str) and name.lower() in WEAK_HASHES:
            if keywords.get("usedforsecurity", "True") == "True":
                return bandit.Issue(
                    severity=bandit.HIGH,
                    confidence=bandit.HIGH,
                    cwe=issue.Cwe.BROKEN_CRYPTO,
                    text=f"Use of weak {name.upper()} hash for "
                    "security. Consider usedforsecurity=False",
                    lineno=context.node.lineno,
                )

