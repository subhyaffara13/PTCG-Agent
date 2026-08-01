
def custom_scalars(layout):
    categories = []
    for k, v in layout.items():
        charts = []
        for chart_name, chart_metadata in v.items():
            tags = chart_metadata[1]
            if chart_metadata[0] == "Margin":
                if len(tags) != 3:
                    raise AssertionError("len(tags) != 3")
                mgcc = layout_pb2.MarginChartContent(
                    series=[
                        layout_pb2.MarginChartContent.Series(
                            value=tags[0], lower=tags[1], upper=tags[2]
                        )
                    ]
                )
                chart = layout_pb2.Chart(title=chart_name, margin=mgcc)
            else:
                mlcc = layout_pb2.MultilineChartContent(tag=tags)
                chart = layout_pb2.Chart(title=chart_name, multiline=mlcc)
            charts.append(chart)
        categories.append(layout_pb2.Category(title=k, chart=charts))

    layout = layout_pb2.Layout(category=categories)
    plugin_data = SummaryMetadata.PluginData(plugin_name="custom_scalars")
    smd = SummaryMetadata(plugin_data=plugin_data)
    tensor = TensorProto(
        dtype="DT_STRING",
        string_val=[layout.SerializeToString()],
        tensor_shape=TensorShapeProto(),
    )
    return Summary(
        value=[
            Summary.Value(tag="custom_scalars__config__", tensor=tensor, metadata=smd)
        ]
    )

