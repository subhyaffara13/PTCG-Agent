
def set_tensorstore_driver_for_test():
  # Sets TS driver for testing. Within Google, this defaults to `gfile`, which
  # results in issues writing to the OCDBT manifest. When using `gfile` on the
  # local filesystem, write operations are not atomic.
  ts_utils.DEFAULT_DRIVER = 'file'

