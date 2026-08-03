from typing import Optional

def _select_tokenizer(
    model: str, custom_tokenizer: Optional[CustomHuggingfaceTokenizer] = None
):
    if custom_tokenizer is not None:
        _tokenizer = create_pretrained_tokenizer(
            identifier=custom_tokenizer["identifier"],
            revision=custom_tokenizer["revision"],
            auth_token=custom_tokenizer["auth_token"],
        )
        return _tokenizer
    return _select_tokenizer_helper(model=model)

