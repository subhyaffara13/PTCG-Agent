
def _view2paddle(safeview, device) -> Dict[str, paddle.Tensor]:
    result = {}
    for k, v in safeview:
        dtype = _getdtype(v["dtype"])
        if len(v["data"]) == 0:
            # Workaround because frombuffer doesn't accept zero-size tensors
            assert any(x == 0 for x in v["shape"])
            arr = paddle.empty(v["shape"], dtype=dtype)
        else:
            arr = paddle.base.core.frombuffer(v["data"], dtype).reshape(v["shape"])
            if device != "cpu":
                arr = arr.to(device)
        if sys.byteorder == "big":
            arr = paddle.to_tensor(arr.numpy().byteswap(inplace=False), place=device)
        result[k] = arr

    return result

