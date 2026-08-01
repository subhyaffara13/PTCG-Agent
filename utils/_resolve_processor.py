
def _resolve_processor(processor, load_processor, model_name, config, task, hub_kwargs, model_kwargs):
    """Resolve and optionally load a multimodal processor."""

    def load(processor):
        processor = _infer_pipeline_component(
            processor,
            model_name,
            config,
            "Impossible to guess which processor to use. "
            "Please provide a processor instance or a path/identifier to a processor.",
        )

        if not isinstance(processor, (str, tuple)):
            return processor

        processor = AutoProcessor.from_pretrained(processor, _from_pipeline=task, **hub_kwargs, **model_kwargs)
        if not isinstance(processor, ProcessorMixin):
            raise TypeError(
                "Processor was loaded, but it is not an instance of `ProcessorMixin`. "
                f"Got type `{type(processor)}` instead. Please check that you specified "
                "correct pipeline task for the model and model has processor implemented and saved."
            )
        return processor

    return _load_pipeline_component(load_processor, processor, load)

