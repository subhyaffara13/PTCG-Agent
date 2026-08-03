import os

def _get_base_dir():
  if 'BUILD_WORKING_DIRECTORY' in os.environ:
    return os.path.join(
        os.environ['BUILD_WORKING_DIRECTORY'],
        'orbax/checkpoint/experimental/v1/_src/testing/compatibility/checkpoints',
    )
  return os.path.join(
      os.path.dirname(__file__),
      'checkpoints',
  )


def _get_base_dir():
  if 'BUILD_WORKING_DIRECTORY' in os.environ:
    return os.path.join(
        os.environ['BUILD_WORKING_DIRECTORY'],
        'orbax/checkpoint/experimental/v1/_src/testing/compatibility/checkpoints',
    )
  return os.path.join(
      os.path.dirname(__file__),
      'checkpoints',
  )

