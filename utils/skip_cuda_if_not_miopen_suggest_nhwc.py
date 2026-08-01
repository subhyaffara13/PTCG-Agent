
def skipCUDAIfNotMiopenSuggestNHWC(fn):
    return skipCUDAIf(
        not TEST_WITH_MIOPEN_SUGGEST_NHWC,
        "test doesn't currently work without MIOpen NHWC activation",
    )(fn)

