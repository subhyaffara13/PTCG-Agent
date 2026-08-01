
def create_default_global_load_plan(
    all_plans: list[LoadPlan],
) -> list[LoadPlan]:
    """
    Create global load plan used by DefaultLoadPlanner.

    The default load behavior involved no global coordination and this function
    currently doesn't change the local plans.
    """
    return all_plans

