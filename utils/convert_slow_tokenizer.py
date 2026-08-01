
def convert_slow_tokenizer(transformer_tokenizer, from_tiktoken=False) -> Tokenizer:
    """
    Utilities to convert a slow tokenizer instance in a fast tokenizer instance.

    Args:
        transformer_tokenizer ([`~tokenization_utils_base.PreTrainedTokenizer`]):
            Instance of a slow tokenizer to convert in the backend tokenizer for
            [`~tokenization_utils_base.PreTrainedTokenizerFast`].
       from_tiktoken (bool, optional): Whether to use the `tiktoken` library to convert the tokenizer instead of sentencepiece.
            Defaults to False.

    Return:
        A instance of [`~tokenizers.Tokenizer`] to be used as the backend tokenizer of a
        [`~tokenization_utils_base.PreTrainedTokenizerFast`]
    """

    tokenizer_class_name = transformer_tokenizer.__class__.__name__
    if tokenizer_class_name in SLOW_TO_FAST_CONVERTERS and not from_tiktoken:
        converter_class = SLOW_TO_FAST_CONVERTERS[tokenizer_class_name]
        return converter_class(transformer_tokenizer).converted()
    elif transformer_tokenizer.vocab_file.endswith("tekken.json"):
        transformer_tokenizer.original_tokenizer = transformer_tokenizer
        logger.info("Converting from Mistral tekken.json")
        return MistralConverter(transformer_tokenizer.vocab_file).converted()
    else:
        try:
            logger.info("Converting from Tiktoken")
            return TikTokenConverter(
                vocab_file=transformer_tokenizer.vocab_file,
                extra_special_tokens=transformer_tokenizer.extra_special_tokens,
            ).converted()
        except Exception:
            raise ValueError(
                f"Converting from SentencePiece and Tiktoken failed, if a converter for SentencePiece is available, provide a model path "
                f"with a SentencePiece tokenizer.model file."
                f"Currently available slow->fast converters: {list(SLOW_TO_FAST_CONVERTERS.keys())}"
            )


def convert_slow_tokenizer(*args, **kwargs):
    requires_backends(convert_slow_tokenizer, ["sentencepiece", "tokenizers"])

