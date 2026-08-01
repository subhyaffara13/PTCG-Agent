
def get_tensorstore_spec(
    ckpt_path: str | PathLike[str], ocdbt: bool = True,
    process_idx: int | None = None, arr: jax.Array | None = None,
    driver: str = _TS_ARRAY_DRIVER) -> dict[str, Any]:

  # Normalize path to exclude trailing '/'. In GCS path case, normpath will
  # replace a the double '//' with a single '/' and we need to restore the
  # filesystem type:// prefix for GCS (gs://) and S3 paths (s3://)
  ckpt_path = os.path.normpath(str(ckpt_path))
  ckpt_path = re.sub(r"^(gs|s3):/", r"\1://", ckpt_path)

  # in cases of multi-process writes, we need to write to a different location
  # for each process and finally created a combined symlink to the final
  # location, tensorstore can do this via ts.KvStore.experimental_copy_range_to
  if process_idx is not None:
    _parent, _name = os.path.split(ckpt_path)
    ckpt_path = os.path.join(_parent, _PROCESS_DIR_FORMAT.format(process_idx),
                             _name)

  is_gcs_path = ckpt_path.startswith('gs://')
  is_s3_path = ckpt_path.startswith('s3://')
  spec = {'driver': driver, 'kvstore': {}}

  # use a combined OCDBT store, the actual path is the parent path
  # the name (filename/last part of the path) is the key in the ocdbt kvstore
  entry_key = None
  if ocdbt:
    (ckpt_path, entry_key), org_ckpt_path = os.path.split(ckpt_path), ckpt_path
    if is_gcs_path:
      m = re.fullmatch('^gs://([^/]*)/(.*)$', ckpt_path)
    elif is_s3_path:
      m = re.fullmatch('^s3://([^/]*)/(.*)$', ckpt_path)
    else:
      m = re.match("a", "a")  # make it True
    if m is None:
      raise ValueError('Using OCDBT requires the bucket name, the directory'
                       ' name and the array name, your path is: '
                       f'{org_ckpt_path}')

  if is_gcs_path:
    base_kvstore = _get_kvstore_for_gcs(ckpt_path)
  elif is_s3_path:
    base_kvstore = _get_kvstore_for_s3(ckpt_path)
  else:
    base_kvstore = {'driver': _DEFAULT_BASE_DRIVER, 'path': ckpt_path}

  if ocdbt:
    if not is_gcs_path and not is_s3_path and not os.path.isabs(ckpt_path):
      raise ValueError(f'Checkpoint path should be absolute. Got {ckpt_path}')
    spec['kvstore'] = {'driver': 'ocdbt', 'base': base_kvstore,
                       'path': entry_key}
  else:
    spec['kvstore'] = base_kvstore  # pyrefly: ignore[bad-typed-dict-key]
  # done writing tensorstore spec based on destination path
  # optionally, if array is provided, we can add metadata to the spec
  if arr is not None:
    spec["metadata"] = _get_tensorstore_metadata(
        arr, driver=str(spec["driver"]))
  return spec

