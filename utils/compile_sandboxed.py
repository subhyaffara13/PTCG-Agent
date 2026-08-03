from typing import Any

def compile_sandboxed(source: str, filename: str = "<guardrail>") -> Any:
    """Compile guardrail source with RestrictedPython's AST transformer.

    Raises ``SyntaxError`` on either a Python syntax error or a restricted
    construct (import, exec, dunder name, etc.).
    """
    return compile_restricted(
        source=source,
        filename=filename,
        mode="exec",
        policy=AsyncAwareTransformer,
    )

