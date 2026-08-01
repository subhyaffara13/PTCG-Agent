
def qnn_data_type_to_onnx_data_type(qnn_data_type):
    # QNN_DATATYPE_UFIXED_POINT_8 QNN_DATATYPE_UINT_8
    if qnn_data_type == 0x0408 or qnn_data_type == 0x0108:
        return TensorProto.UINT8
    # QNN_DATATYPE_UFIXED_POINT_16 QNN_DATATYPE_UINT_16
    elif qnn_data_type == 0x0416 or qnn_data_type == 0x0116:
        return TensorProto.UINT16
    # QNN_DATATYPE_UFIXED_POINT_32 QNN_DATATYPE_UINT_32
    elif qnn_data_type == 0x0432 or qnn_data_type == 0x0132:
        return TensorProto.UINT32
    # QNN_DATATYPE_UINT_64
    elif qnn_data_type == 0x0164:
        return TensorProto.UINT64
    # QNN_DATATYPE_FIXED_POINT_8 QNN_DATATYPE_INT_8
    elif qnn_data_type == 0x0308 or qnn_data_type == 0x0008:
        return TensorProto.INT8
    # QNN_DATATYPE_FIXED_POINT_16 QNN_DATATYPE_INT_16
    elif qnn_data_type == 0x0316 or qnn_data_type == 0x0016:
        return TensorProto.INT16
    # QNN_DATATYPE_FIXED_POINT_32 QNN_DATATYPE_INT_32
    elif qnn_data_type == 0x0332 or qnn_data_type == 0x0032:
        return TensorProto.INT32
    # QNN_DATATYPE_INT_64
    elif qnn_data_type == 0x0064:
        return TensorProto.INT64
    # QNN_DATATYPE_FLOAT_16
    elif qnn_data_type == 0x0216:
        return TensorProto.FLOAT16
    # QNN_DATATYPE_FLOAT_32
    elif qnn_data_type == 0x0232:
        return TensorProto.FLOAT
    # QNN_DATATYPE_BOOL_8
    elif qnn_data_type == 0x0508:
        return TensorProto.BOOL
    else:
        return TensorProto.UNDEFINED


def qnn_data_type_to_onnx_data_type(qnn_data_type, is_converter_json):
    if is_converter_json:
        # QNN_DATATYPE_UFIXED_POINT_8 QNN_DATATYPE_UINT_8
        if qnn_data_type == 0x0408 or qnn_data_type == 0x0108:
            return TensorProto.UINT8
        # QNN_DATATYPE_UFIXED_POINT_16 QNN_DATATYPE_UINT_16
        elif qnn_data_type == 0x0416 or qnn_data_type == 0x0116:
            return TensorProto.UINT16
        # QNN_DATATYPE_UFIXED_POINT_32 QNN_DATATYPE_UINT_32
        elif qnn_data_type == 0x0432 or qnn_data_type == 0x0132:
            return TensorProto.UINT32
        # QNN_DATATYPE_UINT_64
        elif qnn_data_type == 0x0164:
            return TensorProto.UINT64
        # QNN_DATATYPE_FIXED_POINT_8 QNN_DATATYPE_INT_8
        elif qnn_data_type == 0x0308 or qnn_data_type == 0x0008:
            return TensorProto.INT8
        # QNN_DATATYPE_FIXED_POINT_16 QNN_DATATYPE_INT_16
        elif qnn_data_type == 0x0316 or qnn_data_type == 0x0016:
            return TensorProto.INT16
        # QNN_DATATYPE_FIXED_POINT_32 QNN_DATATYPE_INT_32
        elif qnn_data_type == 0x0332 or qnn_data_type == 0x0032:
            return TensorProto.INT32
        # QNN_DATATYPE_INT_64
        elif qnn_data_type == 0x0064:
            return TensorProto.INT64
        # QNN_DATATYPE_FLOAT_16
        elif qnn_data_type == 0x0216:
            return TensorProto.FLOAT16
        # QNN_DATATYPE_FLOAT_32
        elif qnn_data_type == 0x0232:
            return TensorProto.FLOAT
        # QNN_DATATYPE_BOOL_8
        elif qnn_data_type == 0x0508:
            return TensorProto.BOOL
        else:
            return TensorProto.UNDEFINED
    else:
        # QNN_DATATYPE_UFIXED_POINT_8 QNN_DATATYPE_UINT_8
        if qnn_data_type == "QNN_DATATYPE_UFIXED_POINT_8" or qnn_data_type == "QNN_DATATYPE_UINT_8":
            return TensorProto.UINT8
        # QNN_DATATYPE_UFIXED_POINT_16 QNN_DATATYPE_UINT_16
        elif qnn_data_type == "QNN_DATATYPE_UFIXED_POINT_16" or qnn_data_type == "QNN_DATATYPE_UINT_16":
            return TensorProto.UINT16
        # QNN_DATATYPE_UFIXED_POINT_32 QNN_DATATYPE_UINT_32
        elif qnn_data_type == "QNN_DATATYPE_UFIXED_POINT_32" or qnn_data_type == "QNN_DATATYPE_UINT_32":
            return TensorProto.UINT32
        # QNN_DATATYPE_UINT_64
        elif qnn_data_type == "QNN_DATATYPE_UINT_64":
            return TensorProto.UINT64
        # QNN_DATATYPE_FIXED_POINT_8 QNN_DATATYPE_INT_8
        elif qnn_data_type == "QNN_DATATYPE_FIXED_POINT_8" or qnn_data_type == "QNN_DATATYPE_INT_8":
            return TensorProto.INT8
        # QNN_DATATYPE_FIXED_POINT_16 QNN_DATATYPE_INT_16
        elif qnn_data_type == "QNN_DATATYPE_FIXED_POINT_16" or qnn_data_type == "QNN_DATATYPE_INT_16":
            return TensorProto.INT16
        # QNN_DATATYPE_FIXED_POINT_32 QNN_DATATYPE_INT_32
        elif qnn_data_type == "QNN_DATATYPE_FIXED_POINT_32" or qnn_data_type == "QNN_DATATYPE_INT_32":
            return TensorProto.INT32
        # QNN_DATATYPE_INT_64
        elif qnn_data_type == "QNN_DATATYPE_INT_64":
            return TensorProto.INT64
        # QNN_DATATYPE_FLOAT_16
        elif qnn_data_type == "QNN_DATATYPE_FLOAT_16":
            return TensorProto.FLOAT16
        # QNN_DATATYPE_FLOAT_32
        elif qnn_data_type == "QNN_DATATYPE_FLOAT_32":
            return TensorProto.FLOAT
        # QNN_DATATYPE_BOOL_8
        elif qnn_data_type == "QNN_DATATYPE_BOOL_8":
            return TensorProto.BOOL
        else:
            return TensorProto.UNDEFINED

