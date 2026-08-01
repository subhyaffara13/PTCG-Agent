
def characters_popularity_compare(
    language: str, ordered_characters: list[str]
) -> float:
    """
    Determine if a ordered characters list (by occurrence from most appearance to rarest) match a particular language.
    The result is a ratio between 0. (absolutely no correspondence) and 1. (near perfect fit).
    Beware that is function is not strict on the match in order to ease the detection. (Meaning close match is 1.)
    """
    if language not in FREQUENCIES:
        raise ValueError(f"{language} not available")  # Defensive:

    character_approved_count: int = 0
    frequencies_language_set: frozenset[str] = _FREQUENCIES_SET[language]
    lang_rank: dict[str, int] = _FREQUENCIES_RANK[language]

    ordered_characters_count: int = len(ordered_characters)
    target_language_characters_count: int = len(FREQUENCIES[language])

    large_alphabet: bool = target_language_characters_count > 26

    expected_projection_ratio: float = (
        target_language_characters_count / ordered_characters_count
    )

    # Pre-built rank dict for ordered_characters (avoids repeated list slicing).
    ordered_rank: dict[str, int] = {
        char: rank for rank, char in enumerate(ordered_characters)
    }

    # Pre-compute characters common to both orderings.
    # Avoids repeated `c in ordered_rank` dict lookups in the inner counts.
    common_chars: list[tuple[int, int]] = [
        (lr, ordered_rank[c]) for c, lr in lang_rank.items() if c in ordered_rank
    ]

    # Pre-extract lr and orr arrays for faster iteration in the inner loop.
    # Plain integer loops with local arrays are much faster under mypyc than
    # generator expression sums over a list of tuples.
    common_count: int = len(common_chars)
    common_lr: list[int] = [p[0] for p in common_chars]
    common_orr: list[int] = [p[1] for p in common_chars]

    for character, character_rank in zip(
        ordered_characters, range(0, ordered_characters_count)
    ):
        if character not in frequencies_language_set:
            continue

        character_rank_in_language: int = lang_rank[character]
        character_rank_projection: int = int(character_rank * expected_projection_ratio)

        if (
            large_alphabet is False
            and abs(character_rank_projection - character_rank_in_language) > 4
        ):
            continue

        if (
            large_alphabet is True
            and abs(character_rank_projection - character_rank_in_language)
            < target_language_characters_count / 3
        ):
            character_approved_count += 1
            continue

        # Count how many characters appear "before" in both orderings,
        # and how many appear "at or after" in both orderings.
        # Single pass over pre-extracted arrays — much faster under mypyc
        # than two generator expression sums.
        before_match_count: int = 0
        after_match_count: int = 0
        for i in range(common_count):
            lr_i: int = common_lr[i]
            orr_i: int = common_orr[i]
            if lr_i < character_rank_in_language:
                if orr_i < character_rank:
                    before_match_count += 1
            else:
                if orr_i >= character_rank:
                    after_match_count += 1

        after_len: int = target_language_characters_count - character_rank_in_language

        if character_rank_in_language == 0 and before_match_count <= 4:
            character_approved_count += 1
            continue

        if after_len == 0 and after_match_count <= 4:
            character_approved_count += 1
            continue

        if (
            character_rank_in_language > 0
            and before_match_count / character_rank_in_language >= 0.4
        ) or (after_len > 0 and after_match_count / after_len >= 0.4):
            character_approved_count += 1
            continue

    return character_approved_count / len(ordered_characters)

