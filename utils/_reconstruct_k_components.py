
def _reconstruct_k_components(k_comps):
    result = {}
    max_k = max(k_comps) if k_comps else 0
    for k in range(max_k, 0, -1):
        if k == max_k:
            result[k] = list(_consolidate(k_comps[k], k))
        elif k not in k_comps:
            result[k] = list(_consolidate(result[k + 1], k))
        else:
            nodes_at_k = set.union(*k_comps[k])
            to_add = [c for c in result[k + 1] if any(n not in nodes_at_k for n in c)]
            if to_add:
                result[k] = list(_consolidate(k_comps[k] + to_add, k))
            else:
                result[k] = list(_consolidate(k_comps[k], k))
    return result

