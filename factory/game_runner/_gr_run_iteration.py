from . import Counter, Path, ProcessPoolExecutor, _parallel_game_worker, datetime, json, logger, os
from ._setup import DEFAULT_DECK
from ._mutate_deck__load_optimized_deck import _mutate_deck
from ._gr_execute_games import _execute_games

def _gr_run_iteration(self, iteration_id, version_n1, version_n2, deck_base, deck_new, reasoning_base, reasoning_new, num_matchups):
    d_base = deck_base.get("cards", DEFAULT_DECK) if isinstance(deck_base, dict) else deck_base
    d_new = deck_new.get("cards", DEFAULT_DECK) if isinstance(deck_new, dict) else deck_new
    if not isinstance(d_base, list): d_base = DEFAULT_DECK
    if not isinstance(d_new, list): d_new = DEFAULT_DECK
    from factory.league_manager import LeagueManager
    from factory.gauntlet_runner import GauntletRunner
    league = LeagueManager(); gauntlet = GauntletRunner(str(self.log_dir.parent / "skills"))
    games_config = [("reasoning_test", d_base, d_base, False, True, None, None, None)]
    league_matchups = {}
    core_archetypes = ["Aggro", "Control", "Setup", "Stall"]
    mutated_new = _mutate_deck(d_new)
    for idx, arch in enumerate(core_archetypes):
        seed = 2000 + idx; opp_deck = gauntlet._generate_real_deck(arch); opp_name = f"gauntlet_{arch}"
        league_matchups[f"deck_test_{idx}_orig"] = opp_name; league_matchups[f"deck_test_{idx}_swap"] = opp_name
        games_config.extend([(f"deck_test_{idx}_orig", opp_deck, mutated_new, False, False, seed, None, None),
                             (f"deck_test_{idx}_swap", mutated_new, opp_deck, False, False, seed, None, None)])
    return _execute_games(self, iteration_id, version_n1, version_n2, games_config, league, league_matchups)
