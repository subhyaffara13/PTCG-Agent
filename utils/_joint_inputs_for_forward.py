from typing import Any

def _joint_inputs_for_forward(
    joint_inputs: list[Any] | tuple[list[Any], list[Any]],
) -> list[Any]:
    return joint_inputs[0] if isinstance(joint_inputs, tuple) else joint_inputs

