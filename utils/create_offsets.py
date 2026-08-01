
def create_offsets(offs_box, m1_is_2d, m2_is_2d, m, n, k, alignment):
    if m1_is_2d:
        if m2_is_2d:
            end = k
        else:
            end = m
    else:
        if m2_is_2d:
            end = n
        else:
            return None

    end_hint = V.graph.sizevars.optimization_hint(end)
    noffs_hint = V.graph.sizevars.optimization_hint(offs_box.get_size()[0])
    offs = torch.arange(1, noffs_hint + 1, dtype=torch.float32) * (
        end_hint / noffs_hint
    )
    offs[:-1] = (offs[:-1] / alignment).round() * alignment
    offs[-1] = end_hint
    return offs.to(dtype=offs_box.get_dtype(), device=offs_box.get_device())

