
def infer_task_type(df: pd.DataFrame) -> str:
    """
    Infer the likely fine-tuning task type from the data
    """
    CLASSIFICATION_THRESHOLD = 3  # min_average instances of each class
    if sum(df.prompt.str.len()) == 0:
        return "open-ended generation"

    if len(df.completion.unique()) < len(df) / CLASSIFICATION_THRESHOLD:
        return "classification"

    return "conditional generation"

