
def handle_nested_budget_structure_in_organization_update_request(
    raw_data: dict,
) -> dict:
    """
    Transform organization update request to handle UI payload format.

    The UI sends nested budget data in 'litellm_budget_table', but our
    model expects flat budget fields at the top level.
    """
    transformed_data = raw_data.copy()

    # Handle nested budget structure from UI
    if "litellm_budget_table" in transformed_data:
        budget_data = transformed_data.pop("litellm_budget_table", {})
        if budget_data:
            # Extract valid budget fields and merge into top level
            budget_fields = LiteLLM_BudgetTable.model_fields.keys()
            for key, value in budget_data.items():
                if key in budget_fields and value is not None:
                    transformed_data[key] = value

    return transformed_data

