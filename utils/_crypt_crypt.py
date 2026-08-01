
def _crypt_crypt(context, func):
    args = context.call_args
    keywords = context.call_keywords

    if func == "crypt":
        name = args[1] if len(args) > 1 else keywords.get("salt", None)
        if isinstance(name, str) and name in WEAK_CRYPT_HASHES:
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.BROKEN_CRYPTO,
                text=f"Use of insecure crypt.{name.upper()} hash function.",
                lineno=context.node.lineno,
            )
    elif func == "mksalt":
        name = args[0] if args else keywords.get("method", None)
        if isinstance(name, str) and name in WEAK_CRYPT_HASHES:
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.HIGH,
                cwe=issue.Cwe.BROKEN_CRYPTO,
                text=f"Use of insecure crypt.{name.upper()} hash function.",
                lineno=context.node.lineno,
            )

