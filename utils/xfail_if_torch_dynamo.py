
def xfailIfTorchDynamo(func):
    return unittest.expectedFailure(func) if TEST_WITH_TORCHDYNAMO else func

