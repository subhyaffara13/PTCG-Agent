
def lower_inline_asm_elementwise(
    *inputs, asm_str, constraints, dtype, is_pure=True, pack=1
):
    inputs = broadcast_tensors(*inputs)

    input_dtypes = tuple(inp.get_dtype() for inp in inputs)
    loaders = [inp.make_loader() for inp in inputs]

    def inner_fn(idx):
        vals = tuple(loader(idx) for loader in loaders)
        result = ops.inline_asm_elementwise(
            *vals,
            asm=asm_str,
            constraints=constraints,
            dtype=dtype,
            is_pure=is_pure,
            pack=pack,
            input_dtypes=input_dtypes,
        )
        # Inductor computes in fp32 for bf16/fp16. Upcast so fused downstream
        # ops (reductions, etc.) see fp32 values. The Pointwise's storage dtype
        # handles the final downcast on store.
        if dtype in (torch.float16, torch.bfloat16):
            result = ops.to_dtype(result, torch.float32)
        return result

    return ir.Pointwise.create(
        device=inputs[0].get_device(),
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=list(inputs[0].get_size()),
    )

