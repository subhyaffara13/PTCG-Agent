
def _check_unconstrained_bridge_property(G, info1):
    # Check Theorem 5 from Eswaran and Tarjan. (1975) Augmentation problems
    import math

    bridge_ccs = list(nx.connectivity.bridge_components(G))
    # condense G into an forest C
    C = collapse(G, bridge_ccs)

    p = len([n for n, d in C.degree() if d == 1])  # leafs
    q = len([n for n, d in C.degree() if d == 0])  # isolated
    if p + q > 1:
        size_target = math.ceil(p / 2) + q
        size_aug = info1["num_edges"]
        assert size_aug == size_target, (
            "augmentation size is different from what theory predicts"
        )

