
def _get_order_filtered_deployments(
    healthy_deployments: List[Dict], target_order: Optional[int] = None
) -> List:
    if target_order is not None:
        filtered = [
            d for d in healthy_deployments if _get_deployment_order(d) == target_order
        ]
        if filtered:
            return filtered
        # target_order doesn't match any deployment (e.g., external fallback model) — return all
        return healthy_deployments

    # Default: pick min order group
    _valid_orders: List[int] = [
        o
        for deployment in healthy_deployments
        for o in [_get_deployment_order(deployment)]
        if o is not None
    ]
    min_order: Optional[int] = min(_valid_orders) if _valid_orders else None

    if min_order is not None:
        filtered_deployments = [
            deployment
            for deployment in healthy_deployments
            if _get_deployment_order(deployment) == min_order
        ]

        return filtered_deployments
    return healthy_deployments

