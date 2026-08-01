
def imagemath_max(self: _Operand, other: _Operand | float | None) -> _Operand:
    return self.apply("max", self, other)

