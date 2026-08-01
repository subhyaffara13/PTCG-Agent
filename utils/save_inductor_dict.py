
def save_inductor_dict(pass_to_compare=None):
    if not pass_to_compare:
        pass_to_compare = list(config.pre_grad_fusion_options.keys()) + list(
            config.post_grad_fusion_options.keys()
        )
    return {p: dict(counters["inductor"]).get(p, 0) for p in pass_to_compare}

