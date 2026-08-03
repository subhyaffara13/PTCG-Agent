import logging
import os

def initialize_from_env() -> None:
  """Initializes monitoring based on environment and build type."""

  enable_telemetry = os.environ.get(
      'ENABLE_ORBAX_PROMETHEUS_TELEMETRY', 'false'
  )
  if enable_telemetry.lower() == 'true':
    try:
      from orbax.checkpoint._src.logging import prometheus_monitoring  # pylint: disable=g-import-not-at-top
      import multiprocessing  # pylint: disable=g-import-not-at-top

      env_port = os.environ.get('ORBAX_PROMETHEUS_PORT')
      default_port = _DEFAULT_PROMETHEUS_PORT
      if env_port:
        try:
          default_port = int(env_port)
        except ValueError:
          logging.warning(
              'Invalid ORBAX_PROMETHEUS_PORT "%s". Falling back to default %d.',
              env_port,
              _DEFAULT_PROMETHEUS_PORT,
          )
      port = (
          default_port
          if multiprocessing.current_process().name == 'MainProcess'
          else 0
      )
      initialize(prometheus_monitoring.PrometheusMonitoring(port=port))
    except ImportError as e:
      logging.warning('Failed to import PrometheusMonitoring: %s', e)

