
def should_pad_addmm(match: Match) -> bool:
    mat1, mat2, input = fetch_fake_tensors(match, ("mat1", "mat2", "input"))
    return should_pad(match, mat1, mat2, torch.ops.aten.addmm, input=input)

