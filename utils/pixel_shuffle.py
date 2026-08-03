import math


def pixel_shuffle(input_tensor, shuffle_ratio):
    # input_tensor: [batch_size, num_patches, channels]
    batch_size, num_patches, channels = input_tensor.shape
    patch_size = int(math.sqrt(num_patches))

    input_tensor = input_tensor.view(batch_size, patch_size, patch_size, -1)
    batch_size, height, width, channels = input_tensor.size()

    reshaped_tensor = input_tensor.view(batch_size, height, int(width * shuffle_ratio), int(channels / shuffle_ratio))
    reshaped_tensor = reshaped_tensor.permute(0, 2, 1, 3).contiguous()

    reshaped_tensor = reshaped_tensor.view(
        batch_size, int(height * shuffle_ratio), int(width * shuffle_ratio), int(channels / (shuffle_ratio**2))
    )
    reshaped_tensor = reshaped_tensor.permute(0, 2, 1, 3).contiguous()

    output_tensor = reshaped_tensor.view(batch_size, -1, reshaped_tensor.shape[-1])
    return output_tensor


def pixel_shuffle(self: Tensor, upscale_factor: int):
    torch._check(
        self.dim() >= 3,
        lambda: f"pixel_shuffle expects input to have at least 3 dimensions, but got input with {self.dim} dimension(s)",
    )
    batch = self.shape[:-3]
    C_out = self.shape[-3] // upscale_factor**2
    HW_out = (self.shape[-2] * upscale_factor, self.shape[-1] * upscale_factor)
    n = len(batch)
    B_dims = range(n)
    C_dim, r1_dim, r2_dim, H_dim, W_dim = range(n, n + 5)
    return (
        self.view(
            *batch,
            C_out,
            upscale_factor,
            upscale_factor,
            self.shape[-2],
            self.shape[-1],
        )
        .permute(*B_dims, C_dim, H_dim, r1_dim, W_dim, r2_dim)
        .reshape(*batch, C_out, *HW_out)
        .clone(memory_format=utils.suggest_memory_format(self))
    )


def pixel_shuffle(g: jit_utils.GraphContext, self, upscale_factor):
    rank = symbolic_helper._get_tensor_rank(self)
    if rank is not None and rank != 4:
        return symbolic_helper._unimplemented("pixel_shuffle", "only support 4d input")
    return g.op("DepthToSpace", self, blocksize_i=upscale_factor, mode_s="CRD")


def pixel_shuffle(g: jit_utils.GraphContext, self, upscale_factor):
    dims = symbolic_helper._get_tensor_sizes(self)
    if len(dims) != 4:
        return symbolic_helper._unimplemented(
            "pixel_shuffle", "only support 4d input", self
        )
    if any(i is None for i in dims[1:]):
        after_view = symbolic_helper._reshape_helper(
            g,
            symbolic_helper._unsqueeze_helper(g, self, [2, 3]),
            g.op(
                "Constant",
                value_t=torch.tensor([0, -1, upscale_factor, upscale_factor, 0, 0]),
            ),
            allowzero=0,
        )
        after_transpose = g.op("Transpose", after_view, perm_i=[0, 1, 4, 2, 5, 3])
        # For dynamic input shapes, two reshapes are performed
        reshape_h = symbolic_helper._reshape_helper(
            g,
            after_transpose,
            g.op("Constant", value_t=torch.tensor([0, 0, -1, 1, 0, 0])),
            allowzero=0,
        )
        reshape_w = symbolic_helper._reshape_helper(
            g,
            reshape_h,
            g.op("Constant", value_t=torch.tensor([0, 0, 0, 0, -1, 1])),
            allowzero=0,
        )
        return symbolic_helper._squeeze_helper(g, reshape_w, [3, 5])
    else:
        output_channel = dims[1] // upscale_factor // upscale_factor
        after_view = symbolic_helper._reshape_helper(
            g,
            self,
            g.op(
                "Constant",
                value_t=torch.tensor(
                    [
                        -1,
                        output_channel,
                        upscale_factor,
                        upscale_factor,
                        dims[2],
                        dims[3],
                    ]
                ),
            ),
            allowzero=0,
        )
        after_transpose = g.op("Transpose", after_view, perm_i=[0, 1, 4, 2, 5, 3])
        return symbolic_helper._reshape_helper(
            g,
            after_transpose,
            g.op(
                "Constant",
                value_t=torch.tensor(
                    [
                        -1,
                        output_channel,
                        dims[2] * upscale_factor,
                        dims[3] * upscale_factor,
                    ]
                ),
            ),
            allowzero=0,
        )

