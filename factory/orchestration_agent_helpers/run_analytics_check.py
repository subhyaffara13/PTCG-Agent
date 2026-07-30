from . import Path, json, logger

def run_analytics_check(iteration: int):
    """Runs AnalyticsTeam on the latest iteration results."""
    try:
        from factory.teams.analytics_team import AnalyticsTeam
        result_file = Path("logs/iteration_result.json")
        if result_file.exists():
            res_data = json.loads(result_file.read_text(encoding="utf-8"))
            analytics = AnalyticsTeam()
            analytics.run_analysis(
                iteration_id=iteration, log_dir="logs",
                iteration_result=res_data, decks={"player_a": [], "player_b": []}
            )
            logger.info("Analytics heavy check finished.")
    except Exception as e:
        logger.error(f"Analytics check failed: {e}")

