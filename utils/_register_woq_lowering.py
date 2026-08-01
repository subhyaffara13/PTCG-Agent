
def _register_woq_lowering(pattern, computation_woq, computation_reshape):
    @register_lowering_pattern(
        pattern,
        extra_check=_is_valid_woq_optimization_pattern(),
    )
    def woq_int8(match: Match, *args, **kwargs):
        x = kwargs["x"]
        weight = kwargs["weight"]
        scales = kwargs["scales"]
        counters["inductor"]["woq_matcher_count"] += 1
        counters["inductor"]["woq_matcher_nodes"] += len(match.nodes)
        out_features = weight.get_size()[0]
        origin_x_size = x.get_size()
        x_shape = [-1, origin_x_size[-1]]
        out_shape = origin_x_size[:-1] + [
            out_features,
        ]
        func1 = L[computation_reshape](x, x_shape)
        func2 = L[computation_woq](func1, weight, scales)
        return L[computation_reshape](func2, out_shape)

    return woq_int8

