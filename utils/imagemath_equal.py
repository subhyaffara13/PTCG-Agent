
def imagemath_equal(self: _Operand, other: _Operand | float | None) -> _Operand:
    return self.apply("eq", self, other, mode="I")

