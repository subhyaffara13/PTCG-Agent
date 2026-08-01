
def xpassIfTorchDynamo_np(func):
    # numpy 2.0+ is causing issues
    if TEST_WITH_TORCHDYNAMO and np.__version__[0] == '2':
        return unittest.skip("skipping numpy 2.0+ dynamo-wrapped test")(func)
    return func if TEST_WITH_TORCHDYNAMO else unittest.expectedFailure(func)

