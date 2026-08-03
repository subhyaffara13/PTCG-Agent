import re

def _trim_zeros_complex(str_complexes: ArrayLike, decimal: str = ".") -> list[str]:
    """
    Separates the real and imaginary parts from the complex number, and
    executes the _trim_zeros_float method on each of those.
    """
    real_part, imag_part = [], []
    for x in str_complexes:
        # Complex numbers are represented as "(-)xxx(+/-)xxxj"
        # The split will give [{"", "-"}, "xxx", "+/-", "xxx", "j", ""]
        # Therefore, the imaginary part is the 4th and 3rd last elements,
        # and the real part is everything before the imaginary part
        trimmed = re.split(r"(?<!e)([j+-])", x)
        real_part.append("".join(trimmed[:-4]))
        imag_part.append("".join(trimmed[-4:-2]))

    # We want to align the lengths of the real and imaginary parts of each complex
    # number, as well as the lengths the real (resp. complex) parts of all numbers
    # in the array
    n = len(str_complexes)
    padded_parts = _trim_zeros_float(real_part + imag_part, decimal)
    if len(padded_parts) == 0:
        return []
    padded_length = max(len(part) for part in padded_parts) - 1
    padded = [
        real_pt  # real part, possibly NaN
        + imag_pt[0]  # +/-
        + f"{imag_pt[1:]:>{padded_length}}"  # complex part (no sign), possibly nan
        + "j"
        for real_pt, imag_pt in zip(padded_parts[:n], padded_parts[n:], strict=True)
    ]
    return padded

