
def _flatdim_box_multibinary(space: Box | MultiBinary) -> int:
    return reduce(op.mul, space.shape, 1)


def _flatdim_box_multibinary(space: Union[Box, MultiBinary]) -> int:
    return reduce(op.mul, space.shape, 1)

