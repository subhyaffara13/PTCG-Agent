
def get_args_parser() -> ArgumentParser:
    """Parse the command line options."""
    parser = ArgumentParser(description="Torch Distributed Elastic Training Launcher")

    def comma_separated_list(value):
        placeholder = "<COMMA_PLACEHOLDER>"
        value = value.replace(",,", placeholder)
        items = value.split(",")
        items = [item.replace(placeholder, ",") for item in items]
        return items

    #
    # Worker/node size related arguments.
    #

    parser.add_argument(
        "--nnodes",
        action=env,
        type=str,
        default="1:1",
        help="Number of nodes, or the range of nodes in form <minimum_nodes>:<maximum_nodes>.",
    )
    parser.add_argument(
        "--nproc-per-node",
        "--nproc_per_node",
        action=env,
        type=str,
        default="1",
        help="Number of workers per node; supported values: [auto, cpu, gpu, xpu, int].",
    )

    #
    # Rendezvous related arguments
    #

    parser.add_argument(
        "--rdzv-backend",
        "--rdzv_backend",
        action=env,
        type=str,
        default="static",
        help="Rendezvous backend.",
    )
    parser.add_argument(
        "--rdzv-endpoint",
        "--rdzv_endpoint",
        action=env,
        type=str,
        default="",
        help="Rendezvous backend endpoint; usually in form <host>:<port>.",
    )
    parser.add_argument(
        "--rdzv-id",
        "--rdzv_id",
        action=env,
        type=str,
        default="none",
        help="User-defined group id.",
    )
    parser.add_argument(
        "--rdzv-conf",
        "--rdzv_conf",
        action=env,
        type=str,
        default="",
        help="Additional rendezvous configuration (<key1>=<value1>,<key2>=<value2>,...).",
    )
    parser.add_argument(
        "--standalone",
        action=check_env,
        help="Start a local standalone rendezvous backend that is represented by a C10d TCP store "
        "on a free port. Useful when launching single-node, multi-worker job. If specified "
        "--rdzv-backend, --rdzv-endpoint, --rdzv-id are auto-assigned and any explicitly set values "
        "are ignored.",
    )

    #
    # User-code launch related arguments.
    #

    parser.add_argument(
        "--max-restarts",
        "--max_restarts",
        action=env,
        type=int,
        default=0,
        help="Maximum number of worker group restarts before failing.",
    )
    parser.add_argument(
        "--monitor-interval",
        "--monitor_interval",
        action=env,
        type=float,
        default=0.1,
        help="Interval, in seconds, to monitor the state of workers.",
    )
    parser.add_argument(
        "--start-method",
        "--start_method",
        action=env,
        type=str,
        default="spawn",
        choices=["spawn", "fork", "forkserver"],
        help="Multiprocessing start method to use when creating workers.",
    )
    parser.add_argument(
        "--event-log-handler",
        "--event_log_handler",
        action=env,
        type=str,
        default="null",
        help="name of a registered event logging handler (see: https://docs.pytorch.org/docs/stable/elastic/events.html)",
    )
    parser.add_argument(
        "--role",
        action=env,
        type=str,
        default="default",
        help="User-defined role for the workers.",
    )
    parser.add_argument(
        "-m",
        "--module",
        action=check_env,
        help="Change each process to interpret the launch script as a Python module, executing "
        "with the same behavior as 'python -m'.",
    )
    parser.add_argument(
        "--no-python",
        "--no_python",
        action=check_env,
        help="Skip prepending the training script with 'python' - just execute it directly. Useful "
        "when the script is not a Python script.",
    )

    parser.add_argument(
        "--run-path",
        "--run_path",
        action=check_env,
        help="Run the training script with runpy.run_path in the same interpreter."
        " Script must be provided as an abs path (e.g. /abs/path/script.py)."
        " Takes precedence over --no-python.",
    )
    parser.add_argument(
        "--log-dir",
        "--log_dir",
        action=env,
        type=str,
        default=None,
        help="Base directory to use for log files (e.g. /var/log/torch/elastic). The same "
        "directory is reused for multiple runs (a unique job-level sub-directory is created with "
        "rdzv_id as the prefix).",
    )
    parser.add_argument(
        "-r",
        "--redirects",
        action=env,
        type=str,
        default="0",
        help="Redirect std streams into a log file in the log directory (e.g. [-r 3] redirects "
        "both stdout+stderr for all workers, [-r 0:1,1:2] redirects stdout for local rank 0 and "
        "stderr for local rank 1).",
    )
    parser.add_argument(
        "-t",
        "--tee",
        action=env,
        type=str,
        default="0",
        help="Tee std streams into a log file and also to console (see --redirects for format).",
    )

    parser.add_argument(
        "--local-ranks-filter",
        "--local_ranks_filter",
        action=env,
        type=str,
        default="",
        help="Only show logs from specified ranks in console (e.g. [--local_ranks_filter=0,1,2] will "
        "only show logs from rank 0, 1 and 2). This will only apply to stdout and stderr, not to"
        "log files saved via --redirect or --tee",
    )

    parser.add_argument(
        "--duplicate-stdout-filters",
        "--duplicate_stdout_filters",
        action=env,
        type=comma_separated_list,
        default=[],
        help="Duplicates logs streamed to stdout to another specified file with a list of filters (e.g. "
        "[--duplicate_stdout_filters 'apple,orange'] will duplicate log lines matching 'apple' "
        "OR 'orange'. An empty filters list won't duplicate any lines. Use double comma to escape a comma) ",
    )

    parser.add_argument(
        "--duplicate-stderr-filters",
        "--duplicate_stderr_filters",
        action=env,
        type=comma_separated_list,
        default=[],
        help="Duplicates logs streamed to stderr to another specified file with a list of filters (e.g. "
        "[--duplicate_stdout_filters 'apple,orange'] will duplicate log lines matching 'apple' "
        "OR 'orange'. An empty filters list won't duplicate any lines. Use double comma to escape a comma) ",
    )

    #
    # Backwards compatible parameters with caffe2.distributed.launch.
    #

    parser.add_argument(
        "--node-rank",
        "--node_rank",
        type=int,
        action=env,
        default=0,
        help="Rank of the node for multi-node distributed training.",
    )
    parser.add_argument(
        "--master-addr",
        "--master_addr",
        default="127.0.0.1",
        type=str,
        action=env,
        help="Address of the master node (rank 0) that only used for static rendezvous. It should "
        "be either the IP address or the hostname of rank 0. For single node multi-proc training "
        "the --master-addr can simply be 127.0.0.1; IPv6 should have the pattern "
        "`[0:0:0:0:0:0:0:1]`.",
    )
    parser.add_argument(
        "--master-port",
        "--master_port",
        default=None,
        type=int,
        action=env,
        help="Port on the master node (rank 0) to be used for communication during distributed "
        "training. It is only used for static rendezvous. Defaults to 29500.",
    )
    parser.add_argument(
        "--local-addr",
        "--local_addr",
        default=None,
        type=str,
        action=env,
        help="Address of the local node. If specified, will use the given address for connection. "
        "Else, will look up the local node address instead. Else, it will be default to local "
        "machine's FQDN.",
    )

    parser.add_argument(
        "--logs-specs",
        "--logs_specs",
        default=None,
        type=str,
        help="torchrun.logs_specs group entrypoint name, value must be type of LogsSpecs. "
        "Can be used to override custom logging behavior.",
    )

    parser.add_argument(
        "--numa-binding",
        "--numa_binding",
        type=str,
        choices=[mode.value for mode in _AffinityMode],
        default=None,
        help="Bind worker processes to CPUs near their assigned GPUs for better performance. "
        "See torch/numa/binding.py for available modes and details.",
    )

    parser.add_argument(
        "--signals-to-handle",
        "--signals_to_handle",
        action=env,
        type=str,
        default="SIGTERM,SIGINT,SIGHUP,SIGQUIT",
        help="Comma-separated list of signals to handle and forward to subprocesses. "
        "Default: SIGTERM,SIGINT,SIGHUP,SIGQUIT. "
        "Common additional signals: SIGUSR1,SIGUSR2 (used in SLURM environments).",
    )

    parser.add_argument(
        "--shutdown-timeout",
        "--shutdown_timeout",
        action=env,
        type=int,
        default=None,
        help="Time in seconds to wait for graceful shutdown of worker processes before "
        "sending SIGKILL. If not specified, uses TORCH_ELASTIC_SHUTDOWN_TIMEOUT environment "
        "variable or defaults to 30 seconds.",
    )

    parser.add_argument(
        "--virtual-local-rank",
        "--virtual_local_rank",
        action=check_env,
        help="Enable virtual local rank mode for workers. When enabled, LOCAL_RANK is set to 0 "
        "for all workers and CUDA_VISIBLE_DEVICES is adjusted so each worker accesses its "
        "assigned GPU at device index 0.",
    )

    #
    # Positional arguments.
    #

    parser.add_argument(
        "training_script",
        type=str,
        help="Full path to the (single GPU) training program/script to be launched in parallel, "
        "followed by all the arguments for the training script.",
    )

    # Rest from the training program.
    parser.add_argument("training_script_args", nargs=REMAINDER)

    return parser

