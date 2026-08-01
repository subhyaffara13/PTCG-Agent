
def imagemath_convert(self: _Operand, mode: str) -> _Operand:
    return _Operand(self.im.convert(mode))

