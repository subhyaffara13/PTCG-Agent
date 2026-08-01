
def _validate_size(size: SizeDict) -> None:
    if not (size.height and size.width):
        raise ValueError(f"Argument `size` must be a dictionary with keys 'height' and 'width'. Got: {size}")
    if size.height != size.width:
        raise ValueError(f"Argument `size` must have the same height and width, got {size}")


def _validate_size(size: SizeDict) -> None:
    if not (size.height and size.width):
        raise ValueError(f"Argument `size` must be a dictionary with keys 'height' and 'width'. Got: {size}")
    if size.height != size.width:
        raise ValueError(f"Argument `size` must have the same height and width, got {size}")

