
def get_triton_kernel(mod: ModuleType):  # type: ignore[no-untyped-def]
    from torch._inductor.runtime.triton_heuristics import CachingAutotuner

    cand_list = [
        v
        for k, v in mod.__dict__.items()
        if k.startswith("triton_") and isinstance(v, CachingAutotuner)
    ]
    assert len(cand_list) == 1
    return cand_list[0]

