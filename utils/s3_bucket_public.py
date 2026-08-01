
def s3_bucket_public(moto_s3_resource):
    """
    Create a public S3 bucket using moto.
    """
    bucket_name = f"pandas-test-{uuid.uuid4()}"
    bucket = moto_s3_resource.Bucket(bucket_name)
    bucket.create(ACL="public-read")
    yield bucket
    bucket.objects.delete()
    bucket.delete()

