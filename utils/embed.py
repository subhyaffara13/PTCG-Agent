
def embed(model: onnx.ModelProto, tuning_results: list[TuningResults], overwrite=False):
    idx = _find_tuning_results_in_props(model.metadata_props)
    assert overwrite or idx <= 0, "the supplied onnx file already have tuning results embedded!"

    if idx >= 0:
        model.metadata_props.pop(idx)

    entry = model.metadata_props.add()
    entry.key = _TUNING_RESULTS_KEY
    entry.value = json.dumps(tuning_results)
    return model

