
def as_strided_scatter(self, src, size, stride, storage_offset=None):
    output = clone(self)
    output_view = as_strided(output, size, stride, storage_offset)
    copy_(output_view, src)
    return output


def as_strided_scatter(
    input: TensorLikeType,
    src: TensorLikeType,
    size: ShapeType,
    stride: StrideType,
    storage_offset: int | None = None,
) -> TensorLikeType:
    storage_offset_int = 0 if storage_offset is None else storage_offset
    return prims.as_strided_scatter(input, src, size, stride, storage_offset_int)

