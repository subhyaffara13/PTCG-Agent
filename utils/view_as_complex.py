
def view_as_complex(self: TensorLikeType) -> TensorLikeType:
    input_dtype = self.dtype
    torch._check(
        utils.is_float_dtype(input_dtype),
        lambda: f"view_as_complex is only supported for floating point"
        f"tensors, but got a tensor of scalar type: {input_dtype}",
    )
    sizes = self.size()
    torch._check(
        len(sizes) != 0,
        lambda: "Input tensor must have one or more dimensions",
    )
    torch._check(
        sizes[-1] == 2,
        lambda: "Tensor must have a last dimension of size 2",
    )

    old_strides = self.stride()
    torch._check(
        old_strides[-1] == 1,
        lambda: "Tensor must have a last dimension with stride 1",
    )
    dims = old_strides[:-1]
    torch._check(
        builtins.all(stride % 2 == 0 for stride in dims),
        lambda: "Tensor must have a stride divisible by 2 for all but last dimension",
    )
    torch._check(
        self.storage_offset() % 2 == 0,
        lambda: "Tensor must have a storage_offset divisible by 2",
    )
    return prims.view_element_type(
        self, utils.corresponding_complex_dtype(input_dtype)
    ).squeeze(-1)

