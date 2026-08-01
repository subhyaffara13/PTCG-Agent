
def expectedFailureMeta(fn):
    return skipIfTorchDynamo()(expectedFailure("meta")(fn))

