
def sample_inputs_bmm(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, low=None, high=None, requires_grad=requires_grad)
    yield SampleInput(make_arg(M, S, M), make_arg(M, M, S))


def sample_inputs_bmm(op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs):
    for njt_3d in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[3]
    ):
        # (B, j1, D) x (B, D, E) => (B, j1, E)
        if njt_3d._ragged_idx == 1:
            B, D = njt_3d.shape[0], njt_3d.shape[-1]
            E = D + 2
            other = torch.randn(B, D, E, device=device, dtype=dtype)
            # used for slicing in unbind_reference()
            other._batch_dim = 0
            njt_desc = _describe_njt(njt_3d)
            yield SampleInput(
                _clone(njt_3d),
                kwargs={"mat2": other},
                name=f"{njt_desc}: (B, j, D) x (B, D, E)",
            )

