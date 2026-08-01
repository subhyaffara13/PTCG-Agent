
def should_pad_mm(match: Match) -> bool:
    mat1, mat2 = fetch_fake_tensors(match, ("mat1", "mat2"))
    return should_pad(match, mat1, mat2, torch.ops.aten.mm)

