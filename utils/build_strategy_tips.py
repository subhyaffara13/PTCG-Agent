
def build_strategy_tips(trend_stats, strategy_trackers, threshold):
    strategy_tips = {"priority_modifiers": {}}
    report_lines = []
    if strategy_trackers["passed_turns"] > trend_stats["total_games"] * 0.25:
        report_lines.append("- **[CRITICAL TREND]** The agent is passing its turn too frequently across the entire dataset. It needs an aggressive draw multiplier to force plays.")
        strategy_tips["priority_modifiers"]["force_draw_engine"] = 1.25
    if trend_stats["timeouts"] > threshold:
        report_lines.append(f"- **[CRITICAL TREND]** Detected {trend_stats['timeouts']} game timeouts. The agent is looping or stalling. Increasing aggression multiplier.")
        strategy_tips["priority_modifiers"]["aggression_bias"] = 1.5
    return strategy_tips, report_lines

