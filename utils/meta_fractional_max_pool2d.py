
def meta_fractional_max_pool2d(self, kernel_size, output_size, random_samples):
    torch._check(
        self.ndim in (3, 4),
        lambda: f"fractional_max_pool2d: Expected 3D or 4D tensor, but got: {self.ndim}",
    )
    ndim = self.ndim

    for d in range(ndim - 3, ndim):
        torch._check(
            self.size(d) > 0,
            lambda: f"fractional_max_pool2d: Expected input to have non-zero "
            f" size for non-batch dimensions, but got {self.size()} with dimension {d} empty",
        )

    # the check and message are out of sync, but this matches the structured meta
    torch._check(
        len(kernel_size) == 2,
        lambda: "fractional_max_pool2d: kernel_size must"
        "either be a single int or tuple of Ints",
    )
    torch._check(
        len(output_size) == 2,
        lambda: "fractional_max_pool2d: output_size must "
        "either be a single int or tuple of Ints",
    )

    input_channels = self.size(-3)
    input_height = self.size(-2)
    input_width = self.size(-1)
    if ndim == 4:
        input_batch = self.size(0)
    else:
        input_batch = 1

    torch._check(
        self.dtype == random_samples.dtype,
        lambda: "Expect _random_samples to have the same dtype as input",
    )
    torch._check(
        random_samples.ndim == 3,
        lambda: f"Expect _random samples to have 3 dimensions got, {random_samples.ndim}",
    )

    n = random_samples.size(0)
    c = random_samples.size(1)
    d = random_samples.size(2)
    torch._check(
        n >= input_batch,
        lambda: "Expect _random_samples.size(0) no less then input batch size.",
    )
    torch._check(
        c == input_channels,
        lambda: "Expect _random_samples.size(1) equals to input channel size.",
    )
    torch._check(d == 2, lambda: f"Expect _random_samples.size(2) equals to 2 got {d}.")

    torch._check(
        output_size[0] + kernel_size[0] - 1 <= input_height,
        lambda: f"fractional_max_pool2d: kernel height {kernel_size[0]} is too large relative to input height {input_height}",
    )
    torch._check(
        output_size[1] + kernel_size[1] - 1 <= input_width,
        lambda: f"fractional_max_pool2d: kernel width {kernel_size[1]} is too large relative to input width {input_width}",
    )

    if self.dim() == 4:
        size = [input_batch, input_channels, output_size[0], output_size[1]]
    else:
        size = [input_channels, output_size[0], output_size[1]]

    return (
        torch.empty(
            size,
            dtype=self.dtype,
            device=self.device,
        ),
        torch.empty(
            size,
            dtype=torch.int64,
            device=self.device,
        ),
    )

