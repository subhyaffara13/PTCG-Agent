import logging
import os
import re

def _get_kvstore_for_gcs(ckpt_path: str) -> JsonSpec:
  """Constructs a TensorStore kvstore spec for a GCS path."""
  m = re.fullmatch(_GCS_PATH_RE, ckpt_path, re.DOTALL)
  if m is None:
    raise ValueError(
        'The ckpt_path should contain the bucket name and the '
        f'file path inside the bucket. Got: {ckpt_path}'
    )
  gcs_bucket = m.group(1)
  path_without_bucket = m.group(2) or ''
  # TODO(b/518937340): Consider enabling gcs_grpc by default.
  # TODO(b/518937340): Migrate TENSORSTORE_GCS_BACKEND flag to `Context`.
  gcs_backend = os.environ.get('TENSORSTORE_GCS_BACKEND', 'gcs')
  logging.vlog(
      1, 'Using GCS backend (TENSORSTORE_GCS_BACKEND): %s', gcs_backend
  )
  return {
      'driver': gcs_backend,
      'bucket': gcs_bucket,
      'path': path_without_bucket,
  }


def _get_kvstore_for_gcs(ckpt_path: str):
  m = re.fullmatch('^gs://([^/]*)/(.*)$', ckpt_path)
  if m is None:
    raise ValueError('The ckpt_path should contain the bucket name and the '
                      f'file path inside the bucket. Got: {ckpt_path}')
  bucket = m.group(1)
  path_without_bucket = m.group(2)
  return {'driver': 'gcs', 'bucket': bucket, 'path': path_without_bucket}

