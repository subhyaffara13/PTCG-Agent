
def read_profiles_from_yaml(yaml_str: str) -> dict[str, set[OpProfile]]:
    """
    Reads the yaml saved by `save_op_profiles` and returns the operator profiles.
    """

    import yaml

    from torch._export.serde.serialize import (
        _SERIALIZE_TO_TORCH_DTYPE,
        _SERIALIZE_TO_TORCH_LAYOUT,
    )

    def deserialize_tensor_metadata(data: dict) -> TensorMetadata:
        return TensorMetadata(
            rank=data["rank"],
            dtype=_SERIALIZE_TO_TORCH_DTYPE[data["dtype"]],
            device=torch.device(data["device"]),
            layout=_SERIALIZE_TO_TORCH_LAYOUT[data["layout"]],
        )

    def deserialize_op_profile(data: dict) -> OpProfile:
        args_profile = tuple(
            deserialize_tensor_metadata(arg) for arg in data["args_profile"]
        )
        out_profile_data = data["out_profile"]
        out_profile: tuple[TensorMetadata] | TensorMetadata = (
            tuple(deserialize_tensor_metadata(out) for out in out_profile_data)  # type: ignore[assignment]
            if isinstance(out_profile_data, list)
            else deserialize_tensor_metadata(out_profile_data)
        )
        return OpProfile(args_profile=args_profile, out_profile=out_profile)  # type: ignore[arg-type]

    loaded_data = yaml.safe_load(yaml_str)
    loaded_torch_version = loaded_data["torch_version"]

    if loaded_torch_version != get_torch_version():
        raise RuntimeError(
            "Unable to load outdated profile. It was saved with torch version: "
            f"{loaded_torch_version} but the current torch version is: {get_torch_version()}"
        )

    operators_data = loaded_data["operators"]
    return {
        operator: {deserialize_op_profile(profile) for profile in profiles}
        for operator, profiles in operators_data.items()
    }

