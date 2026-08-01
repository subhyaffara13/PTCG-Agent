
def _fetch_recommended_models() -> dict[str, str | None]:
    response = get_session().get(f"{constants.ENDPOINT}/api/tasks", headers=build_hf_headers())
    hf_raise_for_status(response)
    return {task: next(iter(details["widgetModels"]), None) for task, details in response.json().items()}

