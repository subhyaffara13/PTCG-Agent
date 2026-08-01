
def imagemath_float(self: _Operand) -> _Operand:
    return _Operand(self.im.convert("F"))

