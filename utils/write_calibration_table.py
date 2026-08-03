import logging
import os

def write_calibration_table(calibration_cache, dir="."):
    """
    Helper function to write calibration table to files.
    """

    import json  # noqa: PLC0415

    import flatbuffers  # noqa: PLC0415
    import numpy as np  # noqa: PLC0415

    import onnxruntime.quantization.CalTableFlatBuffers.KeyValue as KeyValue  # noqa: PLC0415
    import onnxruntime.quantization.CalTableFlatBuffers.TrtTable as TrtTable  # noqa: PLC0415

    # Use the shared encoder from calibrate.py so write_calibration_table and
    # save_tensors_data produce identical JSON for numpy scalar/array values.
    from onnxruntime.quantization.calibrate import CalibrationCacheEncoder  # noqa: PLC0415

    logging.info(f"calibration cache: {calibration_cache}")

    json_data = json.dumps(calibration_cache, cls=CalibrationCacheEncoder)

    with open(os.path.join(dir, "calibration.json"), "w") as file:
        file.write(json_data)  # use `json.loads` to do the reverse

    # Serialize data using FlatBuffers
    zero = np.array(0)
    builder = flatbuffers.Builder(1024)
    key_value_list = []
    for key in sorted(calibration_cache.keys()):
        values = calibration_cache[key]
        d_values = values.to_dict()
        floats = [
            float(d_values.get("highest", zero).item()),
            float(d_values.get("lowest", zero).item()),
        ]
        value = str(max(floats))

        flat_key = builder.CreateString(key)
        flat_value = builder.CreateString(value)

        KeyValue.KeyValueStart(builder)
        KeyValue.KeyValueAddKey(builder, flat_key)
        KeyValue.KeyValueAddValue(builder, flat_value)
        key_value = KeyValue.KeyValueEnd(builder)

        key_value_list.append(key_value)

    TrtTable.TrtTableStartDictVector(builder, len(key_value_list))
    for key_value in key_value_list:
        builder.PrependUOffsetTRelative(key_value)
    main_dict = builder.EndVector()

    TrtTable.TrtTableStart(builder)
    TrtTable.TrtTableAddDict(builder, main_dict)
    cal_table = TrtTable.TrtTableEnd(builder)

    builder.Finish(cal_table)
    buf = builder.Output()

    with open(os.path.join(dir, "calibration.flatbuffers"), "wb") as file:
        file.write(buf)

    # Deserialize data (for validation)
    if os.environ.get("QUANTIZATION_DEBUG", "0") in (1, "1"):
        cal_table = TrtTable.TrtTable.GetRootAsTrtTable(buf, 0)
        dict_len = cal_table.DictLength()
        for i in range(dict_len):
            key_value = cal_table.Dict(i)
            logging.info(key_value.Key())
            logging.info(key_value.Value())

    # write plain text
    with open(os.path.join(dir, "calibration.cache"), "w") as file:
        for key in sorted(calibration_cache.keys()):
            values = calibration_cache[key]
            d_values = values.to_dict()
            floats = [
                float(d_values.get("highest", zero).item()),
                float(d_values.get("lowest", zero).item()),
            ]
            value = key + " " + str(max(floats))
            file.write(value)
            file.write("\n")

