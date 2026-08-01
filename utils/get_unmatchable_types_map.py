
def get_unmatchable_types_map() -> dict[str, set[NSNodeTargetType]]:
    FUNS_UNMATCHABLE: set[NSNodeTargetType] = {
        torch.quantize_per_tensor,
        operator.getitem,
    }

    MODS_UNMATCHABLE: set[NSNodeTargetType] = {
        nn.Identity,
    }

    METHS_UNMATCHABLE: set[NSNodeTargetType] = {
        "to",
        "dequantize",
        "reshape",
        "view",
        "unsqueeze_",
        "unsqueeze",
        "transpose",
        "squeeze_",
        "squeeze",
        "size",
        "shape",
        "resize_",
        "repeat_interleave",
        "repeat",
        "permute",
        "numel",
        "mean",
        "detach_",
        "detach",
        "contiguous",
        "clamp",
        "chunk",
    }

    return {
        "funs_unmatchable": FUNS_UNMATCHABLE,
        "mods_unmatchable": MODS_UNMATCHABLE,
        "meths_unmatchable": METHS_UNMATCHABLE,
    }

