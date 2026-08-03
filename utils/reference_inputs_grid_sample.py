import itertools

def reference_inputs_grid_sample(op_info, device, dtype, requires_grad, **kwargs):

    batch_size = 2
    num_channels = 3
    height = 345
    width = 456
    modes = ("bilinear", "nearest", "bicubic")
    align_cornerss = (False, True)
    padding_modes = ('zeros', 'border', 'reflection')

    # Create an affine transformation matrix
    a = torch.deg2rad(torch.tensor(45.0))
    ca, sa = torch.cos(a), torch.sin(a)  # rotation angles
    s1, s2 = 1.23, 1.34  # scales

    theta = torch.tensor([[
        [ca / s1, sa, 0.0],
        [-sa, ca / s2, 0.0],
    ]], dtype=dtype, device=device)
    theta = theta.expand(batch_size, 2, 3).contiguous()

    x = torch.arange(batch_size * num_channels * height * width, device=device)
    x = x.reshape(batch_size, num_channels, height, width).to(torch.uint8)
    x = x.to(dtype=dtype)
    x.requires_grad_(requires_grad)

    for mode, padding_mode, align_corners in itertools.product(modes, padding_modes, align_cornerss):
        grid = torch.nn.functional.affine_grid(
            theta, size=(batch_size, num_channels, height, width), align_corners=align_corners
        )
        yield SampleInput(
            x,
            grid,
            mode,
            padding_mode,
            align_corners,
        )

