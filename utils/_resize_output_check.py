
def _resize_output_check(out: TensorLikeType, shape: ShapeType):
    # If the shapes are correct there's nothing to do
    if utils.same_shape(out.shape, shape):
        return False
    if out.numel() != 0:
        msg = (
            f"An output with one or more elements was resized since it had shape {str(out.shape)} "
            "which does not match the required output shape {str(shape)}. "
            "This behavior is deprecated, and in a future PyTorch release outputs will not "
            "be resized unless they have zero elements. "
            "You can explicitly reuse an out tensor t by resizing it, inplace, to zero elements with t.resize_(0)."
        )
        warnings.warn(msg, stacklevel=2)
    return True

