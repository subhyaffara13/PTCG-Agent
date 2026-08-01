
def test_maybe_mangle_lambdas_passthrough():
    assert maybe_mangle_lambdas("mean") == "mean"
    assert maybe_mangle_lambdas(lambda x: x).__name__ == "<lambda>"
    # don't mangle single lambda.
    assert maybe_mangle_lambdas([lambda x: x])[0].__name__ == "<lambda>"

