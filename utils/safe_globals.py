
def safe_globals():
    """
    Context manager to allowlist numpy objects for torch.load with weights_only=True.

    Starting from version 2.4 PyTorch introduces a check for the objects loaded
    with torch.load(weights_only=True). Starting from 2.6 weights_only=True becomes
    a default and requires allowlisting of objects being loaded.

    See: https://github.com/pytorch/pytorch/pull/137602
    See: https://pytorch.org/docs/stable/notes/serialization.html#torch.serialization.add_safe_globals
    See: https://github.com/huggingface/accelerate/pull/3036
    """
    if version.parse(torch.__version__).release < version.parse("2.6").release:
        return contextlib.nullcontext()

    np_core = np._core if version.parse(np.__version__) >= version.parse("2.0.0") else np.core
    allowlist = [np_core.multiarray._reconstruct, np.ndarray, np.dtype]
    # numpy >1.25 defines numpy.dtypes.UInt32DType, but below works for
    # all versions of numpy
    allowlist += [type(np.dtype(np.uint32))]

    return torch.serialization.safe_globals(allowlist)

