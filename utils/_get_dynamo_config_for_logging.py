import json
from typing import Any

def _get_dynamo_config_for_logging() -> str | None:
    def clean_for_json(d: dict[str, Any]) -> dict[str, Any]:
        blocklist = {
            "TYPE_CHECKING",
            "log_file_name",
            "verbose",
            "repro_after",
            "repro_level",
            "repro_forward_only",
            "repro_tolerance",
            "repro_ignore_non_fp",
            "same_two_models_use_fp64",
            "base_dir",
            "debug_dir_root",
            "_save_config_ignore",
            "log_compilation_metrics",
            "inject_BUILD_SET_unimplemented_TESTING_ONLY",
            "_autograd_backward_strict_mode_banned_ops",
            "reorderable_logging_functions",
            "ignore_logger_methods",
            "ignore_logging_functions",
            "traceable_tensor_subclasses",
            "nontraceable_tensor_subclasses",
            "_custom_ops_profile",
        }

        return {
            key: sorted(value) if isinstance(value, set) else value
            for key, value in d.items()
            if key not in blocklist
        }

    config_dict = clean_for_json(config.get_config_copy())
    return json.dumps(config_dict, sort_keys=True)

