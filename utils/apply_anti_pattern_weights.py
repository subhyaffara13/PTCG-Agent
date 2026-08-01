
def apply_anti_pattern_weights(current_weights, anti_patterns):
    adjusted = False
    for pattern in anti_patterns:
        if "brick" in str(pattern).lower() or "timeout" in str(pattern).lower():
            logger.info("Architecture Team detected 'brick/timeout' meta. Bumping consistency weights.")
            for arch in current_weights:
                w = list(current_weights[arch])
                w[0] = min(0.8, w[0] + 0.05)
                w[1] = max(0.05, w[1] - 0.02)
                w[2] = max(0.05, w[2] - 0.02)
                w[3] = max(0.05, w[3] - 0.01)
                total = sum(w)
                current_weights[arch] = tuple(round(x / total, 3) for x in w)
                adjusted = True
    return adjusted

