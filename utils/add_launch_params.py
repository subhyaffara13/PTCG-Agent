import re

def add_launch_params(
    original: str, kernel_to_params: dict[str, tuple[str, str]]
) -> str:
    # Regex to match the function call in the original string
    pattern = r"(\w+)\.run\((.*)\)"

    def replace(match) -> str:
        # Extract parts from the regex match
        func_name = match.group(1)
        params = match.group(2)
        new_params, grid = kernel_to_params[func_name]
        new_params = merge_params(params.split(", "), new_params.split(", "))

        # Format the new function call
        new_string = f"{func_name}[{grid}]({', '.join(new_params)})"
        return new_string

    transformed = re.sub(pattern, replace, original)

    remove_inductor_wrappers = re.sub(
        r"@triton_heuristics[^@]*@triton.jit",
        r"@triton.jit",
        transformed,
        flags=re.DOTALL,
    )

    return remove_inductor_wrappers

