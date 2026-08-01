
def _get_count_function(
    model: Optional[str],
    custom_tokenizer: Optional[Union[dict, SelectTokenizerResponse]] = None,
) -> TokenCounterFunction:
    """
    Get the function to count tokens based on the model and custom tokenizer."""
    from litellm.utils import _select_tokenizer, print_verbose

    if model is not None or custom_tokenizer is not None:
        tokenizer_json = custom_tokenizer or _select_tokenizer(model)  # type: ignore
        if tokenizer_json["type"] == "huggingface_tokenizer":

            def count_tokens(text: str) -> int:
                enc = tokenizer_json["tokenizer"].encode(text)
                return len(enc.ids)

        elif tokenizer_json["type"] == "openai_tokenizer":
            model_to_use = _fix_model_name(model)  # type: ignore
            try:
                if "gpt-4o" in model_to_use:
                    encoding = tiktoken.get_encoding("o200k_base")
                else:
                    encoding = tiktoken.encoding_for_model(model_to_use)
            except KeyError:
                print_verbose("Warning: model not found. Using cl100k_base encoding.")
                encoding = tiktoken.get_encoding("cl100k_base")

            def count_tokens(text: str) -> int:
                return len(encoding.encode(text, disallowed_special=()))

        else:
            raise ValueError("Unsupported tokenizer type")
    else:

        def count_tokens(text: str) -> int:
            return len(default_encoding.encode(text, disallowed_special=()))

    return count_tokens

