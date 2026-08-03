from typing import Any

def _get_or_add_example_inputs(frame: DynamoFrameType) -> list[Any]:
    key = frame.f_code.co_filename + str(frame.f_code.co_firstlineno)
    example_inputs = get_example_inputs(key)

    if len(example_inputs) < 2:
        example_inputs.append(clone_and_convert_to_meta(frame.f_locals))

    return example_inputs

