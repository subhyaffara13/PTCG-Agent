
def get_storage_transfer_cls(
    src_storage: StorageType, dst_storage: StorageType
) -> Type[StorageTransfer]:
  if src_storage == StorageType.LUSTRE:
    if dst_storage == StorageType.GCS:
      return LustreToGcs
  elif src_storage == StorageType.GCS:
    if dst_storage == StorageType.LUSTRE:
      return GcsToLustre

  raise ValueError(
      f"Unsupported storage transfer: {src_storage} -> {dst_storage}"
  )

