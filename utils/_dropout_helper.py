
def _dropout_helper(
    self: TensorLikeType,
    val: float,
) -> TensorLikeType:
    """
    Helper function for all dropout-type operators. During training,
    some of the elements of the input tensor are randomly masked.

    Returns the masked tensor of the boolean values.

    """

    return (
        refs._uniform_helper(
            self.shape,
            low=0.0,
            high=1.0,
            dtype=torch.float32,
            device=self.device,
            stride=self.stride(),
        )
        < val
    )

