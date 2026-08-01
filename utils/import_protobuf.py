
def import_protobuf(error_message=""):
    if is_sentencepiece_available():
        from sentencepiece import sentencepiece_model_pb2

        return sentencepiece_model_pb2
    if is_protobuf_available():
        import google.protobuf

        if version.parse(google.protobuf.__version__) < version.parse("4.0.0"):
            from transformers.utils import sentencepiece_model_pb2
        else:
            from transformers.utils import sentencepiece_model_pb2_new as sentencepiece_model_pb2
        return sentencepiece_model_pb2
    else:
        raise ImportError(PROTOBUF_IMPORT_ERROR.format(error_message))

