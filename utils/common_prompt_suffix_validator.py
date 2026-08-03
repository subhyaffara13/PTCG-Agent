from typing import Any

def common_prompt_suffix_validator(df: pd.DataFrame) -> Remediation:
    """
    This validator will suggest to add a common suffix to the prompt if one doesn't already exist in case of classification or conditional generation.
    """
    error_msg = None
    immediate_msg = None
    optional_msg = None
    optional_fn = None  # type: ignore

    # Find a suffix which is not contained within the prompt otherwise
    suggested_suffix = "\n\n### =>\n\n"
    suffix_options = [
        " ->",
        "\n\n###\n\n",
        "\n\n===\n\n",
        "\n\n---\n\n",
        "\n\n===>\n\n",
        "\n\n--->\n\n",
    ]
    for suffix_option in suffix_options:
        if suffix_option == " ->":
            if df.prompt.str.contains("\n").any():
                continue
        if df.prompt.str.contains(suffix_option, regex=False).any():
            continue
        suggested_suffix = suffix_option
        break
    display_suggested_suffix = suggested_suffix.replace("\n", "\\n")

    ft_type = infer_task_type(df)
    if ft_type == "open-ended generation":
        return Remediation(name="common_suffix")

    def add_suffix(x: Any, suffix: Any) -> Any:
        x["prompt"] += suffix
        return x

    common_suffix = get_common_xfix(df.prompt, xfix="suffix")
    if (df.prompt == common_suffix).all():
        error_msg = f"All prompts are identical: `{common_suffix}`\nConsider leaving the prompts blank if you want to do open-ended generation, otherwise ensure prompts are different"
        return Remediation(name="common_suffix", error_msg=error_msg)

    if common_suffix != "":
        common_suffix_new_line_handled = common_suffix.replace("\n", "\\n")
        immediate_msg = f"\n- All prompts end with suffix `{common_suffix_new_line_handled}`"
        if len(common_suffix) > 10:
            immediate_msg += f". This suffix seems very long. Consider replacing with a shorter suffix, such as `{display_suggested_suffix}`"
        if df.prompt.str[: -len(common_suffix)].str.contains(common_suffix, regex=False).any():
            immediate_msg += f"\n  WARNING: Some of your prompts contain the suffix `{common_suffix}` more than once. We strongly suggest that you review your prompts and add a unique suffix"

    else:
        immediate_msg = "\n- Your data does not contain a common separator at the end of your prompts. Having a separator string appended to the end of the prompt makes it clearer to the fine-tuned model where the completion should begin. See https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset for more detail and examples. If you intend to do open-ended generation, then you should leave the prompts empty"

    if common_suffix == "":
        optional_msg = f"Add a suffix separator `{display_suggested_suffix}` to all prompts"

        def optional_fn(x: Any) -> Any:
            return add_suffix(x, suggested_suffix)

    return Remediation(
        name="common_completion_suffix",
        immediate_msg=immediate_msg,
        optional_msg=optional_msg,
        optional_fn=optional_fn,
        error_msg=error_msg,
    )

