
def conv1x1_via_mm(x, w, *, out):
    w = torch.squeeze(torch.squeeze(w, -1), -1)
    return torch.matmul(
        x.permute(0, 2, 3, 1), w.permute(1, 0), out=out.permute(0, 2, 3, 1)
    )

