
def num_examples_validator(df: pd.DataFrame) -> Remediation:
    """
    This validator will only print out the number of examples and recommend to the user to increase the number of examples if less than 100.
    """
    MIN_EXAMPLES = 100
    optional_suggestion = (
        ""
        if len(df) >= MIN_EXAMPLES
        else ". In general, we recommend having at least a few hundred examples. We've found that performance tends to linearly increase for every doubling of the number of examples"
    )
    immediate_msg = f"\n- Your file contains {len(df)} prompt-completion pairs{optional_suggestion}"
    return Remediation(name="num_examples", immediate_msg=immediate_msg)

