
def get_profiling_event(event_name, profiler, dedup_gpu_user_annotation=False):
    event_list = (
        profiler.events()
        if isinstance(profiler, torch.profiler.profile)
        else profiler.function_events
    )
    return [
        event
        for event in event_list
        if (
            (event.name.endswith(event_name) or event.name.startswith(event_name))
            and (
                not dedup_gpu_user_annotation
                or event.device_type not in [DeviceType.CUDA, DeviceType.XPU]
            )
        )
    ]

