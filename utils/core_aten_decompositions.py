
def core_aten_decompositions() -> "CustomDecompTable":
    from torch.export.exported_program import default_decompositions

    return default_decompositions()

