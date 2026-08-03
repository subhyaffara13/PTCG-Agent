import json
import os
from typing import Any
from pathlib import Path


def _save_pretrained_fastai(
    learner,
    save_directory: str | Path,
    config: dict[str, Any] | None = None,
):
    """
    Saves a fastai learner to `save_directory` in pickle format using the default pickle protocol for the version of python used.

    Args:
        learner (`Learner`):
            The `fastai.Learner` you'd like to save.
        save_directory (`str` or `Path`):
            Specific directory in which you want to save the fastai learner.
        config (`dict`, *optional*):
            Configuration object. Will be uploaded as a .json file. Example: 'https://huggingface.co/espejelomar/fastai-pet-breeds-classification/blob/main/config.json'.

    > [!TIP]
    > Raises the following error:
    >
    >     - [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError)
    >       if the config file provided is not a dictionary.
    """
    _check_fastai_fastcore_versions()

    os.makedirs(save_directory, exist_ok=True)

    # if the user provides config then we update it with the fastai and fastcore versions in CONFIG_TEMPLATE.
    if config is not None:
        if not isinstance(config, dict):
            raise RuntimeError(f"Provided config should be a dict. Got: '{type(config)}'")
        path = os.path.join(save_directory, constants.CONFIG_NAME)
        with open(path, "w") as f:
            json.dump(config, f)

    _create_model_card(Path(save_directory))
    _create_model_pyproject(Path(save_directory))

    # learner.export saves the model in `self.path`.
    learner.path = Path(save_directory)
    os.makedirs(save_directory, exist_ok=True)
    try:
        learner.export(
            fname="model.pkl",
            pickle_protocol=DEFAULT_PROTOCOL,
        )
    except PicklingError:
        raise PicklingError(
            "You are using a lambda function, i.e., an anonymous function. `pickle`"
            " cannot pickle function objects and requires that all functions have"
            " names. One possible solution is to name the function."
        )

