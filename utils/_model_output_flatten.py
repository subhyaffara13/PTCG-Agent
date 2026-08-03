from typing import Any

def _model_output_flatten(output: ModelOutput) -> tuple[list[Any], list[str]]:
    return list(output.values()), list(output.keys())

