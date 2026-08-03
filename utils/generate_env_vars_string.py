import os

def generate_env_vars_string(*, stable_output: bool = False) -> str:
    """
    Generate a string configuration for environment variables related to Dynamo, Inductor, and Triton.
    """
    if stable_output:
        return "# env var omitted due to stable_output=True"

    allow_list = ["TORCH", "DYNAMO", "INDUCTOR", "TRITON"]
    skip_list = ["TRITON_LIBDEVICE_PATH", "TRITON_PTXAS_PATH", "TRITON_LIBCUDA_PATH"]

    def filter(key: str) -> bool:
        return any(string in key for string in allow_list) and key not in skip_list

    config_lines = [
        f"""os.environ['{key}'] = '{value.replace("'", '"')}'"""
        for key, value in os.environ.items()
        if filter(key)
    ]
    config_string = "\n".join(config_lines)
    return normalize_path_separator(f"""\
import os
{config_string}
    """)

