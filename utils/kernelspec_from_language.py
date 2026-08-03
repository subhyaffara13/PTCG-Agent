import os
import sys

def kernelspec_from_language(language):
    """Return the python kernel that matches the current env, or the first kernel that matches the given language"""
    if language == "python":
        # Return the kernel that matches the current Python executable
        for name in find_kernel_specs():
            kernel_specs = get_kernel_spec(name)
            cmd = kernel_specs.argv[0]
            if kernel_specs.language == "python" and os.path.isfile(cmd) and os.path.samefile(cmd, sys.executable):
                return {
                    "name": name,
                    "language": language,
                    "display_name": kernel_specs.display_name,
                }
        raise ValueError(
            f"No kernel found that matches the current python executable {sys.executable}\n"
            + "Install one with 'python -m ipykernel install --name kernel_name [--user]'"
        )

    for name in find_kernel_specs():
        kernel_specs = get_kernel_spec(name)
        if same_language(kernel_specs.language, language):
            return {
                "name": name,
                "language": language,
                "display_name": kernel_specs.display_name,
            }

    raise ValueError(f"No kernel found for the language {language}")

