
def get_bedrock_response_stream_shape():
    """
    Lazily load and cache the bedrock-runtime ResponseStream shape for the process.

    Avoids importing botocore (and logging warnings) unless Bedrock event-stream
    decoding is actually needed.
    """
    return _load_bedrock_response_stream_shape()

