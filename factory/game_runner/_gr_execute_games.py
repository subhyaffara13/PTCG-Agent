from . import Counter, ProcessPoolExecutor, _parallel_game_worker, datetime, json, logger, os
from ._gr_consolidate import _consolidate_results

def _execute_games(self, iteration_id, version_n1, version_n2, games_config, league, league_matchups):
    results = {}
    executor = type(self)._executor
    if executor is None:
        type(self)._executor = ProcessPoolExecutor(max_workers=os.cpu_count() or 16)
        executor = type(self)._executor
    try:
        futures = [executor.submit(_parallel_game_worker, str(self.log_dir), *g) for g in games_config]
    except RuntimeError as re:
        if "after shutdown" in str(re):
            type(self)._executor = ProcessPoolExecutor(max_workers=os.cpu_count() or 16)
            executor = type(self)._executor
            futures = [executor.submit(_parallel_game_worker, str(self.log_dir), *g) for g in games_config]
        else: raise
    for future in futures:
        try: res = future.result(timeout=330.0); results[res["label"]] = res
        except Exception as e:
            logger.error(f"Process crashed: {e}")
            if type(self)._executor: type(self)._executor.shutdown(wait=False, cancel_futures=True)
            type(self)._executor = None
    for label, res in list(results.items()):
        if label.endswith("_swap"):
            w = res.get("winner")
            if w == "player_a": res["winner"] = "player_b"
            elif w == "player_b": res["winner"] = "player_a"
            pa = res.get("prizes_taken_a", 0); pb = res.get("prizes_taken_b", 0)
            res["prizes_taken_a"] = pb; res["prizes_taken_b"] = pa
    for label, opp_name in league_matchups.items():
        res = results.get(label)
        if res and res.get("winner") != "error":
            winner = res.get("winner"); league.update_elo(opp_name, "main_agent", winner)
            if opp_name.startswith("checkpoint_"):
                try:
                    from factory.model_checkpoint_manager import ModelCheckpointManager
                    mcm = ModelCheckpointManager()
                    r = 1.0 if winner == "player_a" else (0.0 if winner == "player_b" else 0.5)
                    mcm.update_checkpoint_elo(opp_name, league.ratings.get("main_agent", 1200.0), r)
                except Exception as e: logger.debug(f"Failed to update checkpoint Elo: {e}")
    _consolidate_results(results)
    for k in ["reasoning_test", "deck_test", "variance_baseline"]:
        if k not in results: results[k] = {"winner": "error", "turns_taken": 0, "log_files": {}}
    disk_payload = {"iteration": iteration_id, "timestamp": datetime.now().isoformat(),
                    "games": {l: {k: v for k, v in r.items() if k != "steps_dump"} for l, r in results.items()},
                    "ready_for_eval": True}
    (self.log_dir / "iteration_result.json").write_text(json.dumps(disk_payload, indent=2), encoding="utf-8")
    return {"iteration": iteration_id, "timestamp": datetime.now().isoformat(), "games": results, "ready_for_eval": True}
