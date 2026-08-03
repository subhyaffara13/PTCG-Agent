import logging
import os
import sys
from typing import Any

def initialize(linter: PyLinter) -> None:
    """Initialize linter with checkers in this package."""
    register_plugins(linter, __path__[0])


def initialize(linter: PyLinter) -> None:
    """Initialize linter with checkers in the extensions' directory."""
    register_plugins(linter, __path__[0])


def initialize(linter: PyLinter) -> None:
    """Initialize linter with reporters in this package."""
    utils.register_plugins(linter, __path__[0])


def initialize(recorder: MetricRecorder) -> None:
  """Registers a recorder and binds its methods to JAX monitoring listeners."""
  global _initialized

  with _init_lock:
    _recorders.append(recorder)

    if _initialized:
      return

    from jax import monitoring as jax_monitoring  # pylint: disable=g-import-not-at-top

    def _proxy_record_event(metric_name: str, **kwargs: Any) -> None:
      with _init_lock:
        recorders_snapshot = _recorders[:]
      for r in recorders_snapshot:
        r.record_event(metric_name, **kwargs)

    def _proxy_record_scalar(
        metric_name: str, value: float | int, **kwargs: Any
    ) -> None:
      with _init_lock:
        recorders_snapshot = _recorders[:]
      for r in recorders_snapshot:
        r.record_scalar(metric_name, value, **kwargs)

    def _proxy_record_duration(
        metric_name: str, duration: float | int, **kwargs: Any
    ) -> None:
      with _init_lock:
        recorders_snapshot = _recorders[:]
      for r in recorders_snapshot:
        r.record_duration(metric_name, duration, **kwargs)

    jax_monitoring.register_event_listener(_proxy_record_event)
    jax_monitoring.register_scalar_listener(_proxy_record_scalar)
    jax_monitoring.register_event_duration_secs_listener(_proxy_record_duration)

    _initialized = True
    logging.info('Installed JAX monitoring proxy listeners for Orbax.')


def initialize(game, train_meta_solver, eval_meta_solver, policy_init,
               ignore_repeats, br_selection):
  """Return initialized data structures."""
  num_players = game.num_players()

  # Initialize.
  iteration = 0
  per_player_repeats = [[] for _ in range(num_players)]
  per_player_policies = [[] for _ in range(num_players)]
  joint_policies = {}  # Eg. (1, 0): Joint policy.
  joint_returns = {}
  meta_games = []
  train_meta_dists = []
  eval_meta_dists = []
  train_meta_values = []
  eval_meta_values = []
  train_meta_gaps = []
  eval_meta_gaps = []

  # Initialize policies.
  per_player_new_policies = [
      [initialize_policy(game, player, policy_init)]
      for player in range(num_players)]
  per_player_gaps_train = [[1.0] for _ in range(num_players)]
  per_player_num_novel_policies = add_new_policies(
      per_player_new_policies, per_player_gaps_train, per_player_repeats,
      per_player_policies, joint_policies, joint_returns, game, br_selection)
  del per_player_num_novel_policies
  add_meta_game(
      meta_games,
      per_player_policies,
      joint_returns)
  add_meta_dist(
      train_meta_dists, train_meta_values, train_meta_solver,
      meta_games[-1], per_player_repeats, ignore_repeats)
  add_meta_dist(
      eval_meta_dists, eval_meta_values, eval_meta_solver,
      meta_games[-1], per_player_repeats, ignore_repeats)

  return (
      iteration,
      per_player_repeats,
      per_player_policies,
      joint_policies,
      joint_returns,
      meta_games,
      train_meta_dists,
      eval_meta_dists,
      train_meta_values,
      eval_meta_values,
      train_meta_gaps,
      eval_meta_gaps)


def initialize(coordinator_address: str | None = None,
               num_processes: int | None = None,
               process_id: int | None = None,
               local_device_ids: int | Sequence[int] | None = None,
               cluster_detection_method: str | None = None,
               initialization_timeout: int = 300,
               heartbeat_timeout_seconds: int = 100,
               shutdown_timeout_seconds: int = 300,
               coordinator_bind_address: str | None = None,
               slice_index: int | None = None,
               partition_index: int | None = None):
  """Initializes the JAX distributed system.

  Calling :func:`~jax.distributed.initialize` prepares JAX for execution on
  multi-host GPU and Cloud TPU. :func:`~jax.distributed.initialize` must be
  called before performing any JAX computations.

  The JAX distributed system serves a number of roles:

    * It allows JAX processes to discover each other and share topology information,
    * It performs health checking, ensuring that all processes shut down if any process dies, and
    * It is used for distributed checkpointing.

  If you are using TPU, Slurm, or Open MPI, all arguments are optional: if omitted, they
  will be chosen automatically.

  The ``cluster_detection_method`` may be used to choose a specific method for detecting those
  distributed arguments. You may pass any of the automatic ``spec_detect_methods`` to this
  argument though it is not necessary in the TPU, Slurm, or Open MPI cases.  For other MPI
  installations, if you have a functional ``mpi4py`` installed, you may pass
  ``cluster_detection_method="mpi4py"`` to bootstrap the required arguments.

  Otherwise, you must provide the ``coordinator_address``,
  ``num_processes``, ``process_id``, and ``local_device_ids`` arguments
  to :func:`~jax.distributed.initialize`. When all four arguments are provided, cluster
  environment auto detection will be skipped.

  Please note: on some systems, particularly HPC clusters that only access external networks
  through proxy variables such as HTTP_PROXY, HTTPS_PROXY, etc., the call to
  :func:`~jax.distributed.initialize` may timeout.  You may need to unset these variables
  prior to application launch.

  Args:
    coordinator_address: the IP address of process `0` and a port on which that
      process should launch a coordinator service. The choice of
      port does not matter, so long as the port is available on the coordinator
      and all processes agree on the port.
      May be ``None`` only on supported environments, in which case it will be chosen automatically.
      Note that special addresses like ``localhost`` or ``127.0.0.1`` usually mean that the program
      will bind to a local interface and are not suitable when running in a multi-host environment.
    num_processes: Number of processes. May be ``None`` only on supported environments, in
      which case it will be chosen automatically.
    process_id: The ID number of the current process. The ``process_id`` values across
      the cluster must be a dense range ``0``, ``1``, ..., ``num_processes - 1``.
      May be ``None`` only on supported environments; if ``None`` it will be chosen automatically.
    local_device_ids: Restricts the visible devices of the current process to ``local_device_ids``.
      If ``None``, defaults to all local devices being visible to the process except when processes
      are launched via Slurm and Open MPI on GPUs. In that case, it will default to a single device per process.
    cluster_detection_method: An optional string to attempt to autodetect the configuration of the distributed
      run.  Note that "mpi4py" method requires you to have a working ``mpi4py`` install in your environment,
      and launch the applicatoin with an MPI-compatible job launcher such as ``mpiexec`` or ``mpirun``.
      Legacy auto-detect options "ompi" (OMPI) and "slurm" (Slurm) remain enabled. "deactivate" bypasses
      automatic cluster detection.
    initialization_timeout: Time period (in seconds) for which connection will
      be retried. If the initialization takes more than the timeout specified,
      the initialization will error. Defaults to 300 secs i.e. 5 mins.
    heartbeat_timeout_seconds: The time (in seconds) after which a process is
      considered dead if it hasn't successfully sent any heartbeats. Defaults
      to 100 seconds.
    shutdown_timeout_seconds: The time (in seconds) a terminating process will
      wait for all other processes to also terminate. Defaults to 300 seconds.
    coordinator_bind_address: the address and port to which the coordinator service
      on process `0` should bind. If this is not specified, the default is to bind to
      all available addresses on the same port as ``coordinator_address``. On systems
      that have multiple network interfaces per node it may be insufficient to only
      have the coordinator service listen on one address/interface.
    slice_index: DEPRECATED: Use ``partition_index`` instead.
    partition_index: The partition index assigned to this process' local devices. If any process sets ``partition_index``,
      then all processes must do so. If ``None`` the partition indices will be chosen automatically.

  Raises:
    RuntimeError: If :func:`~jax.distributed.initialize` is called more than once
      or if called after the backend is already initialized.

  Examples:

  Suppose there are two GPU processes, and process 0 is the designated coordinator
  with address ``10.0.0.1:1234``. To initialize the GPU cluster, run the
  following commands before anything else.

  On process 0:

  >>> jax.distributed.initialize(coordinator_address='10.0.0.1:1234', num_processes=2, process_id=0)  # doctest: +SKIP

  On process 1:

  >>> jax.distributed.initialize(coordinator_address='10.0.0.1:1234', num_processes=2, process_id=1)  # doctest: +SKIP
  """
  if xla_bridge.backends_are_initialized():
    raise RuntimeError("jax.distributed.initialize() must be called before "
                        "any JAX calls that might initialise the XLA backend. "
                        "This includes any computation, but also calls to jax.devices, jax.device_put, and others.")
  if partition_index is None:
    if slice_index is not None:
      # Deprecation added 2025-08-05. Should be removed after 3 months.
      warnings.warn(
          '`slice_index` has been deprecated. Please use `partition_index` instead.',
          DeprecationWarning,
      )
    partition_index = slice_index
  global_state.initialize(coordinator_address, num_processes, process_id,
                          local_device_ids, cluster_detection_method,
                          initialization_timeout, coordinator_bind_address,
                          heartbeat_timeout_seconds=heartbeat_timeout_seconds,
                          shutdown_timeout_seconds=shutdown_timeout_seconds,
                          partition_index=partition_index)


def initialize():
    """Initialize arguments and output formats."""
    valid = True

    # #################### Parse Args #########################################
    parser = argparse.ArgumentParser(
        description="Bandit Baseline - Generates Bandit results compared to "
        "a baseline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Additional Bandit arguments such as severity filtering (-ll) "
        "can be added and will be passed to Bandit.",
    )
    if sys.version_info >= (3, 14):
        parser.suggest_on_error = True
        parser.color = False

    parser.add_argument(
        "targets",
        metavar="targets",
        type=str,
        nargs="+",
        help="source file(s) or directory(s) to be tested",
    )

    parser.add_argument(
        "-f",
        dest="output_format",
        action="store",
        default="terminal",
        help="specify output format",
        choices=valid_baseline_formats,
    )

    args, _ = parser.parse_known_args()

    # #################### Setup Output #######################################
    # set the output format, or use a default if not provided
    output_format = (
        args.output_format if args.output_format else default_output_format
    )

    if output_format == default_output_format:
        LOG.info("No output format specified, using %s", default_output_format)

    # set the report name based on the output format
    report_fname = f"{report_basename}.{output_format}"

    # #################### Check Requirements #################################
    if git is None:
        LOG.error("Git not available, reinstall with baseline extra")
        valid = False
        return (None, None, None)

    try:
        repo = git.Repo(os.getcwd())

    except git.exc.InvalidGitRepositoryError:
        LOG.error("Bandit baseline must be called from a git project root")
        valid = False

    except git.exc.GitCommandNotFound:
        LOG.error("Git command not found")
        valid = False

    else:
        if repo.is_dirty():
            LOG.error(
                "Current working directory is dirty and must be " "resolved"
            )
            valid = False

    # if output format is specified, we need to be able to write the report
    if output_format != default_output_format and os.path.exists(report_fname):
        LOG.error("File %s already exists, aborting", report_fname)
        valid = False

    # Bandit needs to be able to create this temp file
    if os.path.exists(baseline_tmp_file):
        LOG.error(
            "Temporary file %s needs to be removed prior to running",
            baseline_tmp_file,
        )
        valid = False

    # we must validate -o is not provided, as it will mess up Bandit baseline
    if "-o" in bandit_args:
        LOG.error("Bandit baseline must not be called with the -o option")
        valid = False

    return (output_format, repo, report_fname) if valid else (None, None, None)

