
def is_quantized_data_type(qnn_data_type, is_converter_json):
    if is_converter_json:
        # QNN_DATATYPE_UFIXED_POINT_8 QNN_DATATYPE_UFIXED_POINT_16 QNN_DATATYPE_FIXED_POINT_8 QNN_DATATYPE_FIXED_POINT_16
        return qnn_data_type == 0x0408 or qnn_data_type == 0x0416 or qnn_data_type == 0x0308 or qnn_data_type == 0x0316
    else:
        return (
            qnn_data_type == "QNN_DATATYPE_UFIXED_POINT_8"
            or qnn_data_type == "QNN_DATATYPE_UFIXED_POINT_16"
            or qnn_data_type == "QNN_DATATYPE_FIXED_POINT_8"
            or qnn_data_type == "QNN_DATATYPE_FIXED_POINT_16"
        )

