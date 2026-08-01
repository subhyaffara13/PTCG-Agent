
def imagemath_notequal(self: _Operand, other: _Operand | float | None) -> _Operand:
    return self.apply("ne", self, other, mode="I")

