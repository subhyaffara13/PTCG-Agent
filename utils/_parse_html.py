
def _parse_html(to_parse: bool, input_text: str) -> str:
    if not to_parse:
        return input_text
    from . import rich_utils

    return rich_utils.rich_to_html(input_text)

