
def maybe_convert_css_to_tuples(style: CSSProperties) -> CSSList:
    """
    Convert css-string to sequence of tuples format if needed.
    'color:red; border:1px solid black;' -> [('color', 'red'),
                                             ('border','1px solid red')]
    """
    if isinstance(style, str):
        if style and ":" not in style:
            raise ValueError(
                "Styles supplied as string must follow CSS rule formats, "
                f"for example 'attr: val;'. '{style}' was given."
            )
        s = style.split(";")
        return [
            (x.split(":")[0].strip(), ":".join(x.split(":")[1:]).strip())
            for x in s
            if x.strip() != ""
        ]

    return style

