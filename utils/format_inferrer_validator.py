
def format_inferrer_validator(df: pd.DataFrame) -> Remediation:
    """
    This validator will infer the likely fine-tuning format of the data, and display it to the user if it is classification.
    It will also suggest to use ada and explain train/validation split benefits.
    """
    ft_type = infer_task_type(df)
    immediate_msg = None
    if ft_type == "classification":
        immediate_msg = f"\n- Based on your data it seems like you're trying to fine-tune a model for {ft_type}\n- For classification, we recommend you try one of the faster and cheaper models, such as `ada`\n- For classification, you can estimate the expected model performance by keeping a held out dataset, which is not used for training"
    return Remediation(name="num_examples", immediate_msg=immediate_msg)

