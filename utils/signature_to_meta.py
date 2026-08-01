
def signature_to_meta(
    signature: list[KernelArgType],
    *,
    size_dtype: str | None,
    argdefs: list[ArgName],
    indices: list[int] | None = None,
    is_template: bool = False,
) -> dict[str, str]:
    if indices is None:
        indices = list(range(len(signature)))

    def _decide_tl_dtype(arg):
        # Even if the ks0 symbol itself is within tl.int32 range, it's
        # risky to use tl.int32 dtype since we may have ks0*ks1 later
        # for kernels like torch.mean when dynamic shape is enabled.
        #
        # Check config.triton.use_block_ptr, since Triton block pointer
        # does not support 64bit indexing:
        # https://gist.github.com/shunting314/6a41c776171720ce4561f202dcde0ad6
        #
        # If the triton metadata is for a template, don't use tl.int64 index.
        # Templates like flex attention/decoding uses block pointers which
        # does not support 64 bit indexing.
        if (
            not config.triton.use_block_ptr
            and not is_template
            and isinstance(arg, SizeArg)
            and arg.name.startswith("ks")
        ):
            return "tl.int64"
        return size_dtype

    return {
        argdefs[i].name: signature_of(arg, size_dtype=_decide_tl_dtype(arg))
        for i, arg in zip(indices, signature)
    }

