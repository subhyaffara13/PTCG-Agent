import logging
import os

def cleanup_hns_folders(path: epath.Path) -> None:
  """For a hierarchical namespace bucket, delete empty folders recursively."""
  # pylint: disable=g-import-not-at-top
  from google.cloud import storage_control_v2  # pytype: disable=import-error

  bucket, prefix = parse_gcs_path(path)

  client = storage_control_v2.StorageControlClient()
  project_path = client.common_project_path('_')
  bucket_path = f'{project_path}/buckets/{bucket}'
  folders = set(
      # Format: "projects/{project}/buckets/{bucket}/folders/{folder}"
      folder.name
      for folder in client.list_folders(
          request=storage_control_v2.ListFoldersRequest(
              parent=bucket_path, prefix=prefix.strip('/') + '/'
          )
      )
  )

  while folders:
    parents = set(os.path.dirname(x.rstrip('/')) + '/' for x in folders)
    leaves = folders - parents
    requests = [storage_control_v2.DeleteFolderRequest(name=f) for f in leaves]
    for req in requests:
      client.delete_folder(request=req)
    folders = folders - leaves
    logging.vlog(
        1,
        'Deleted %s folders, %s remaining. [%s][%s]',
        len(leaves),
        len(folders),
        bucket,
        prefix,
    )

