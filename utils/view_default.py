
def view_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    size = new_kwargs.pop("size")

    if inp._ragged_idx != 1 and tuple(inp._size) != tuple(size):
        raise RuntimeError(
            f"view(): does not support ragged_idx != 1 except when inp._size == size. "
            f"inp._size is ({inp._size}) and size is ({size})."
        )

    # Ensure specified size still includes batch and ragged dims
    if len(size) < 3 or not raggedness_matches(inp, size):
        raise RuntimeError(f"view(): cannot view shape {inp._size} as {size}")

    # outer size: the size of the NT, e.g. [3, j0, 10]
    # inner size: the size of the values, e.g. [8, 10] (e.g. for offsets = [0, 3, 5, 8])
    # this function gets inner_size[inner_idx] for a given inner_idx.
    #
    # example: for outer size [a, b, c, j0, d, e, f]
    #                         assume that j0 is ragged, other are concrete integers
    #                         and ragged_idx=3
    # inner size will be      [b, c, inp._values.size(ragged_idx), d, e, f]
    # therefore:
    #    inner_size[0] = outer_size[1]
    #    inner_size[1] = outer_size[2]
    #    inner_size[0] = inp._values.size(ragged_idx - 1)
    #    inner_size[3] = outer_size[4]
    #    inner_size[4] = outer_size[5]
    def get_inner_size(inner_idx):
        nonlocal inp, size
        if inner_idx == inp._ragged_idx - 1:
            return inp._values.size(inner_idx)
        else:
            return size[inner_idx + 1]

    inner_size = [get_inner_size(i) for i in range(len(size) - 1)]

    # Preserve inference-mode-ness of input.
    # TODO: Do this for all other views!
    with torch.inference_mode(inp.is_inference()):
        return NestedTensor(func(inp._values, inner_size), **extract_kwargs(inp))

