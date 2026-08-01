
def _get_tokenizer_loading_kwargs(tokenizer, use_fast, model_kwargs):
    """Normalize tokenizer tuple/string inputs into `AutoTokenizer.from_pretrained` kwargs."""
    if isinstance(tokenizer, tuple):
        tokenizer_identifier = tokenizer[0]
        tokenizer_kwargs = tokenizer[1].copy()
        tokenizer_use_fast = tokenizer_kwargs.pop("use_fast", use_fast)
    else:
        tokenizer_identifier = tokenizer
        tokenizer_kwargs = model_kwargs.copy()
        tokenizer_kwargs.pop("torch_dtype", None)
        tokenizer_kwargs.pop("dtype", None)
        tokenizer_use_fast = use_fast

    return tokenizer_identifier, tokenizer_kwargs, tokenizer_use_fast

