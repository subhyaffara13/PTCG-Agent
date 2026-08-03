from typing import Any, Dict, Optional

def _prepare_azure_extra_body(
    extra_body: Optional[Dict[str, Any]],
    kwargs: Dict[str, Any],
    azure_specific_hyperparams: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Prepare extra_body for Azure fine-tuning API by combining Azure-specific parameters.

    Azure fine-tuning API accepts additional parameters beyond the standard OpenAI spec:
    - trainingType: Type of training (e.g., 1 for supervised fine-tuning)
    - prompt_loss_weight: Weight for prompt loss in training

    These parameters must be passed in the extra_body field when calling the Azure OpenAI SDK.

    Args:
        extra_body: Optional existing extra_body dict
        kwargs: Request kwargs that may contain Azure-specific parameters
        azure_specific_hyperparams: Dict of Azure-specific hyperparameters already extracted

    Returns:
        Dict containing all Azure-specific parameters to be passed in extra_body
    """
    if extra_body is None:
        extra_body = {}

    # Azure-specific root-level parameters
    azure_specific_params = ["trainingType"]
    for param in azure_specific_params:
        if param in kwargs:
            extra_body[param] = kwargs[param]

    # Add Azure-specific hyperparameters
    if azure_specific_hyperparams:
        extra_body.update(azure_specific_hyperparams)

    return extra_body

