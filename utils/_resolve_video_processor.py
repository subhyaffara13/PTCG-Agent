
def _resolve_video_processor(
    video_processor,
    load_video_processor,
    model_name,
    config,
    task,
    hub_kwargs,
    model_kwargs,
):
    def load(video_processor):
        video_processor = _infer_pipeline_component(
            video_processor,
            model_name,
            config,
            "Impossible to guess which video processor to use. "
            "Please provide a BaseVideoProcessor class or a path/identifier to a pretrained video processor.",
        )

        if not isinstance(video_processor, str):
            return video_processor

        return AutoVideoProcessor.from_pretrained(video_processor, _from_pipeline=task, **hub_kwargs, **model_kwargs)

    return _load_pipeline_component(load_video_processor, video_processor, load)

