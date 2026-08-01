
def _starts_in_thinking(input_ids, start_ids: list[int]) -> bool:
    """True if the rendered prompt ends with an unclosed thinking block.

    Some reasoning-model chat templates prefill the thinking opener as the final
    prompt tokens (e.g. DeepSeek-R1, QwQ-32B emit ``<think>\\n`` at the end when
    ``add_generation_prompt=True``). In those cases the model resumes *inside*
    the block, so its output contains only ``...reasoning</think>answer`` with
    no opening tag — the streamer must start with ``_inside_thinking=True``.

    The prefill always lands at the tail of the prompt (optionally followed by a
    single whitespace token like ``\\n``), so we only inspect the last few tokens.
    """
    if hasattr(input_ids, "tolist"):
        input_ids = input_ids.tolist()
    if input_ids and isinstance(input_ids[0], list):
        if len(input_ids) != 1:
            return False
        input_ids = input_ids[0]
    n = len(start_ids)
    # Match start_ids at the tail, allowing up to one trailing token (e.g. "\n").
    for trailing in (0, 1):
        if len(input_ids) >= n + trailing:
            end = len(input_ids) - trailing
            if input_ids[end - n : end] == start_ids:
                return True
    return False

