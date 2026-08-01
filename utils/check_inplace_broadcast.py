
def check_inplace_broadcast(self_shape, *args_shape):
    broadcasted_shape = tuple(_broadcast_shapes(self_shape, *args_shape))
    torch._check(
        broadcasted_shape == self_shape,
        lambda: f"output with shape {self_shape} doesn't match the broadcast shape {broadcasted_shape}",
    )

