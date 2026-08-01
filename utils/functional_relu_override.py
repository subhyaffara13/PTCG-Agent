
def functional_relu_override(x, inplace=False):
    if inplace:
        raise AssertionError(
            "dont support inplace functional.relu for metatensor analysis"
        )
    return x

