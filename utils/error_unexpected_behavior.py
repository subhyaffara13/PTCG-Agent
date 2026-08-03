from typing import Union

def error_unexpected_behavior(
    detail: str, api: CheckerPluginInterface | SemanticAnalyzerPluginInterface, context: Context
) -> None:  # pragma: no cover
    """Emits unexpected behavior error."""
    # Can't think of a good way to test this, but I confirmed it renders as desired by adding to a non-error path
    link = 'https://github.com/pydantic/pydantic/issues/new/choose'
    full_message = f'The pydantic mypy plugin ran into unexpected behavior: {detail}\n'
    full_message += f'Please consider reporting this bug at {link} so we can try to fix it!'
    api.fail(full_message, context, code=ERROR_UNEXPECTED)


def error_unexpected_behavior(
    detail: str, api: Union[CheckerPluginInterface, SemanticAnalyzerPluginInterface], context: Context
) -> None:  # pragma: no cover
    # Can't think of a good way to test this, but I confirmed it renders as desired by adding to a non-error path
    link = 'https://github.com/pydantic/pydantic/issues/new/choose'
    full_message = f'The pydantic mypy plugin ran into unexpected behavior: {detail}\n'
    full_message += f'Please consider reporting this bug at {link} so we can try to fix it!'
    api.fail(full_message, context, code=ERROR_UNEXPECTED)

