import os
from typing import Any, Optional

def get_instance_fn(value: str, config_file_path: Optional[str] = None) -> Any:
    module_name = value
    instance_name = None
    try:
        # Check if value starts with s3:// or gcs://
        if value.startswith("s3://") or value.startswith("gcs://"):
            # Remote module loading is a documented operator feature when
            # invoked from config-file load (``config_file_path`` carries
            # the YAML path). Without that signal the URL is request-body
            # data on an admin endpoint — a one-step admin-to-RCE primitive
            # via ``_load_instance_from_remote_storage``'s ``exec_module``.
            # Register the module under ``litellm_settings`` in the
            # config.yaml instead.
            if config_file_path is None:
                raise ValueError(
                    "Remote module loading (s3://, gcs://) is only "
                    "permitted from the config-file load path. Register "
                    "the module under ``litellm_settings`` in your "
                    "config.yaml instead."
                )
            return _load_instance_from_remote_storage(value, config_file_path)

        # Split the path by dots to separate module from instance
        parts = value.split(".")

        # The module path is all but the last part, and the instance_name is the last part
        module_name = ".".join(parts[:-1])
        instance_name = parts[-1]

        # If config_file_path is provided, use it to determine the module spec and load the module
        if config_file_path is not None:
            directory = os.path.dirname(config_file_path)
            module_file_path = os.path.join(directory, *module_name.split("."))
            module_file_path += ".py"

            # Check if the file exists before trying to load it
            if not os.path.exists(module_file_path):
                raise ImportError(f"Could not find module file {module_file_path}")

            spec = importlib.util.spec_from_file_location(module_name, module_file_path)  # type: ignore
            if spec is None:
                raise ImportError(
                    f"Could not find a module specification for {module_file_path}"
                )
            module = importlib.util.module_from_spec(spec)  # type: ignore
            if spec.loader is None:
                raise ImportError(
                    f"Could not find a module loader for {module_file_path}"
                )
            spec.loader.exec_module(module)  # type: ignore
        else:
            # Dynamically import the module
            module = importlib.import_module(module_name)

        # Get the instance from the module
        instance = getattr(module, instance_name)

        return instance
    except ImportError as e:
        # Re-raise the exception with a user-friendly message
        if instance_name and module_name:
            raise ImportError(
                f"Could not import {instance_name} from {module_name}"
            ) from e
        else:
            raise e
    except Exception as e:
        raise e

