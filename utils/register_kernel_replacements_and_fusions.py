import re
import sys
from pathlib import Path


def register_kernel_replacements_and_fusions(
    cls: "type[PreTrainedModel]",
    config: "PretrainedConfig",
    kernel_config: "KernelConfig",
) -> None:
    if not hasattr(cls, "config_class") or not hasattr(cls.config_class, "model_type"):
        raise ValueError(f"Model {cls.__name__} has no config_class or model_type.")
    model_type = cls.config_class.model_type

    patch_mapping: dict[str, type] = {}
    new_mapping: dict = {}

    # We might need to instantiate the model on meta device.
    # We do it lazily, only if we encounter a fused kernel.
    meta_model = None

    for layer_name, hub_repo in kernel_config.kernel_mapping.items():
        if isinstance(hub_repo, dict):
            if len(hub_repo.values()) != 1:
                raise ValueError(
                    f"Expected exactly one kernel repo regardless of device/mode specificity, got {hub_repo}"
                )
            repo_str = next(iter(hub_repo.values()))
        elif isinstance(hub_repo, str):
            repo_str = hub_repo
        else:
            raise ValueError(f"Invalid hub repo {hub_repo!r} for layer {layer_name!r}")

        repo_id, _, layer_name_in_repo = repo_str.partition(":")
        if not repo_id or not layer_name_in_repo:
            raise ValueError(f"Invalid kernel repo string {repo_str!r} for layer {layer_name!r}")

        if kernel_config.use_local_kernel:
            package_name = repo_id.rstrip("/").split("/")[-1]
            repo = LocalLayerRepository(
                repo_path=Path(repo_id),
                package_name=package_name,
                layer_name=layer_name_in_repo,
            )
        else:
            repo = LayerRepository(repo_id=repo_id, layer_name=layer_name_in_repo)

        kernel_cls = repo.load()

        if kernel_cls is None:
            raise ValueError(f"Could not load kernel class from hub_repo={hub_repo!r}")

        kernel_mod = sys.modules.get(kernel_cls.__module__)
        layout_cls = getattr(kernel_mod, f"{kernel_cls.__name__}Layout", None) if kernel_mod else None

        # Case 1: no fusion.
        if isinstance(layer_name, str):
            # No layout class: stateless kernel, leave for kernels.kernelize.
            if layout_cls is None:
                new_mapping[layer_name] = repo_str
                continue

            # Register the layout class as a monkey patch for the parent module containing the target layer.
            layout_cls.kernel_layer_name = kernel_cls.__name__
            patch_mapping[layer_name] = layout_cls

            # Keep the original repo string so kernelize can replace the layout's forward.
            new_mapping[kernel_cls.__name__] = repo_str

        # Case 2: fusion.
        elif isinstance(layer_name, tuple):
            if layout_cls is None:
                raise ValueError(
                    f"Fused kernel {kernel_cls.__name__!r} requires a companion layout class "
                    f"named '{kernel_cls.__name__}Layout' in the same module."
                )

            layout_cls.kernel_layer_name = kernel_cls.__name__

            glob_patterns = [item[1] for item in layer_name]
            parent_patterns = [p.rsplit(".", 1)[0] for p in glob_patterns]

            if len(set(parent_patterns)) != 1:
                raise ValueError(
                    f"All patterns for a fused kernel must share the same parent module, got {glob_patterns}"
                )

            parent_pattern = parent_patterns[0].replace("*", r"\w+")
            child_names = [p.rsplit(".", 1)[1] for p in glob_patterns]

            if meta_model is None:
                with torch.device("meta"):
                    meta_model = cls(config)

            matched_any = False
            for name, module in meta_model.named_modules():
                if not re.fullmatch(parent_pattern, name):
                    continue
                if not all(hasattr(module, child) for child in child_names):
                    raise ValueError(
                        f"Module {name!r} does not have the expected child modules {child_names} required for "
                        f"the fused kernel {kernel_cls.__name__!r}"
                    )
                matched_any = True
                module_cls = type(module)
                patch_mapping[module_cls.__name__] = make_parent_class_for_kernel_fusion(
                    module_cls, child_names, layout_cls
                )

            if not matched_any:
                raise ValueError(
                    f"No module matched pattern {parent_pattern!r} for fused kernel {kernel_cls.__name__!r}. "
                    f"Provide the full dotted path from the model root."
                )

        register_patch_mapping(patch_mapping, overwrite=True)

        if hasattr(layout_cls, "conversion_mapping"):
            existing = get_checkpoint_conversion_mapping(model_type)
            transforms = list(layout_cls.conversion_mapping)
            if existing is not None:
                transforms = existing + transforms
            register_checkpoint_conversion_mapping(model_type, transforms, overwrite=True)

        new_mapping[kernel_cls.__name__] = repo_str

    kernel_config.kernel_mapping = new_mapping

