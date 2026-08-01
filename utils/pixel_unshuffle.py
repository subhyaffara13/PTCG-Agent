
def pixel_unshuffle(self: Tensor, downscale_factor: int):
    torch._check(
        self.dim() >= 3,
        lambda: f"pixel_unshuffle expects input to have at least 3 dimensions, but got input with {self.dim} dimension(s)",
    )
    batch = self.shape[:-3]
    C_out = self.shape[-3] * downscale_factor**2
    HW_out = (self.shape[-2] // downscale_factor, self.shape[-1] // downscale_factor)
    n = len(batch)
    B_dims = range(n)
    C_dim, H_dim, r1_dim, W_dim, r2_dim = range(n, n + 5)
    return (
        self.view(
            *batch,
            self.shape[-3],
            HW_out[0],
            downscale_factor,
            HW_out[1],
            downscale_factor,
        )
        .permute(*B_dims, C_dim, r1_dim, r2_dim, H_dim, W_dim)
        .reshape(*batch, C_out, *HW_out)
        .clone(memory_format=utils.suggest_memory_format(self))
    )


def pixel_unshuffle(g: jit_utils.GraphContext, self, downscale_factor):
    dims = symbolic_helper._get_tensor_sizes(self)
    if len(dims) != 4:
        return symbolic_helper._unimplemented(
            "pixel_shuffle", "only support 4d input", self
        )
    if any(i is None for i in dims[1:]):
        # For dynamic input shapes, two reshapes are performed
        reshape_h = symbolic_helper._reshape_helper(
            g,
            symbolic_helper._unsqueeze_helper(g, self, [3]),
            g.op("Constant", value_t=torch.tensor([0, 0, -1, downscale_factor, 0])),
            allowzero=0,
        )
        reshape_w = symbolic_helper._reshape_helper(
            g,
            reshape_h,
            g.op("Constant", value_t=torch.tensor([0, 0, 0, 0, -1, downscale_factor])),
            allowzero=0,
        )
        after_transpose = g.op("Transpose", reshape_w, perm_i=[0, 1, 3, 5, 2, 4])
        final_reshape = symbolic_helper._reshape_helper(
            g,
            after_transpose,
            g.op("Constant", value_t=torch.tensor([0, -1, 1, 1, 0, 0])),
            allowzero=0,
        )
        return symbolic_helper._squeeze_helper(g, final_reshape, [2, 3])
    else:
        output_channel = dims[1] * downscale_factor * downscale_factor
        after_view = symbolic_helper._reshape_helper(
            g,
            self,
            g.op(
                "Constant",
                value_t=torch.tensor(
                    [
                        -1,
                        dims[1],
                        dims[2] // downscale_factor,
                        downscale_factor,
                        dims[3] // downscale_factor,
                        downscale_factor,
                    ]
                ),
            ),
            allowzero=0,
        )
        after_transpose = g.op("Transpose", after_view, perm_i=[0, 1, 3, 5, 2, 4])
        return symbolic_helper._reshape_helper(
            g,
            after_transpose,
            g.op(
                "Constant",
                value_t=torch.tensor(
                    [
                        -1,
                        output_channel,
                        dims[2] // downscale_factor,
                        dims[3] // downscale_factor,
                    ]
                ),
            ),
            allowzero=0,
        )

