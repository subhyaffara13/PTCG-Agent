
def _get_kvstore_for_s3(ckpt_path: str):
  m = re.fullmatch('^s3://([^/]*)/(.*)$', ckpt_path, re.DOTALL)
  if m is None:
    raise ValueError('The ckpt_path should contain the bucket name and the '
                      f'file path inside the bucket. Got: {ckpt_path}')
  bucket = m.group(1)
  path_without_bucket = m.group(2)
  return {'driver': 's3', 'bucket': bucket, 'path': path_without_bucket}

