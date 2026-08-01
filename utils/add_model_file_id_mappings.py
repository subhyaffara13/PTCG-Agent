
def add_model_file_id_mappings(
    healthy_deployments: Union[List[Dict], Dict], responses: List["OpenAIFileObject"]
) -> dict:
    """
    Create a mapping of model id to file id
    {
        "model_id": "file_id",
        "model_id": "file_id",
    }

    `healthy_deployments` may be either a list of deployment dicts (multiple
    matched deployments) or a single deployment dict (when the router resolved
    a specific deployment, e.g. because the requested model matched a
    `model_info.id`). Both shapes must be handled by extracting
    `model_info.id` from each deployment.
    """
    model_file_id_mapping: Dict[str, str] = {}
    deployments_list: List[Dict] = (
        healthy_deployments
        if isinstance(healthy_deployments, list)
        else [healthy_deployments]
    )
    for deployment, response in zip(deployments_list, responses):
        model_id = deployment.get("model_info", {}).get("id")
        if model_id is not None:
            model_file_id_mapping[model_id] = response.id
    return model_file_id_mapping

