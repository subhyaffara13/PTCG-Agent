
def _return_openai_tokenizer(model: str) -> SelectTokenizerResponse:
    return {"type": "openai_tokenizer", "tokenizer": _get_default_encoding()}

