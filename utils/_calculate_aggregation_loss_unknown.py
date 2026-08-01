
def _calculate_aggregation_loss_unknown(logits_aggregation, aggregate_mask):
    """
    Calculates aggregation loss in the case of answer supervision.

    Args:
        logits_aggregation (`torch.FloatTensor` of shape `(batch_size, num_aggregation_labels)`):
            Logits per aggregation operation.
        aggregate_mask (`torch.FloatTensor` of shape `(batch_size, )`):
            A mask set to 1 for examples that should use aggregation functions

    Returns:
        aggregation_loss_unknown (`torch.FloatTensor` of shape `(batch_size,)`): Aggregation loss (in case of answer
        supervision) per example.
    """
    dist_aggregation = torch.distributions.categorical.Categorical(logits=logits_aggregation)
    # Index 0 corresponds to "no aggregation".
    aggregation_ops_total_mass = torch.sum(dist_aggregation.probs[:, 1:], dim=1)
    # Predict some aggregation in case of an answer that needs aggregation.
    # This increases the probability of all aggregation functions, in a way
    # similar to MML, but without considering whether the function gives the
    # correct answer.
    return -torch.log(aggregation_ops_total_mass) * aggregate_mask

