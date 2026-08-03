from typing import Optional, Union

def normalize_mlflow_name(
    name_str: str,
    qualifiers: Union[str, bytes, dict[str, str], None],
) -> Optional[str]:
    """MLflow purl names are case-sensitive for Azure ML, it is case sensitive and must be kept as-is in the package URL
    For Databricks, it is case insensitive and must be lowercased in the package URL"""
    if isinstance(qualifiers, dict):
        repo_url = qualifiers.get("repository_url")
        if repo_url and "azureml" in repo_url.lower():
            return name_str
        if repo_url and "databricks" in repo_url.lower():
            return name_str.lower()
    if isinstance(qualifiers, str):
        if "azureml" in qualifiers.lower():
            return name_str
        if "databricks" in qualifiers.lower():
            return name_str.lower()
    return name_str

