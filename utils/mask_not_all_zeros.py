
def mask_not_all_zeros(shape):
    if len(shape) <= 0:
        raise AssertionError(f"Expected len(shape) > 0, got {len(shape)}")
    while True:
        result = torch.randn(shape).gt(0)
        if result.sum() > 0:
            return result

