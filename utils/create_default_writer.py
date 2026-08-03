from typing import Optional

def create_default_writer(logdir: Optional[str] = None,
                          just_logging: bool = False,
                          **kwargs) -> metric_writers.MetricWriter:
  """Create the default metrics writer.

  See metric_writers.LoggingWriter interface for the API to write the metrics
  and other metadata, e.g. hyper-parameters. Sample usage is as follows:

  writer = metrics.create_default_writer('/some/path')
  writer.write_hparams({"learning_rate": 0.001, "batch_size": 64})
  ...
  # e.g. in training loop.
  writer.write_scalars(step, {"loss": loss})
  ...
  writer.flush()

  Args:
    logdir: Path of the directory to store the metric logs as TF summary files.
      If None, files will not be created.
    just_logging: If true, metrics will be outputted only to INFO log.
    **kwargs: kwargs passed to the CLU default writer.

  Returns:
    a metric_writers.MetricWriter.
  """
  return metric_writers.create_default_writer(
      logdir=logdir, just_logging=just_logging, **kwargs)

