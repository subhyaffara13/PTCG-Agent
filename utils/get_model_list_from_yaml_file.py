from typing import Any

def get_model_list_from_yaml_file(yaml_file: str) -> list[dict[str, Any]]:
    """Load and validate the model list from a YAML file."""
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
    if not data or "model_list" not in data:
        raise click.ClickException(
            "YAML file must contain a 'model_list' key with a list of models."
        )
    model_list = data["model_list"]
    if not isinstance(model_list, list):
        raise click.ClickException("'model_list' must be a list of model definitions.")
    return model_list

