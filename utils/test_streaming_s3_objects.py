
def test_streaming_s3_objects(data):
    # GH 17135
    # botocore gained iteration support in 1.10.47, can now be used in read_*
    pytest.importorskip("botocore", minversion="1.10.47")
    from botocore.response import StreamingBody

    body = StreamingBody(BytesIO(data), content_length=len(data))
    read_csv(body)

