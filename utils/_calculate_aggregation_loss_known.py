
def _calculate_aggregation_loss_known(
    logits_aggregation, aggregate_mask, aggregation_labels, use_answer_as_supervision, num_aggregation_labels
):
    """
    Calculates aggregation loss when its type is known during training.

    In the weakly supervised setting, the only known information is that for cell selection examples, "no aggregation"
    should be predicted. For other examples (those that require aggregation), no loss is accumulated. In the setting
    where aggregation type is always known, standard cross entropy loss is accumulated for all examples

    Args:
        logits_aggregation (`torch.FloatTensor` of shape `(batch_size, num_aggregation_labels)`):
            Logits per aggregation operation.
        aggregate_mask (`torch.FloatTensor` of shape `(batch_size, )`):
            A mask set to 1 for examples that should use aggregation functions.
        aggregation_labels (`torch.LongTensor` of shape `(batch_size, )`):
            Aggregation function id for every example in the batch.
        use_answer_as_supervision (`bool`, *optional*):
            Whether to use the answer as the only supervision for aggregation examples.
        num_aggregation_labels (`int`, *optional*, defaults to 0):
            The number of aggregation operators to predict.

    Returns:
        aggregation_loss_known (`torch.FloatTensor` of shape `(batch_size,)`): Aggregation loss (when its type is known
        during training) per example.
    """
    if use_answer_as_supervision:
        # Prepare "no aggregation" targets for cell selection examples.
        target_aggregation = torch.zeros_like(aggregate_mask, dtype=torch.long)
    else:
        # Use aggregation supervision as the target.
        target_aggregation = aggregation_labels

    one_hot_labels = nn.functional.one_hot(target_aggregation, num_classes=num_aggregation_labels).type(torch.float32)
    log_probs = nn.functional.log_softmax(logits_aggregation, dim=-1)

    # torch.FloatTensor[batch_size]
    per_example_aggregation_intermediate = -torch.sum(one_hot_labels * log_probs, dim=-1)
    if use_answer_as_supervision:
        # Accumulate loss only for examples requiring cell selection
        # (no aggregation).
        return per_example_aggregation_intermediate * (1 - aggregate_mask)
    else:
        return per_example_aggregation_intermediate

