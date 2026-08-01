
def sample_inputs_squeeze(op_info, device, dtype, requires_grad, **kwargs):
    shapes_and_args = (
        ((S, 1, S, 1), ()),
        ((1, 1, 1, 1), ()),
        ((1, 1, 1, 1), (0,)),
        ((S, 1, S, 1), (1,)),
        ((S, 1, S, 1), (-1,)),
        ((S, 1, S, 1), (2,)),
        ((S, 1, S, 1), (-2,)),
        ((), (0, )),
    )

    for shape, args in shapes_and_args:
        tensor = make_tensor(shape, dtype=dtype, device=device, low=None, high=None,
                             requires_grad=requires_grad)

        yield SampleInput(tensor, args=args)


def sample_inputs_squeeze(op_info, device, dtype, requires_grad, **kwargs):
    # squeeze-specific NJT generator (need to ensure there are some 1s in the shape)
    def _get_njts():
        njt = random_nt_from_dims(
            (4, None, 1, 3, 1),
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
            layout=torch.jagged,
        )
        yield njt
        # without min / max seqlen cached
        values = njt.values().detach().clone()
        offsets = njt.offsets().detach().clone()
        yield torch.nested.nested_tensor_from_jagged(values, offsets)
        # non-contiguous transposed
        yield njt.transpose(1, 3)
        # non-contiguous with holes
        values = njt.values().detach().clone()
        offsets = njt.offsets().detach().clone()
        # subtract 1 to cause holes
        lengths = (offsets.diff() - 1).detach().clone()
        yield torch.nested.nested_tensor_from_jagged(
            values=values,
            offsets=offsets,
            lengths=lengths,
        )

    for njt in _get_njts():
        # single dim operation
        for dim in range(njt.dim()):
            # Operation on batch / ragged dim is never expected to work.
            # TODO: Handle these via error_inputs.
            if dim == 0 or dim == njt._ragged_idx:
                continue

            yield SampleInput(
                _clone(njt),
                kwargs={"dim": dim},
                name=f"{_describe_njt(njt)}: {_describe_dim(njt, dim)}",
            )

        # multiple dim operation (pass no args)
        yield SampleInput(
            _clone(njt),
            kwargs={"dim": dim},
            name=f"{_describe_njt(njt)}: multiple dims",
        )

