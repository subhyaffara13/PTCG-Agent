
def build_k_number_dict(kcomps):
    return {
        node: k
        for k, comps in sorted(kcomps.items(), key=itemgetter(0))
        for comp in comps
        for node in comp
    }


def build_k_number_dict(k_components):
    k_num = {}
    for k, comps in sorted(k_components.items()):
        for comp in comps:
            for node in comp:
                k_num[node] = k
    return k_num

