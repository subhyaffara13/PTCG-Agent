
def convert_gguf_tokenizer(architecture: str, tokenizer_dict) -> tuple[Tokenizer, dict]:
    """
    Utilities to convert a slow tokenizer instance in a fast tokenizer instance.

    Args:
        architecture (`str`): The model architecture derived from gguf file.
        transformer_tokenizer ([`~tokenization_utils_base.PreTrainedTokenizer`]):
            Instance of a slow tokenizer to convert in the backend tokenizer for
            [`~tokenization_utils_base.PreTrainedTokenizerFast`].

    Return:
        A instance of [`~tokenizers.Tokenizer`] to be used as the backend tokenizer of a
        [`~tokenization_utils_base.PreTrainedTokenizerFast`]
    """
    tokenizer_class_name = architecture
    converter = GGUF_TO_FAST_CONVERTERS[tokenizer_class_name](tokenizer_dict)
    fast_tokenizer = converter.converted()
    return fast_tokenizer, converter.additional_kwargs

