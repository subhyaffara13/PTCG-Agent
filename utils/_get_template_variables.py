
def _get_template_variables(chat_template: str | None) -> frozenset[str]:
    """Return the set of undeclared variables referenced by a chat template.

    Uses ``jinja2.meta.find_undeclared_variables`` so that callers can
    automatically distinguish template-level kwargs from processor kwargs
    without maintaining a manual allowlist. Needed only to support BC as we
    allowed all `kwargs` to be merged into one in the past
    """
    if chat_template is None:
        return frozenset()
    compiled = _compile_jinja_template(chat_template)
    ast = compiled.environment.parse(chat_template)
    return frozenset(jinja2.meta.find_undeclared_variables(ast))

