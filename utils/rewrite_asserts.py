
def rewrite_asserts(
    mod: ast.Module,
    source: bytes,
    module_path: str | None = None,
    config: Config | None = None,
) -> None:
    """Rewrite the assert statements in mod."""
    AssertionRewriter(module_path, config, source).run(mod)

