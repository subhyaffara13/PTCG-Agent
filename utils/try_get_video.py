from pathlib import Path


def try_get_video(env, keep_running=False):
    if not env.football_video_path:
        internal_env = m_envs[env.configuration.id]
        while not hasattr(internal_env, "_env"):
            internal_env = internal_env.env
        if not keep_running and internal_env._env._step == -1:
            # Generate no-op step, so that video is available.
            internal_env.step([0] * (env.configuration.team_1 + env.configuration.team_2))
        trace = internal_env._env._trace
        if trace:
            trace._dump_config["episode_done"]._min_frequency = 0
            dumps = trace.process_pending_dumps(True)
            env.football_video_path = retrieve_video_link(dumps)
        if not env.football_video_path:
            return
        if keep_running:
            trace.write_dump("episode_done")
    if "LiveVideoPath" in env.info and env.info["LiveVideoPath"] is not None:
        target_path = Path(env.info["LiveVideoPath"])
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(env.football_video_path, target_path)
        env.football_video_path = env.info["LiveVideoPath"]

