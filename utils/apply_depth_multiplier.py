
def apply_depth_multiplier(config: MobileNetV2Config, channels: int) -> int:
    return make_divisible(int(round(channels * config.depth_multiplier)), config.depth_divisible_by, config.min_depth)

