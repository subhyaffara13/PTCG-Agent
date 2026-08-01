
def load_dm_lab(
    level_name: str = "lt_chasm",
    observations: str | None = "RGBD",
    renderer: str | None = "hardware",
    width: int | None = 320,
    height: int | None = 240,
    fps: int | None = 60,
    mixerSeed: int | None = 0,
    levelDirectory: str | None = "",
    appendCommand: str | None = "",
    botCount: int | None = None,
):
    """Helper function to load a DM Lab environment.

    Handles arguments which are None or unspecified (which will throw errors otherwise).

    Args:
        level_name (str): name of level to load
        observations: (Optional[str]): type of observations to use (default: "RGBD")
        renderer (Optional[str]): renderer to use (default: "hardware")
        width (Optional[int]): horizontal resolution of the observation frames (default: 240)
        height (Optional[int]): vertical resolution of the observation frames (default: 320)
        fps (Optional[int]): frames-per-second (default: 60)
        mixerSeed (Optional[int]):	value combined with each of the seeds fed to the environment to define unique subsets of seeds (default: 0)
        levelDirectory (Optional[str]): optional path to level directory (relative paths are relative to game_scripts/levels)
        appendCommand (Optional[str]): Commands for the internal Quake console
        botCount (Optional[int]): number of bots to use

    Returns:
        env: DM Lab environment
    """
    import deepmind_lab

    if observations is not None:
        obs = [observations]
    else:
        obs = ["RGBD"]

    renderer = renderer

    # botCount is a specific config option for certain level and may result in errors
    try:
        config = {
            "width": str(width),
            "height": str(height),
            "fps": str(fps),
            "levelDirectory": levelDirectory,
            "appendCommand": appendCommand,
            "mixerSeed": str(mixerSeed),
            "botCount": str(botCount),
        }
        return deepmind_lab.Lab(level_name, obs, config=config, renderer=renderer)

    except Exception:
        pass

    # try without botCount configuration option as it is not used for all environments
    try:
        config = {
            "width": str(width),
            "height": str(height),
            "fps": str(fps),
            "levelDirectory": levelDirectory,
            "appendCommand": appendCommand,
        }
        return deepmind_lab.Lab("lt_chasm", obs, config=config, renderer=renderer)

    except Exception as e:
        print("Could not load DM Lab environment with given configuration: ", e)

