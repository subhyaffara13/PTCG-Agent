
def glue_convert_examples_to_features(
    examples: list[InputExample],
    tokenizer: PreTrainedTokenizer,
    max_length: int | None = None,
    task=None,
    label_list=None,
    output_mode=None,
):
    """
    Loads a data file into a list of `InputFeatures`

    Args:
        examples: List of `InputExamples` containing the examples.
        tokenizer: Instance of a tokenizer that will tokenize the examples
        max_length: Maximum example length. Defaults to the tokenizer's max_len
        task: GLUE task
        label_list: List of labels. Can be obtained from the processor using the `processor.get_labels()` method
        output_mode: String indicating the output mode. Either `regression` or `classification`

    Returns:
        Will return a list of task-specific `InputFeatures` which can be fed to the model.

    """
    warnings.warn(DEPRECATION_WARNING.format("function"), FutureWarning)
    return _glue_convert_examples_to_features(
        examples, tokenizer, max_length=max_length, task=task, label_list=label_list, output_mode=output_mode
    )

