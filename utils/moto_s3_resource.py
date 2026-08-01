
def moto_s3_resource(moto_server):
    boto3 = pytest.importorskip("boto3")
    s3 = boto3.resource("s3", endpoint_url=moto_server)
    return s3

