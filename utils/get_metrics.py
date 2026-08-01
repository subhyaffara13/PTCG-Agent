
def get_metrics(device_metrics):
  """Helper utility for pmap, gathering replicated timeseries metric data.

  Args:
   device_metrics: replicated, device-resident pytree of metric data,
     whose leaves are presumed to be a sequence of arrays recorded over time.
  Returns:
   A pytree of unreplicated, host-resident, stacked-over-time arrays useful for
   computing host-local statistics and logging.
  """
  # We select the first element of x in order to get a single copy of a
  # device-replicated metric.
  device_metrics = jax.tree_util.tree_map(
      lambda x: x.addressable_shards[0].data.squeeze(0), device_metrics
  )
  metrics_np = jax.device_get(device_metrics)
  return stack_forest(metrics_np)


def get_metrics(manager):
    bits = []
    bits.append(header("\nRun metrics:"))
    for criteria, _ in constants.CRITERIA:
        bits.append(f"\tTotal issues (by {criteria.lower()}):")
        for rank in constants.RANKING:
            bits.append(
                "\t\t%s: %s"
                % (
                    rank.capitalize(),
                    manager.metrics.data["_totals"][f"{criteria}.{rank}"],
                )
            )
    return "\n".join([str(bit) for bit in bits])


def get_metrics(manager):
    bits = []
    bits.append("\nRun metrics:")
    for criteria, _ in constants.CRITERIA:
        bits.append(f"\tTotal issues (by {criteria.lower()}):")
        for rank in constants.RANKING:
            bits.append(
                "\t\t%s: %s"
                % (
                    rank.capitalize(),
                    manager.metrics.data["_totals"][f"{criteria}.{rank}"],
                )
            )
    return "\n".join([bit for bit in bits])

