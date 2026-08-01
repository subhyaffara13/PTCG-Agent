
def _verify_batch_size(size: list[int]) -> None:
    # XXX: JIT script does not support the reduce from functools, and mul op is a
    # builtin, which cannot be used as a value to a func yet, so rewrite this size
    # check to a simple equivalent for loop
    #
    # TODO: make use of reduce like below when JIT is ready with the missing features:
    # from operator import mul
    # from functools import reduce
    #
    #   if reduce(mul, size[2:], size[0]) == 1
    size_prods = size[0]
    for i in range(len(size) - 2):
        size_prods *= size[i + 2]
    if size_prods == 1:
        raise ValueError(
            f"Expected more than 1 value per channel when training, got input size {size}"
        )

