
def _n_shadows_compare_weights(
    model: torch.nn.Module,
    example_inputs: Any,
    qconfig_mapping: QConfigMapping,
    backend_config: BackendConfig,
) -> NSResultsType:
    """
    Note: this API is not recommended for wide usage, it is only
    provided for customers who need to migrate from the `add_loggers`
    API.
    """
    qconfig_multi_mapping = QConfigMultiMapping.from_list_qconfig_mapping(
        [qconfig_mapping]
    )
    mp = prepare_n_shadows_model(
        model, example_inputs, qconfig_multi_mapping, backend_config
    )
    # passing inputs through the model is necessary to populate
    # observers which observe weights with real values
    mp(*example_inputs)
    mq = convert_n_shadows_model(mp)
    weight_comparison = extract_weight_comparison(mq)
    return weight_comparison

