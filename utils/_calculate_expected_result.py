
def _calculate_expected_result(
    dist_per_cell, numeric_values, numeric_values_scale, input_mask_float, logits_aggregation, config
):
    """
    Calculates the expected result given cell and aggregation probabilities.

    Args:
        dist_per_cell (`torch.distributions.Bernoulli`):
            Cell selection distribution for each cell.
        numeric_values (`torch.FloatTensor` of shape `(batch_size, seq_length)`):
            Numeric values of every token. Nan for tokens which are not numeric values.
        numeric_values_scale (`torch.FloatTensor` of shape `(batch_size, seq_length)`):
            Scale of the numeric values of every token.
        input_mask_float (`torch.FloatTensor` of shape `(batch_size, seq_length)`):
            Mask for the table, without question tokens and table headers.
        logits_aggregation (`torch.FloatTensor` of shape `(batch_size, num_aggregation_labels)`):
            Logits per aggregation operation.
        config ([`TapasConfig`]):
            Model configuration class with all the hyperparameters of the model

    Returns:
        expected_result (`torch.FloatTensor` of shape `(batch_size,)`): The expected result per example.
    """
    if config.use_gumbel_for_cells:
        gumbel_dist = torch.distributions.RelaxedBernoulli(
            # The token logits where already divided by the temperature and used for
            # computing cell selection errors so we need to multiply it again here
            temperature=config.temperature,
            logits=dist_per_cell.logits * config.temperature,
        )
        scaled_probability_per_cell = gumbel_dist.sample()
    else:
        scaled_probability_per_cell = dist_per_cell.probs

    # <float32>[batch_size, seq_length]
    scaled_probability_per_cell = (scaled_probability_per_cell / numeric_values_scale) * input_mask_float
    count_result = torch.sum(scaled_probability_per_cell, dim=1)
    numeric_values_masked = torch.where(
        torch.isnan(numeric_values), torch.zeros_like(numeric_values), numeric_values
    )  # Mask non-numeric table values to zero.
    sum_result = torch.sum(scaled_probability_per_cell * numeric_values_masked, dim=1)
    avg_approximation = config.average_approximation_function
    if avg_approximation == AverageApproximationFunction.RATIO:
        average_result = sum_result / (count_result + EPSILON_ZERO_DIVISION)
    elif avg_approximation == AverageApproximationFunction.FIRST_ORDER:
        # The sum of all probabilities except that correspond to other cells
        # Ex here stands for expectation, more explicitly the expectation of the sum of N-1 Bernoulli random variables plus
        # the constant 1, which is computed as adding all N expected values and subtracting the extra one. It corresponds to X_c
        # in Appendix D of the original TAPAS paper which is trying to approximate the average of a random set.
        ex = torch.sum(scaled_probability_per_cell, dim=1, keepdim=True) - scaled_probability_per_cell + 1
        average_result = torch.sum(numeric_values_masked * scaled_probability_per_cell / ex, dim=1)
    elif avg_approximation == AverageApproximationFunction.SECOND_ORDER:
        # The sum of all probabilities except that correspond to other cells
        ex = torch.sum(scaled_probability_per_cell, dim=1, keepdim=True) - scaled_probability_per_cell + 1
        pointwise_var = scaled_probability_per_cell * (1 - scaled_probability_per_cell)
        var = torch.sum(pointwise_var, dim=1, keepdim=True) - pointwise_var

        multiplier = (var / torch.square(ex) + 1) / ex
        average_result = torch.sum(numeric_values_masked * scaled_probability_per_cell * multiplier, dim=1)
    else:
        raise ValueError(f"Invalid average_approximation_function: {config.average_approximation_function}")

    if config.use_gumbel_for_aggregation:
        gumbel_dist = torch.distributions.RelaxedOneHotCategorical(
            config.aggregation_temperature, logits=logits_aggregation[:, 1:]
        )
        # <float32>[batch_size, num_aggregation_labels - 1]
        aggregation_op_only_probs = gumbel_dist.sample()
    else:
        # <float32>[batch_size, num_aggregation_labels - 1]
        aggregation_op_only_probs = nn.functional.softmax(
            logits_aggregation[:, 1:] / config.aggregation_temperature, dim=-1
        )

    all_results = torch.cat(
        [
            torch.unsqueeze(sum_result, dim=1),
            torch.unsqueeze(average_result, dim=1),
            torch.unsqueeze(count_result, dim=1),
        ],
        dim=1,
    )

    expected_result = torch.sum(all_results * aggregation_op_only_probs, dim=1)
    return expected_result

