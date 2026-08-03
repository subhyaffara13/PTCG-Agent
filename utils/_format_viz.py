import json

def _format_viz(data, viz_kind, device):
    if device is not None:
        warnings.warn(
            "device argument is deprecated, plots now contain all device",
            FutureWarning,
            stacklevel=3,
        )
    buffer = pickle.dumps(data)
    buffer += b"\x00" * (3 - len(buffer) % 3)
    # Encode the buffer with base64
    encoded_buffer = base64.b64encode(buffer).decode("utf-8")

    json_format = json.dumps([{"name": "snapshot.pickle", "base64": encoded_buffer}])
    return _memory_viz_template.replace("$VIZ_KIND", repr(viz_kind)).replace(
        "$SNAPSHOT", json_format
    )

