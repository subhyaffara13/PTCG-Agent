
def sample_inputs_elementwise_njt_binary(
    op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs
):
    if not op_kwargs:
        op_kwargs = {}

    for njt1 in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[2, 3, 4]
    ):
        njt_desc = _describe_njt(njt1)
        njt2 = torch.randn_like(njt1)
        yield SampleInput(
            _clone(njt1),
            args=(njt2,),
            kwargs=dict(op_kwargs),
            name=f"{njt_desc}: (NT, NT)",
        )

        # broadcasting case: (B, j0, ...) with (B, 1, ...)
        dense_shape = list(njt1.shape)
        dense_shape[njt1._ragged_idx] = 1
        t = torch.randn(
            dense_shape,
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
        )
        t2 = _clone(t)
        # used for slicing in unbind_reference()
        t._batch_dim = 0
        t2._batch_dim = 0
        # (NT, T)
        yield SampleInput(
            _clone(njt1),
            args=(t,),
            kwargs=dict(op_kwargs),
            name=f"{njt_desc}: (NT, T) broadcasting 1 over ragged",
        )
        # (T, NT)
        yield SampleInput(
            t2,
            args=(_clone(njt1),),
            kwargs=dict(op_kwargs),
            name=f"{njt_desc}: (T, NT) broadcasting 1 over ragged",
        )

        # broadcasting case: (B, j0, ...) with (1, 1...)
        t = torch.randn(
            [1 for _ in range(njt1.dim())],
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
        )
        t2 = _clone(t)
        # used for slicing in unbind_reference()
        t._batch_dim = 0
        t2._batch_dim = 0
        # (NT, T)
        yield SampleInput(
            _clone(njt1),
            args=(t,),
            kwargs=dict(op_kwargs),
            name=f"{njt_desc}: (NT, T) broadcasting all 1s",
        )
        # (T, NT)
        yield SampleInput(
            t2,
            args=(_clone(njt1),),
            kwargs=dict(op_kwargs),
            name=f"{njt_desc}: (T, NT) broadcasting all 1s",
        )

        # broadcasting case: (B, j0, ...) with (...)
        if njt1.dim() > njt1._ragged_idx + 1:
            t = torch.randn(
                njt1.shape[njt1._ragged_idx + 1 :],
                device=device,
                dtype=dtype,
                requires_grad=requires_grad,
            )
            # (NT, T)
            yield SampleInput(
                _clone(njt1),
                args=(_clone(t),),
                kwargs=dict(op_kwargs),
                name=f"{njt_desc}: (NT, T) broadcasting normal dims",
            )
            # (T, NT)
            yield SampleInput(
                _clone(t),
                args=(_clone(njt1),),
                kwargs=dict(op_kwargs),
                name=f"{njt_desc}: (T, NT) broadcasting normal dims",
            )

        # broadcasting case: (B, j0, ...) with scalar
        t = torch.randn((), device=device, dtype=dtype, requires_grad=requires_grad)
        # (NT, T)
        yield SampleInput(
            _clone(njt1),
            args=(_clone(t),),
            kwargs=dict(op_kwargs),
            name=f"{njt_desc}: (NT, T) broadcasting with scalar",
        )
        # (T, NT)
        yield SampleInput(
            _clone(t),
            args=(_clone(njt1),),
            kwargs=dict(op_kwargs),
            name=f"{njt_desc}: (T, NT) broadcasting with scalar",
        )

    # mixed broadcasting case: (B, j0, 1) with (B, 1, D)
    B = 4
    D = 16
    njt = random_nt_from_dims(
        (B, None, 1),
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        layout=torch.jagged,
    )
    njt_desc = _describe_njt(njt)
    t = torch.randn(B, 1, D, device=device, dtype=dtype, requires_grad=requires_grad)
    t2 = _clone(t)
    # used for slicing in unbind_reference()
    t._batch_dim = 0
    t2._batch_dim = 0

    # (NT, T)
    yield SampleInput(
        _clone(njt),
        args=(t,),
        kwargs=dict(op_kwargs),
        name=f"{njt_desc}: (NT, T) mixed broadcasting",
    )
    # (T, NT)
    yield SampleInput(
        t2,
        args=(_clone(njt),),
        kwargs=dict(op_kwargs),
        name=f"{njt_desc}: (T, NT) mixed broadcasting",
    )

