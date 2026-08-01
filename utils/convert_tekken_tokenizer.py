
def convert_tekken_tokenizer(tokenizer_file: str):
    """Convert a "tekken" tokenizer to a fast Tokenizer."""
    # Tekken format -- need to use the Converter

    from mistral_common.tokens.tokenizers.base import SpecialTokens
    from mistral_common.tokens.tokenizers.mistral import MistralTokenizer

    # Load directly using their lib
    mistral_tokenizer = MistralTokenizer.from_file(tokenizer_file)

    # Extract vocab and special tokens
    vocab = mistral_tokenizer.instruct_tokenizer.tokenizer._tekken_token2id_nospecial
    sorted_tokens = sorted(mistral_tokenizer.instruct_tokenizer.tokenizer._all_special_tokens, key=lambda x: x["rank"])
    all_special = [token["token_str"] for token in sorted_tokens]

    specials_tokens = {token: idx for idx, token in enumerate(all_special)}

    specials_tokens.update(vocab)
    vocab = specials_tokens

    # TODO(juliendenize): expose this in mistral-common to avoid accessing private attributes
    # and improve maintainability
    pattern = mistral_tokenizer.instruct_tokenizer.tokenizer._model._pat_str

    # Convert
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_object=MistralConverter(
            vocab=vocab, additional_special_tokens=all_special, pattern=pattern
        ).converted()
    )

    # Post-process
    tokenizer.add_special_tokens({"additional_special_tokens": all_special})

    MAP_SPECAL = {
        "bos_token": SpecialTokens.bos.value,
        "eos_token": SpecialTokens.eos.value,
        "pad_token": SpecialTokens.pad.value,
        "unk_token": SpecialTokens.unk.value,
    }

    for special_key, special_token in MAP_SPECAL.items():
        if special_token in all_special:
            tokenizer.add_special_tokens({special_key: special_token})

    return tokenizer

