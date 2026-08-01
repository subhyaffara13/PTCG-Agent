
def load_tensor_reader(loc: str) -> Generator[None, None, None]:
    global LOAD_TENSOR_READER
    if LOAD_TENSOR_READER is not None:
        raise AssertionError("LOAD_TENSOR_READER is already set")
    # load_tensor is an "op", and we will play merry hell on
    # Inductor's memory planning if we return a tensor that
    # aliases another tensor that we previously returned from
    # an operator.  So unlike standard ContentStoreReader use,
    # we disable the cache so that you always get fresh storages
    # (no aliasing for you!)
    LOAD_TENSOR_READER = ContentStoreReader(loc, cache=False)
    try:
        yield
    finally:
        LOAD_TENSOR_READER = None

