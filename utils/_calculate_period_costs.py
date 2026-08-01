
def _calculate_period_costs(
    num_requests, cost_per_request, input_cost, output_cost, margin_cost
):
    """
    Calculate costs for a given number of requests.

    Returns tuple of (total_cost, input_cost, output_cost, margin_cost) or all None if num_requests is None/0.
    """
    if not num_requests:
        return None, None, None, None
    return (
        cost_per_request * num_requests,
        input_cost * num_requests,
        output_cost * num_requests,
        margin_cost * num_requests,
    )

