
def imagemath_min(self: _Operand, other: _Operand | float | None) -> _Operand:
    return self.apply("min", self, other)

