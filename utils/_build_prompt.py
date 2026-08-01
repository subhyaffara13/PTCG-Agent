
def _build_prompt(
    text: str,
    suffix: str,
    show_default: bool | str = False,
    default: t.Any | None = None,
    show_choices: bool = True,
    type: ParamType[t.Any] | None = None,
) -> str:
    prompt = text
    if type is not None and show_choices and isinstance(type, Choice):
        prompt += f" ({', '.join(map(str, type.choices))})"
    if isinstance(show_default, str):
        default = f"({show_default})"
    if default is not None and show_default:
        prompt = f"{prompt} [{_format_default(default)}]"
    return f"{prompt}{suffix}"

