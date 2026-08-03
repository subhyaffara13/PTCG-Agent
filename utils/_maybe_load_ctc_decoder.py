import os

def _maybe_load_ctc_decoder(model_name, hub_kwargs, kwargs, pretrained_model_name_or_path):
    """Attach a pyctcdecode decoder when the loaded feature extractor declares an LM-backed processor."""
    config_dict, _ = FeatureExtractionMixin.get_feature_extractor_dict(
        pretrained_model_name_or_path or model_name,
        **hub_kwargs,
    )
    processor_class = config_dict.get("processor_class", None)

    if processor_class is None or not processor_class.endswith("WithLM") or not isinstance(model_name, str):
        return

    try:
        import kenlm  # to trigger `ImportError` if not installed
        from pyctcdecode import BeamSearchDecoderCTC

        if os.path.isdir(model_name) or os.path.isfile(model_name):
            decoder = BeamSearchDecoderCTC.load_from_dir(model_name)
        else:
            language_model_glob = os.path.join(BeamSearchDecoderCTC._LANGUAGE_MODEL_SERIALIZED_DIRECTORY, "*")
            alphabet_filename = BeamSearchDecoderCTC._ALPHABET_SERIALIZED_FILENAME
            allow_patterns = [language_model_glob, alphabet_filename]
            decoder = BeamSearchDecoderCTC.load_from_hf_hub(model_name, allow_patterns=allow_patterns)

        kwargs["decoder"] = decoder
    except ImportError as error:
        logger.warning(f"Could not load the `decoder` for {model_name}. Defaulting to raw CTC. Error: {error}")
        if not is_kenlm_available():
            logger.warning("Try to install `kenlm`: `pip install kenlm")

        if not is_pyctcdecode_available():
            logger.warning("Try to install `pyctcdecode`: `pip install pyctcdecode")

