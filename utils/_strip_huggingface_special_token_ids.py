
def _strip_huggingface_special_token_ids(
    tokenizer: Tokenizer, tokens: List[int]
) -> List[int]:
    try:
        added_tokens_decoder = tokenizer.get_added_tokens_decoder()
    except Exception:
        return tokens

    special_token_ids = {
        token_id
        for token_id, added_token in added_tokens_decoder.items()
        if getattr(added_token, "special", False)
    }
    if not special_token_ids:
        return tokens
    return [token for token in tokens if token not in special_token_ids]

