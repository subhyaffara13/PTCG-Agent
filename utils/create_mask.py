
def create_mask(
    mod_fn: _score_mod_signature | _mask_mod_signature,
    B: int | None,
    H: int | None,
    Q_LEN: int,
    KV_LEN: int,
    device: DeviceLikeType | None = None,
) -> Tensor:
    r"""This function creates a mask tensor from a mod_fn function.

    Args:
        mod_fn (Union[_score_mod_signature, _mask_mod_signature]): Function to modify attention scores.
        B (int): Batch size.
        H (int): Number of query heads.
        Q_LEN (int): Sequence length of query.
        KV_LEN (int): Sequence length of key/value.
        device (str): Device to run the mask creation on.

    Returns:
        mask (Tensor): A mask tensor with shape (B, H, M, N).
    """
    if device is None:
        device = torch.accelerator.current_accelerator() or "cpu"
    if B is None:
        B = 1
    if H is None:
        H = 1
    b = torch.arange(0, B, device=device)
    h = torch.arange(0, H, device=device)
    m = torch.arange(0, Q_LEN, device=device)
    n = torch.arange(0, KV_LEN, device=device)
    mod_type = _get_mod_type(mod_fn)

    from torch._dynamo._trace_wrapped_higher_order_op import TransformGetItemToIndex

    with TransformGetItemToIndex():
        if mod_type == _ModificationType.SCORE_MOD:
            score_mod = mod_fn
            score_mod = _vmap_for_bhqkv(score_mod, prefix=(0,))  # first input is score
            out = score_mod(torch.zeros(B, H, Q_LEN, KV_LEN, device=device), b, h, m, n)
            mask = torch.where(torch.isneginf(out), False, True)
            return mask
        elif mod_type == _ModificationType.MASK_MOD:
            mask_mod = mod_fn
            mask_mod = _vmap_for_bhqkv(mask_mod, prefix=())
            mask = mask_mod(b, h, m, n)
            return mask
        else:
            raise AssertionError


def create_mask(output: _ods_ir.Type, low: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], high: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CreateMaskOp(output=output, low=low, high=high, loc=loc, ip=ip).result


def create_mask(result: _ods_ir.Type, mask_dim_sizes: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return CreateMaskOp(result=result, mask_dim_sizes=mask_dim_sizes, loc=loc, ip=ip).result

