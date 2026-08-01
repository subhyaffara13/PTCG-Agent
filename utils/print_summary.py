
def print_summary(
    *,
    workload_name: str,
    run_id: str,
    project: str,
    zone: str,
    cluster: str,
    output_directory: str,
):
  """Prints a clean summary of the launched workload."""
  if output_directory.startswith('gs://'):
    gcs_bucket = output_directory.replace('gs://', '')
    artifacts_info = (
        f' https://console.cloud.google.com/storage/browser/{gcs_bucket}/{run_id}?project={project}'
    )
  else:
    artifacts_info = f' {output_directory}/{run_id}'

  summary = [
      '',
      '=' * 80,
      f'{Console.BOLD}🚀 Workload Launched Successfully{Console.RESET}',
      '=' * 80,
      f'  🆔 {Console.BOLD}Workload Name:{Console.RESET} {workload_name}',
      f'  🆔 {Console.BOLD}Run ID:{Console.RESET}        {run_id}',
      '',
      (
          f'  📄 {Console.BOLD}Logs:{Console.RESET}      '
          f' https://console.cloud.google.com/logs/query;query=resource.labels.pod_name:"{workload_name}"%0Aresource.labels.container_name:"jax-tpu"?project={project}'
      ),
      f'  📦 {Console.BOLD}Artifacts:{Console.RESET} {artifacts_info}',
      (
          f'  🔍 {Console.BOLD}Status:{Console.RESET}     xpk workload list'
          f' --cluster={cluster} --workload={workload_name} --project={project}'
          f' --zone={zone}'
      ),
      '=' * 80,
      '',
  ]
  print('\n'.join(summary))

