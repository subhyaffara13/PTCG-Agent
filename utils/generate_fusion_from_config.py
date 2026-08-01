
def generate_fusion_from_config(config_options: dict[str, Any], pre_grad=True):
    fusions: list[GroupBatchFusionBase] = []
    for name, options in config_options.items():
        # we skip all patterns from pattern_matcher passes (e.g., split_cat)
        if name not in PRE_GRAD_FUSIONS and name not in POST_GRAD_FUSIONS:
            continue
        fusion_cls = PRE_GRAD_FUSIONS[name] if pre_grad else POST_GRAD_FUSIONS[name]
        _options = graph_search_options.copy()
        _options.update(options)
        fusions.append(fusion_cls(graph_search_options=_options))  # type: ignore[operator]
    return fusions

