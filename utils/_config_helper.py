
def _config_helper(bmm=False, persistent=False):
    # Each entry is: (sizes_dict, num_warps, num_stages)
    _base_mm_configs = [
        ({"x": 32, "y": 32, "r": 16}, 2, 1),
        ({"x": 32, "y": 32, "r": 128}, 4, 2),
        ({"x": 32, "y": 64, "r": 32}, 8, 5),
        ({"x": 64, "y": 32, "r": 32}, 8, 5),
        ({"x": 64, "y": 32, "r": 128}, 4, 5),
        ({"x": 64, "y": 64, "r": 16}, 4, 2),
        ({"x": 64, "y": 64, "r": 32}, 4, 2),
        ({"x": 64, "y": 64, "r": 64}, 8, 3),
        ({"x": 64, "y": 64, "r": 128}, 4, 5),
        ({"x": 64, "y": 128, "r": 32}, 4, 3),
        ({"x": 64, "y": 128, "r": 32}, 8, 4),
        ({"x": 64, "y": 128, "r": 64}, 4, 3),
        ({"x": 64, "y": 128, "r": 128}, 4, 4),
        ({"x": 128, "y": 64, "r": 32}, 4, 3),
        ({"x": 128, "y": 64, "r": 32}, 8, 4),
        ({"x": 128, "y": 128, "r": 32}, 8, 2),
        ({"x": 128, "y": 128, "r": 32}, 4, 3),
        ({"x": 128, "y": 128, "r": 64}, 4, 3),
        ({"x": 128, "y": 128, "r": 64}, 8, 5),
    ]
    out = []
    for sizes, w, s in _base_mm_configs:
        d = dict(sizes)
        if persistent:
            d.pop("r", None)
        if bmm:
            d["z"] = 1
        out.append((d, w, s))

    # Deduplicate by converting dicts to immutable frozensets
    deduped = {(frozenset(d.items()), w, s): (d, w, s) for d, w, s in out}

    return list(deduped.values())

