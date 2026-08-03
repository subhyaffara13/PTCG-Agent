import os

def setup_environment(args):
    """Sets up the output directory and logging."""
    run_output_dir = append_timestamp_to_dir(args.output_dir, append=args.append_timestamp_to_dir)
    os.makedirs(run_output_dir, exist_ok=True)
    setup_logger(run_output_dir, "run_sample")
    log_launch_command()
    log_git_hash()

    # Save configs
    config_dump_dir = os.path.join(run_output_dir, "configs")
    base_config_path = os.path.join(config_dump_dir, "base_config.yaml")
    agents_pool_dir = os.path.join(config_dump_dir, "pool_of_agents")
    os.makedirs(agents_pool_dir, exist_ok=True)
    for config_path in args.agent_pool_configs:
        shutil.copy(config_path, agents_pool_dir)
    shutil.copy(args.base_game_config, base_config_path)
    logger.info(f"Copied experiment configs to {config_dump_dir}")
    return run_output_dir

