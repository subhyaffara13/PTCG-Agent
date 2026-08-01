
def mode_default(self, dim=-1, keepdim=False):
    """Lower aten.mode via sort-based decomposition or fallback."""
    if not config.triton.decompose_sort_ops:
        return mode_fallback(self, dim, keepdim)
    shape = self.get_size()
    ndim = len(shape)
    device = self.get_device()
    if ndim == 0:
        return clone(self), _full(0, device, torch.int64, shape)
    dim = canonicalize_dim(ndim, dim)
    sorted_vals, sorted_idxs = sort_stable(self, stable=True, dim=dim)
    n = shape[dim]

    # Position indices along dim: [0, 1, ..., n-1]
    positions = iota(
        n, start=0, step=1, dtype=torch.int64, device=device, requires_grad=False
    )
    pos_view_shape = [sympy.Integer(1)] * ndim
    pos_view_shape[dim] = n
    positions = view(positions, pos_view_shape)
    positions = expand(positions, shape)

    # Shift positions by -1, clamp to 0 for position 0
    positions_loader0 = positions.make_loader()

    def prev_pos_fn(idx):
        return ops.maximum(
            ops.sub(positions_loader0(idx), ops.constant(1, torch.int64)),
            ops.constant(0, torch.int64),
        )

    prev_positions = Pointwise.create(
        device=decode_device(device),
        dtype=torch.int64,
        inner_fn=prev_pos_fn,
        ranges=shape,
    )

    # Gather shifted values and compare for run boundaries
    shifted_vals = gather(sorted_vals, dim, prev_positions)

    sorted_loader = sorted_vals.make_loader()
    shifted_loader = shifted_vals.make_loader()
    positions_loader = positions.make_loader()

    # is_boundary = (sorted != shifted) | (position == 0)
    def is_boundary_fn(idx):
        return ops.or_(
            ops.ne(sorted_loader(idx), shifted_loader(idx)),
            ops.eq(positions_loader(idx), ops.constant(0, torch.int64)),
        )

    is_boundary = Pointwise.create(
        device=decode_device(device),
        dtype=torch.bool,
        inner_fn=is_boundary_fn,
        ranges=shape,
    )

    # boundary_pos = where(is_boundary, position, -1)
    is_boundary_loader = is_boundary.make_loader()
    positions_loader2 = positions.make_loader()

    def boundary_pos_fn(idx):
        return ops.where(
            is_boundary_loader(idx),
            positions_loader2(idx),
            ops.constant(-1, torch.int64),
        )

    boundary_pos = Pointwise.create(
        device=decode_device(device),
        dtype=torch.int64,
        inner_fn=boundary_pos_fn,
        ranges=shape,
    )

    # Propagate boundary positions forward with cummax
    last_boundary, _ = cummax(boundary_pos, dim)

    # run_len = position - last_boundary + 1
    positions_loader3 = positions.make_loader()
    last_boundary_loader = last_boundary.make_loader()

    def run_len_fn(idx):
        return ops.add(
            ops.sub(positions_loader3(idx), last_boundary_loader(idx)),
            ops.constant(1, torch.int64),
        )

    run_len = Pointwise.create(
        device=decode_device(device),
        dtype=torch.int64,
        inner_fn=run_len_fn,
        ranges=shape,
    )

    # argmax returns first maximum -> end of leftmost longest run
    max_pos = reduce_argmax(run_len, axis=dim, keepdims=True)
    mode_vals = gather(sorted_vals, dim, max_pos)
    mode_idxs = gather(sorted_idxs, dim, max_pos)

    if not keepdim:
        mode_vals = squeeze(mode_vals, dim)
        mode_idxs = squeeze(mode_idxs, dim)

    return mode_vals, mode_idxs

