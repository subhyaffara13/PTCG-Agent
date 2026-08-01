
def get_optimum_ort_pipeline(
    model_name: str,
    directory: str,
    provider="CUDAExecutionProvider",
    disable_safety_checker: bool = True,
    use_io_binding: bool = False,
):
    from optimum.onnxruntime import ORTPipelineForText2Image  # noqa: PLC0415

    if directory is not None and os.path.exists(directory):
        pipeline = ORTPipelineForText2Image.from_pretrained(directory, provider=provider, use_io_binding=use_io_binding)
    else:
        pipeline = ORTPipelineForText2Image.from_pretrained(
            model_name,
            export=True,
            provider=provider,
            use_io_binding=use_io_binding,
        )
        pipeline.save_pretrained(directory)

    if disable_safety_checker:
        pipeline.safety_checker = None
        pipeline.feature_extractor = None

    return pipeline

