
def triu_onnx(x, diagonal=0):
    l = x.shape[0]
    arange = torch.arange(l, device=x.device)
    mask = arange.expand(l, l)
    arange = arange.unsqueeze(-1)
    if diagonal:
        arange = arange + diagonal
    mask = mask >= arange
    return x.masked_fill(mask == 0, 0)


def triu_onnx(x, diagonal=0, out=None):
    assert out is None
    assert len(x.shape) == 2 and x.size(0) == x.size(1)

    torch_triu = torch_func["triu"]
    template = torch_triu(torch.ones((1024, 1024), dtype=torch.uint8), diagonal)
    mask = template[: x.size(0), : x.size(1)]
    return torch.where(mask.bool(), x, torch.zeros_like(x))

