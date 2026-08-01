
def parse_format_value(
    format_value: str, ctx: Context, msg: MessageBuilder, nested: bool = False
) -> list[ConversionSpecifier] | None:
    """Parse format string into list of conversion specifiers.

    The specifiers may be nested (two levels maximum), in this case they are ordered as
    '{0:{1}}, {2:{3}{4}}'. Return None in case of an error.
    """
    top_targets = find_non_escaped_targets(format_value, ctx, msg)
    if top_targets is None:
        return None

    result: list[ConversionSpecifier] = []
    for target, start_pos in top_targets:
        match = FORMAT_RE_NEW.fullmatch(target)
        if match:
            conv_spec = ConversionSpecifier(match, start_pos=start_pos)
        else:
            custom_match = FORMAT_RE_NEW_CUSTOM.fullmatch(target)
            if custom_match:
                conv_spec = ConversionSpecifier(
                    custom_match, start_pos=start_pos, non_standard_format_spec=True
                )
            else:
                msg.fail(
                    "Invalid conversion specifier in format string",
                    ctx,
                    code=codes.STRING_FORMATTING,
                )
                return None

        if conv_spec.key and ("{" in conv_spec.key or "}" in conv_spec.key):
            msg.fail("Conversion value must not contain { or }", ctx, code=codes.STRING_FORMATTING)
            return None
        result.append(conv_spec)

        # Parse nested conversions that are allowed in format specifier.
        if (
            conv_spec.format_spec
            and conv_spec.non_standard_format_spec
            and ("{" in conv_spec.format_spec or "}" in conv_spec.format_spec)
        ):
            if nested:
                msg.fail(
                    "Formatting nesting must be at most two levels deep",
                    ctx,
                    code=codes.STRING_FORMATTING,
                )
                return None
            sub_conv_specs = parse_format_value(conv_spec.format_spec, ctx, msg, nested=True)
            if sub_conv_specs is None:
                return None
            result.extend(sub_conv_specs)
    return result

