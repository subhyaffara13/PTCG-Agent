
def _collate_word_timestamps(tokenizer, tokens, token_timestamps, language, return_language):
    words, _, token_indices = _combine_tokens_into_words(tokenizer, tokens, language)

    optional_language_field = {"language": language} if return_language else {}

    timings = [
        {
            "text": word,
            "timestamp": (token_timestamps[indices[0]][0], token_timestamps[indices[-1]][1]),
            **optional_language_field,
        }
        for word, indices in zip(words, token_indices)
    ]
    return timings

