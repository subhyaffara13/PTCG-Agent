
def pr_curve(tag, labels, predictions, num_thresholds=127, weights=None):
    # weird, value > 127 breaks protobuf
    num_thresholds = min(num_thresholds, 127)
    data = compute_curve(
        labels, predictions, num_thresholds=num_thresholds, weights=weights
    )
    pr_curve_plugin_data = PrCurvePluginData(
        version=0, num_thresholds=num_thresholds
    ).SerializeToString()
    plugin_data = SummaryMetadata.PluginData(
        plugin_name="pr_curves", content=pr_curve_plugin_data
    )
    smd = SummaryMetadata(plugin_data=plugin_data)
    tensor = TensorProto(
        dtype="DT_FLOAT",
        float_val=data.reshape(-1).tolist(),
        tensor_shape=TensorShapeProto(
            dim=[
                TensorShapeProto.Dim(size=data.shape[0]),
                TensorShapeProto.Dim(size=data.shape[1]),
            ]
        ),
    )
    return Summary(value=[Summary.Value(tag=tag, metadata=smd, tensor=tensor)])

