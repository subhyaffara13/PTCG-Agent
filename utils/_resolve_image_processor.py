
def _resolve_image_processor(
    image_processor,
    feature_extractor,
    load_image_processor,
    model_name,
    config,
    task,
    hub_kwargs,
    model_kwargs,
):
    """Resolve and optionally load the image processor for vision-capable pipelines."""

    def load(image_processor):
        image_processor = _infer_pipeline_component(
            image_processor,
            model_name,
            config,
            "Impossible to guess which image processor to use. "
            "Please provide a PreTrainedImageProcessor class or a path/identifier to a pretrained image processor.",
            fallback_component=feature_extractor if isinstance(feature_extractor, BaseImageProcessor) else None,
        )

        if not isinstance(image_processor, (str, tuple)):
            return image_processor

        return AutoImageProcessor.from_pretrained(image_processor, _from_pipeline=task, **hub_kwargs, **model_kwargs)

    return _load_pipeline_component(load_image_processor, image_processor, load)

