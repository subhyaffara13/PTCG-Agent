
def get_assertion_text_diff_style(config: Config) -> _AssertionTextDiffStyle:
    style = str(config.getini(ASSERTION_TEXT_DIFF_STYLE_INI))
    match style:
        case "ndiff" | "block":
            return style
        case _:
            choices = ", ".join(
                repr(choice) for choice in ASSERTION_TEXT_DIFF_STYLE_CHOICES
            )
            raise UsageError(
                f"{ASSERTION_TEXT_DIFF_STYLE_INI} must be one of {choices}; got {style!r}"
            )

