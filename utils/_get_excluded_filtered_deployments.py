from typing import Dict, List, Optional

def _get_excluded_filtered_deployments(
    healthy_deployments: List[Dict],
    excluded_deployment_ids: Optional[Iterable[str]] = None,
) -> List:
    """
    Filter out deployments whose `model_info.id` appears in `excluded_deployment_ids`.

    Used by weighted-routing failover so a single logical request can re-pick
    across the remaining deployments in the same model group after one of them
    has failed.

    If the filter would leave no deployments, an empty list is returned so the
    caller raises its usual no-deployments error and the weighted-failover
    helper falls through to the cross-group fallback path. Returning the
    original unfiltered list here would re-include the just-failed deployment.
    """
    if not excluded_deployment_ids:
        return healthy_deployments

    excluded_set = set(excluded_deployment_ids)
    return [
        d
        for d in healthy_deployments
        if (d.get("model_info") or {}).get("id") not in excluded_set
    ]

