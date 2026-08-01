
def _ufunc_postprocess(result, out, casting):
    if out is not None:
        result = _util.typecast_tensor(result, out.dtype.torch_dtype, casting)
        result = torch.broadcast_to(result, out.shape)
    return result

