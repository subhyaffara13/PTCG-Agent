
def parse_css_declarations(style_attr: str) -> Dict[str, str]:
    # https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/style
    # https://developer.mozilla.org/en-US/docs/Web/CSS/Syntax#css_declarations
    result = {}
    for declaration in style_attr.split(";"):
        if declaration.count(":") == 1:
            property_name, value = declaration.split(":")
            property_name = property_name.strip()
            result[property_name] = value.strip()
        elif declaration.strip():
            raise ValueError(f"Invalid CSS declaration syntax: {declaration}")
    return result

