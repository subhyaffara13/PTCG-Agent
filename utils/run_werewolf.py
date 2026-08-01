
def run_werewolf(output_dir, base_name, config, agents, debug):
    """
    Runs a game of Werewolf, saves the replay, and logs the execution time.

    Args:
        output_dir (str): The directory where the output files will be saved.
        base_name (str): The base name for the output files (HTML, JSON).
        config (dict): The configuration for the Werewolf environment.
        agents (list): A list of agents to participate in the game.
        debug (bool): A flag to enable or disable debug mode.
    """
    start_time = time.time()
    logger.info(f"Results saved to {output_dir}.")
    os.makedirs(output_dir, exist_ok=True)
    html_file = os.path.join(output_dir, f"{base_name}.html")
    json_file = os.path.join(output_dir, f"{base_name}.json")

    with LogExecutionTime(logger_obj=logger, task_str="env run") as timer:
        env = make("werewolf", debug=debug, configuration=config)
        env.run(agents)

    env.info["total_run_time"] = timer.elapsed_time
    env.info["total_run_time_formatted"] = timer.elapsed_time_formatted()

    logger.info("Game finished")
    env_out = env.render(mode="html")
    with open(html_file, "w") as out:
        out.write(env_out)
    logger.info(f"HTML replay written to {html_file}")
    env_out = env.render(mode="json")
    with open(json_file, "w") as out:
        out.write(env_out)
    logger.info(f"JSON replay written to {json_file}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    logger.info(f"Script finished in {formatted_time}.")
    return env

