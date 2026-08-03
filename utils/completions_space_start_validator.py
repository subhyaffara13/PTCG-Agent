from typing import Any

def completions_space_start_validator(df: pd.DataFrame) -> Remediation:
    """
    This validator will suggest to add a space at the start of the completion if it doesn't already exist. This helps with tokenization.
    """

    def add_space_start(x: Any) -> Any:
        x["completion"] = x["completion"].apply(lambda s: ("" if s.startswith(" ") else " ") + s)
        return x

    optional_msg = None
    optional_fn = None
    immediate_msg = None

    if df.completion.str[:1].nunique() != 1 or df.completion.values[0][0] != " ":
        immediate_msg = "\n- The completion should start with a whitespace character (` `). This tends to produce better results due to the tokenization we use. See https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset for more details"
        optional_msg = "Add a whitespace character to the beginning of the completion"
        optional_fn = add_space_start
    return Remediation(
        name="completion_space_start",
        immediate_msg=immediate_msg,
        optional_msg=optional_msg,
        optional_fn=optional_fn,
    )

