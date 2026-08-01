
def build_pipeline_init_args(
    has_tokenizer: bool = False,
    has_feature_extractor: bool = False,
    has_image_processor: bool = False,
    has_video_processor: bool = False,
    has_processor: bool = False,
    supports_binary_output: bool = True,
) -> str:
    docstring = r"""
    Arguments:
        model ([`PreTrainedModel`]):
            The model that will be used by the pipeline to make predictions. This needs to be a model inheriting from
            [`PreTrainedModel`]."""
    if has_tokenizer:
        docstring += r"""
        tokenizer ([`PreTrainedTokenizer`]):
            The tokenizer that will be used by the pipeline to encode data for the model. This object inherits from
            [`PreTrainedTokenizer`]."""
    if has_feature_extractor:
        docstring += r"""
        feature_extractor ([`SequenceFeatureExtractor`]):
            The feature extractor that will be used by the pipeline to encode data for the model. This object inherits from
            [`SequenceFeatureExtractor`]."""
    if has_image_processor:
        docstring += r"""
        image_processor ([`BaseImageProcessor`]):
            The image processor that will be used by the pipeline to encode data for the model. This object inherits from
            [`BaseImageProcessor`]."""
    if has_video_processor:
        docstring += r"""
        video_processor ([`BaseVideoProcessor`]):
            The video processor that will be used by the pipeline to encode video data for the model. This object
            inherits from [`BaseVideoProcessor`]."""
    if has_processor:
        docstring += r"""
        processor ([`ProcessorMixin`]):
            The processor that will be used by the pipeline to encode data for the model. This object inherits from
            [`ProcessorMixin`]. Processor is a composite object that might contain `tokenizer`, `feature_extractor`, and
            `image_processor`."""
    docstring += r"""
        task (`str`, defaults to `""`):
            A task-identifier for the pipeline.
        num_workers (`int`, *optional*, defaults to 8):
            When the pipeline will use *DataLoader* (when passing a dataset, on GPU for a Pytorch model), the number of
            workers to be used.
        batch_size (`int`, *optional*, defaults to 1):
            When the pipeline will use *DataLoader* (when passing a dataset, on GPU for a Pytorch model), the size of
            the batch to use, for inference this is not always beneficial, please read [Batching with
            pipelines](https://huggingface.co/transformers/main_classes/pipelines.html#pipeline-batching) .
        args_parser ([`~pipelines.ArgumentHandler`], *optional*):
            Reference to the object in charge of parsing supplied pipeline parameters.
        device (`int`, *optional*, defaults to -1):
            Device ordinal for CPU/GPU supports. Setting this to -1 will leverage CPU, a positive will run the model on
            the associated CUDA device id. You can pass native `torch.device` or a `str` too
        dtype (`str` or `torch.dtype`, *optional*):
            Sent directly as `model_kwargs` (just a simpler shortcut) to use the available precision for this model
            (`torch.float16`, `torch.bfloat16`, ... or `"auto"`)"""
    if supports_binary_output:
        docstring += r"""
        binary_output (`bool`, *optional*, defaults to `False`):
            Flag indicating if the output the pipeline should happen in a serialized format (i.e., pickle) or as
            the raw output data e.g. text."""
    return docstring

