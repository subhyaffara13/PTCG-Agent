
def is_divisible_by(divisor: int | float):
    @as_validated_field
    def _inner(value: int | float):
        if value % divisor != 0:
            raise ValueError(f"Value has to be divisble by {divisor} but got value={value}")

    return _inner

