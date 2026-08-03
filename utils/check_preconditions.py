import subprocess

def check_preconditions() -> bool:
  """Runs pre-flight checks. Returns True if cluster exists, False otherwise.

  Raises:
    PreconditionError: If any precondition check fails.

  Returns:
    True if the cluster already exists, False otherwise.
  """
  if _SKIP_PREFLIGHT_CHECKS.value:
    Console.print_warning('Skipping pre-flight checks.')
    return True

  Console.print_step(1, 6, 'Running Pre-flight Checks')

  # 1. Check Dependencies
  dependencies = (_XPK_PATH.value, 'gcloud')
  for dep in dependencies:
    try:
      run_command(['which', dep], capture_output=True, suppress_output=True)
      Console.print_success(f'Found {dep}')
    except subprocess.CalledProcessError as exc:
      Console.print_error(f'{dep} not found in PATH.')
      raise PreconditionError(f'{dep} not found.') from exc

  # 2. Check GCS Access
  if _OUTPUT_DIRECTORY.value.startswith('gs://'):
    bucket = _OUTPUT_DIRECTORY.value.split('/')[2]
    try:
      run_command(
          ['gcloud', 'storage', 'buckets', 'describe', f'gs://{bucket}'],
          capture_output=True,
          suppress_output=True,
      )
      Console.print_success(f'GCS Bucket accessible: gs://{bucket}')
    except subprocess.CalledProcessError as exc:
      Console.print_error(f'Cannot access GCS bucket: gs://{bucket}')
      raise PreconditionError(
          f'Cannot access GCS bucket: gs://{bucket}'
      ) from exc
  else:
    Console.print_info(
        f'Skipping GCS access check for non-GCS path: {_OUTPUT_DIRECTORY.value}'
    )

  # 3. Check Docker Image
  images_to_check = [_DOCKER_IMAGE.value]

  if _ENABLE_PATHWAYS.value:
    images_to_check.extend(
        [_PATHWAYS_SERVER_IMAGE.value, _PATHWAYS_PROXY_IMAGE.value]
    )

  for img in images_to_check:
    # Simple check: if it's a gcr/pkg.dev image, try describing it.
    # If it's local or other, we might skip or just warn.
    if img.startswith(('gcr.io/', 'pkg.dev/')):
      try:
        run_command(
            [
                'gcloud',
                'container',
                'images',
                'describe',
                img,
                f'--project={_PROJECT.value}',
            ],
            capture_output=True,
            suppress_output=True,
        )
        Console.print_success(f'Docker image found: {img}')
      except subprocess.CalledProcessError:
        Console.print_warning(
            f'Could not verify Docker image: {img} (might be private or'
            ' missing)'
        )
    else:
      Console.print_info(f'Skipping verification for non-GCP image: {img}')

  # 4. Check Cluster Existence
  try:
    clusters = run_command(
        [
            _XPK_PATH.value,
            'cluster',
            'list',
            f'--project={_PROJECT.value}',
            f'--zone={_ZONE.value}',
        ],
        capture_output=True,
        suppress_output=not _VERBOSE.value,
    )
  except subprocess.CalledProcessError:
    Console.print_warning('Could not list clusters to verify existence.')
    return False
  else:
    if clusters and _CLUSTER_NAME.value in clusters.split():
      Console.print_success(f'Cluster found: {_CLUSTER_NAME.value}')
      return True

    if _CREATE_CLUSTER.value:
      Console.print_warning(
          f'Cluster {_CLUSTER_NAME.value} not found. Will create it.'
      )
      return False

    Console.print_error(
        f'Cluster {_CLUSTER_NAME.value} not found in'
        f' {_PROJECT.value}/{_ZONE.value}.'
    )
    raise PreconditionError(
        f'Cluster {_CLUSTER_NAME.value} not found. Use --create_cluster to'
        ' create it automatically.'
    )

