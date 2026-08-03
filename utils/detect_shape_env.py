from typing import Any

def detect_shape_env(inputs: Any = None):
    shape_envs = []

    for i, flat_input in enumerate(inputs):
        if isinstance(flat_input, torch.SymInt):
            shape_envs.append((flat_input.node.shape_env, "symint input", i))

    if shape_envs:
        shape_env, desc1, i1 = shape_envs[0]
        for m, desc2, i2 in shape_envs[1:]:
            if shape_env is not m:
                raise AssertionError(
                    f"shape env ({shape_env}) from {desc1} {i1} doesn't match mode ({m}) from {desc2} {i2}\n\n"
                    f"shape env from {desc1} {i1} allocated at:\n{shape_env.stack}\n"
                    f"shape env from {desc2} {i2} allocated at:\n{m.stack}"
                )
        return shape_env
    else:
        return None

