import uuid

def s3_bucket_private(moto_s3_resource):
    """
    Create a private S3 bucket using moto.
    """
    bucket_name = f"cant_get_it-{uuid.uuid4()}"
    bucket = moto_s3_resource.Bucket(bucket_name)
    bucket.create(ACL="private")
    yield bucket
    bucket.objects.delete()
    bucket.delete()

