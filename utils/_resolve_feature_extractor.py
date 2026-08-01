
def _resolve_feature_extractor(
    feature_extractor,
    load_feature_extractor,
    model_name,
    config,
    task,
    hub_kwargs,
    model_kwargs,
    kwargs,
    pretrained_model_name_or_path,
):
    """Resolve and optionally load the feature extractor, including CTC decoder side-loading."""

    def load(feature_extractor):
        feature_extractor = _infer_pipeline_component(
            feature_extractor,
            model_name,
            config,
            "Impossible to guess which feature extractor to use. "
            "Please provide a PreTrainedFeatureExtractor class or a path/identifier to a pretrained feature extractor.",
        )

        if not isinstance(feature_extractor, (str, tuple)):
            return feature_extractor

        feature_extractor = AutoFeatureExtractor.from_pretrained(
            feature_extractor, _from_pipeline=task, **hub_kwargs, **model_kwargs
        )
        _maybe_load_ctc_decoder(model_name, hub_kwargs, kwargs, pretrained_model_name_or_path)
        return feature_extractor

    return _load_pipeline_component(load_feature_extractor, feature_extractor, load)

