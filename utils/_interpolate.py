from typing import Any, Callable

def _interpolate(name, dim, interpolate_mode):
    @symbolic_helper.quantized_args(True, False, False)
    def symbolic_fn(g, input, output_size, *args):
        scales, align_corners = symbolic_helper._get_interpolate_attributes(
            g, interpolate_mode, args
        )
        symbolic_helper._interpolate_warning(interpolate_mode)
        align_corners = symbolic_helper._maybe_get_scalar(align_corners)
        if align_corners:
            return symbolic_helper._unimplemented(name, "align_corners == True", input)
        if scales is None:
            scales = symbolic_helper._interpolate_size_to_scales(
                g, input, output_size, dim
            )
        return g.op("Resize", input, scales, mode_s=interpolate_mode)

    return symbolic_fn


def _interpolate(name: str, dim: int, interpolate_mode: str):
    return symbolic_helper._interpolate_helper(name, dim, interpolate_mode)


def _interpolate(name, dim, interpolate_mode):
    def symbolic_fn(g, input, output_size, *args):
        scales, align_corners = symbolic_helper._get_interpolate_attributes(
            g, interpolate_mode, args
        )
        symbolic_helper._interpolate_warning(interpolate_mode)
        align_corners = symbolic_helper._maybe_get_scalar(align_corners)
        if align_corners:
            return symbolic_helper._unimplemented(name, "align_corners == True", input)
        output_size = symbolic_helper._maybe_get_const(output_size, "is")
        if symbolic_helper._is_value(output_size):
            return symbolic_helper._unimplemented(
                name, "torch._C.Value (output_size) indexing"
            )
        if scales is None:
            scales = [
                1.0
                if i < 2
                else float(output_size[-(dim - i)])
                / float(input.type().sizes()[-(dim - i)])
                for i in range(dim)
            ]
        return g.op("Upsample", input, mode_s=interpolate_mode, scales_f=scales)

    return symbolic_fn


def _interpolate(name: str, dim: int, interpolate_mode: str):
    def symbolic_fn(g, input, output_size, *args):
        scales, align_corners = symbolic_helper._get_interpolate_attributes(
            g, interpolate_mode, args
        )
        symbolic_helper._interpolate_warning(interpolate_mode)
        align_corners = symbolic_helper._maybe_get_scalar(align_corners)
        if align_corners:
            return symbolic_helper._unimplemented(name, "align_corners == True", input)
        if scales is None:
            scales = symbolic_helper._interpolate_size_to_scales(
                g, input, output_size, dim
            )
        return g.op("Upsample", input, scales, mode_s=interpolate_mode)

    return symbolic_fn


def _interpolate(
    template: str,
    values: Mapping[str, Any],
    quoter: Callable[[str], str],
) -> str:
    """Replace {name} placeholders in `template`, quoting each value with `quoter`.

    Placeholder names are looked up in `values`.

    Raises:
        KeyError: If a placeholder is not found in `values`.
    """
    # re.split with a capturing group returns alternating
    # [text, name, text, name, ..., text] elements.
    parts = _PLACEHOLDER_RE.split(template)

    for i in range(1, len(parts), 2):
        name = parts[i]
        if name not in values:
            raise KeyError(f"a value for placeholder {{{name}}} was not provided")
        val = values[name]
        if val is None:
            parts[i] = "null"
        elif isinstance(val, bool):
            parts[i] = "true" if val else "false"
        else:
            parts[i] = quoter(str(values[name]))

    return "".join(parts)

