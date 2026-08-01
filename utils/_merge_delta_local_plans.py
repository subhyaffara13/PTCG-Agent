
def _merge_delta_local_plans(
    cached_plans: list[SavePlan],
    delta_plans: list[SavePlan],
) -> list[SavePlan]:
    """
    Merge a list of delta plans into a single plan.

    Args:
        cached_plans (List[SavePlan]): A list of cached plans.
        delta_plans (List[SavePlan]): A list of delta plans to merge. It can contain empty plans

    Returns:
        A single merged plan. If a delta plan is not usable, use the cached plan. Otherwise, use the delta plan.
    """
    merged_plans = []

    for cached_plan, delta_plan in zip(cached_plans, delta_plans):
        if delta_plan and not delta_plan.usable:
            merged_plans.append(cached_plan)
        else:
            merged_plans.append(delta_plan)

    return merged_plans

