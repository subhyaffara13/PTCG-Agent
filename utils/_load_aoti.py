
def _load_aoti(
    file: str,
    model_name: str,
    run_single_threaded: bool,
    num_runners: int,
    device_idx: int,
) -> AOTICompiledModel:
    loaded_metadata = torch._C._aoti.AOTIModelPackageLoader.load_metadata_from_package(  # type: ignore[attr-defined]
        file, model_name
    )

    device = loaded_metadata["AOTI_DEVICE_KEY"]
    from torch._inductor.codecache import get_device_information

    current_device_info = get_device_information(device)

    for k, v in current_device_info.items():
        if k in loaded_metadata:
            if v != loaded_metadata[k]:
                logger.warning(
                    "Device information mismatch for %s: %s vs %s. "
                    "This could cause some issues when loading the AOTInductor compiled artifacts.",
                    k,
                    v,
                    loaded_metadata[k],
                )

    aoti_compiled_model = AOTICompiledModel(
        torch._C._aoti.AOTIModelPackageLoader(
            file,
            model_name,
            run_single_threaded,
            num_runners,
            device_idx,
        )
    )

    return aoti_compiled_model

