
def load_verifier(dialect: str) -> type[Verifier]:
    if dialect == "ATEN" or dialect == "":
        return _VerifierMeta._registry.get(dialect, Verifier)
    return _VerifierMeta._registry[dialect]

