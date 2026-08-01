
def get_scroll_interval(step, config):
    if step >= config.scrollRampSteps:
        return config.scrollEndInterval
    progress = step / max(1, config.scrollRampSteps)
    interval = config.scrollStartInterval - (config.scrollStartInterval - config.scrollEndInterval) * progress
    return max(config.scrollEndInterval, round(interval))

