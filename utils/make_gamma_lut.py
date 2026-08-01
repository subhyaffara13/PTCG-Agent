
def make_gamma_lut(exp: float) -> list[int]:
    return [int(((i / 255.0) ** exp) * 255.0 + 0.5) for i in range(256)]

