
def get_schedule_class(schedule_name: str):
    """
    Maps a schedule name (case insensitive) to its corresponding class object.

    Args:
        schedule_name (str): The name of the schedule.
    """
    schedule_map = {
        "1F1B": Schedule1F1B,
        "Interleaved1F1B": ScheduleInterleaved1F1B,
        "GPipe": ScheduleGPipe,
        "LoopedBFS": ScheduleLoopedBFS,
        "InterleavedZeroBubble": ScheduleInterleavedZeroBubble,
        "PipelineScheduleSingle": PipelineScheduleSingle,
        "PipelineScheduleMulti": PipelineScheduleMulti,
        "ZBVZeroBubble": ScheduleZBVZeroBubble,
        "DualPipeV": ScheduleDualPipeV,
    }
    lowercase_keys = {k.lower(): k for k in schedule_map}
    lowercase_schedule_name = schedule_name.lower()
    if lowercase_schedule_name not in lowercase_keys:
        raise ValueError(
            f"Unknown schedule name '{schedule_name}'. The valid options are {list(schedule_map.keys())}"
        )
    return schedule_map[lowercase_keys[lowercase_schedule_name]]

