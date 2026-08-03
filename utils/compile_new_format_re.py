import re

def compile_new_format_re(custom_spec: bool) -> Pattern[str]:
    """Construct regexps to match format conversion specifiers in str.format() calls.

    See After https://docs.python.org/3/library/string.html#formatspec for
    specifications. The regexps are intentionally wider, to report better errors,
    instead of just not matching.
    """

    # Field (optional) is an integer/identifier possibly followed by several .attr and [index].
    field = r"(?P<field>(?P<key>[^.[!:]*)([^:!]+)?)"

    # Conversion (optional) is ! followed by one of letters for forced repr(), str(), or ascii().
    conversion = r"(?P<conversion>![^:])?"

    # Format specification (optional) follows its own mini-language:
    if not custom_spec:
        # Fill and align is valid for all builtin types.
        fill_align = r"(?P<fill_align>.?[<>=^])?"
        # Number formatting options are only valid for int, float, complex, and Decimal,
        # except if only width is given (it is valid for all types).
        # This contains sign, flags (sign, # and/or 0), width, grouping (_ or ,) and precision.
        num_spec = r"(?P<flags>[+\- ]?#?0?)(?P<width>\d+)?[_,]?(?P<precision>\.\d+)?"
        # The last element is type.
        conv_type = r"(?P<type>.)?"  # only some are supported, but we want to give a better error
        format_spec = r"(?P<format_spec>:" + fill_align + num_spec + conv_type + r")?"
    else:
        # Custom types can define their own form_spec using __format__().
        format_spec = r"(?P<format_spec>:.*)?"

    return re.compile(field + conversion + format_spec)

