import json
import logging
import os
import sys
import datetime
from pathlib import Path

# Setup basic log capture
logger = logging.getLogger(__name__)

# Add agent directory to sys.path to ensure imports find cb_agents and router
agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
if agent_dir not in sys.path:
    sys.path.insert(0, agent_dir)

import time
_GLOBAL_START_TIME = time.time()


def compile_extension_on_kaggle(configuration=None):
    """Compiles the C++ ptcg_core extension on Kaggle at module load time or Step 0."""
    import sys
    import os
    import shutil
    import subprocess
    from pathlib import Path
    
    # 1. Check if we are running on Kaggle
    is_kaggle_run = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")
    if not is_kaggle_run:
        return False

    sys.stderr.write("[compile] Running inside Kaggle sandbox. Checking C++ extension...\n")
        
    # 2. Check if we have already built the .so file in /kaggle/working
    working_dir = Path("/kaggle/working")
    if not working_dir.exists():
        sys.stderr.write("[compile] /kaggle/working does not exist. Skipping compilation.\n")
        return False
        
    # See if ptcg_core*.so is already in /kaggle/working
    so_files = list(working_dir.glob("ptcg_core*.so"))
    if so_files:
        sys.stderr.write(f"[compile] Found pre-compiled C++ extension: {so_files[0].name}. Adding to path.\n")
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
        try:
            import ptcg_core  # type: ignore
            _update_mcts_module(ptcg_core)
        except Exception as e:
            sys.stderr.write(f"[compile] Error loading pre-compiled extension: {e}\n")
        return True
        
    # 3. Locate source files in the agent extraction directory
    raw_path = None
    if isinstance(configuration, dict):
        raw_path = configuration.get("__raw_path__")
    
    if not raw_path:
        # Fallback to sys.path or guess
        sys.stderr.write("[compile] __raw_path__ not found in configuration. Trying path lookup...\n")
        for p in sys.path:
            if p and Path(p).joinpath("setup.py").exists():
                raw_path = str(Path(p).joinpath("main.py"))
                break
                
    if not raw_path:
        # Try parent directory relative guess
        curr_dir = Path(__file__).parent.resolve() if "__file__" in globals() and globals()["__file__"] else Path(os.getcwd())
        if curr_dir.joinpath("setup.py").exists():
            raw_path = str(curr_dir.joinpath("main.py"))
            
    if not raw_path:
        sys.stderr.write("[compile] Could not determine agent extraction directory. Skipping compilation.\n")
        return False
        
    curr_agent_dir = Path(raw_path).parent.resolve()
    src_dir = curr_agent_dir / "src"
    setup_file = curr_agent_dir / "setup.py"
    
    sys.stderr.write(f"[compile] Resolved agent extraction directory: {curr_agent_dir}\n")
    
    if not src_dir.exists() or not setup_file.exists():
        sys.stderr.write("[compile] C++ source files or setup.py not found in agent directory. Skipping on-the-fly compile.\n")
        return False
        
    # 4. Create temporary build dir in /kaggle/working
    build_dir = working_dir / "ptcg_build"
    try:
        if build_dir.exists():
            shutil.rmtree(build_dir, ignore_errors=True)
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy src/ and setup.py to build_dir
        shutil.copytree(src_dir, build_dir / "src")
        shutil.copy2(setup_file, build_dir / "setup.py")
        if (curr_agent_dir / "CMakeLists.txt").exists():
            shutil.copy2(curr_agent_dir / "CMakeLists.txt", build_dir / "CMakeLists.txt")
            
        sys.stderr.write(f"[compile] Copied C++ sources to build dir: {build_dir}\n")
        
        # 5. Run compilation command
        sys.stderr.write("[compile] Compiling C++ ptcg_core extension on-the-fly...\n")
        try:
            res = subprocess.run(
                [sys.executable, "setup.py", "build_ext", "--inplace"],
                cwd=str(build_dir),
                capture_output=True,
                text=True,
                timeout=120
            )
        except subprocess.TimeoutExpired as e:
            sys.stderr.write(f"[compile] Compilation timed out: {e}\n")
            return False
        sys.stderr.write(f"[compile] Compilation stdout:\n{res.stdout}\n")
        sys.stderr.write(f"[compile] Compilation stderr:\n{res.stderr}\n")
        
        if res.returncode != 0:
            sys.stderr.write(f"[compile] Compilation failed with exit code: {res.returncode}\n")
            return False
            
        # 6. Locate compiled .so file
        compiled_so = list(build_dir.glob("ptcg_core*.so"))
        if not compiled_so:
            sys.stderr.write("[compile] Compilation completed but ptcg_core*.so not found.\n")
            return False
            
        # Copy to /kaggle/working
        target_so = working_dir / compiled_so[0].name
        shutil.copy2(compiled_so[0], target_so)
        sys.stderr.write(f"[compile] Successfully copied compiled extension to {target_so}\n")
        
        # Add to sys.path
        if str(working_dir) not in sys.path:
            sys.path.insert(0, str(working_dir))
            
        # Try importing to verify
        import ptcg_core  # type: ignore
        _update_mcts_module(ptcg_core)
        sys.stderr.write("[compile] ptcg_core successfully compiled, loaded, and verified!\n")
        return True
    except Exception as build_err:
        sys.stderr.write(f"[compile] Exception during on-the-fly compilation: {build_err}\n")
        return False

def _update_mcts_module(ptcg_core_module):
    """Helper to dynamically patch mcts_engine with C++ simulator module."""
    import sys
    for name, mod in list(sys.modules.items()):
        if name == "cb_agents.mcts_engine" or name.endswith("mcts_engine"):
            setattr(mod, "ptcg_core", ptcg_core_module)
            setattr(mod, "HAS_CPP", True)

def load_deck_on_kaggle(configuration=None):
    import csv
    import sys
    from pathlib import Path
    
    agent_dir = None
    if isinstance(configuration, dict) and configuration.get("__raw_path__"):
        agent_dir = Path(configuration["__raw_path__"]).parent
    
    if not agent_dir:
        for p in sys.path:
            if p and Path(p).joinpath("deck.csv").exists():
                agent_dir = Path(p)
                break
                
    if not agent_dir:
        curr_dir = Path(__file__).parent.resolve() if "__file__" in globals() and globals()["__file__"] else Path(os.getcwd())
        if curr_dir.joinpath("deck.csv").exists():
            agent_dir = curr_dir
            
    if not agent_dir:
        sys.stderr.write("[deck] Could not determine agent directory to load deck.csv. Using fallback.\n")
        return None
        
    deck_path = agent_dir / "deck.csv"
    sys.stderr.write(f"[deck] Loading deck from: {deck_path}\n")
    if not deck_path.exists():
        sys.stderr.write(f"[deck] deck.csv not found at {deck_path}\n")
        return None
        
    try:
        loaded_deck = []
        with open(deck_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                loaded_deck.extend([int(row["card_id"])] * int(row["count"]))
        if len(loaded_deck) == 60:
            sys.stderr.write(f"[deck] Successfully loaded deck from deck.csv (60 cards)\n")
            return loaded_deck
        else:
            sys.stderr.write(f"[deck] Loaded deck has invalid length: {len(loaded_deck)}\n")
    except Exception as e:
        sys.stderr.write(f"[deck] Error loading deck.csv: {e}\n")
    return None

# Run compilation on Kaggle immediately at module load time (best-effort)
compile_extension_on_kaggle()

# Try to import Orchestrator from cb_agents if not already present
if globals().get("orchestrator") is None:
    try:
        from cb_agents.orchestrator import Orchestrator
        orchestrator = Orchestrator(
            skills_dir=os.path.join(agent_dir, "skills"),
            log_dir=os.path.join(agent_dir, "logs")
        )
        orchestrator.start_game()
    except Exception as global_err:
        logger.error(f"Global orchestrator initialization failed: {global_err}")
        orchestrator = None

# Default deck from the competition environment if not already defined (single-file mode)
_existing_deck = globals().get("DEFAULT_DECK")
if _existing_deck is None:
    DEFAULT_DECK = [
        957, 957, 957, 979, 979, 979, 37, 37, 37, 210,
        210, 210, 1121, 1227, 1227, 1227, 1227, 1152, 1152, 1152,
        1152, 1210, 1210, 1210, 1194, 1194, 1194, 1211, 1198, 1256,
        1097, 1097, 1097, 1097, 1182, 1182, 1182, 1182, 1102, 1086,
        1086, 1086, 1086, 1123, 1081, 1122, 6, 6, 6, 6,
        6, 6, 6, 6, 4, 4, 4, 4, 4, 4
    ]

    try:
        _deck_csv_path = None
        if "__file__" in globals() and globals()["__file__"]:
            _deck_csv_path = Path(__file__).parent / "deck.csv"
        if not _deck_csv_path or not _deck_csv_path.exists():
            _deck_csv_path = Path("deck.csv")
        if not _deck_csv_path.exists():
            _deck_csv_path = Path("submission/deck.csv")
        
        if _deck_csv_path.exists():
            import csv
            _loaded_deck = []
            with open(_deck_csv_path, "r", encoding="utf-8") as _f:
                _reader = csv.DictReader(_f)
                for _row in _reader:
                    _loaded_deck.extend([int(_row["card_id"])] * int(_row["count"]))
            if len(_loaded_deck) == 60:
                DEFAULT_DECK = _loaded_deck
    except Exception:
        pass



from typing import Any

def get_val(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    try:
        return getattr(obj, key, default)
    except Exception:
        return default

def _log_action_exception(exc: Exception):
    try:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "action_log.json"
        
        error_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "submission_agent_crash",
            "agent_called": "submission/main.py",
            "packet_type": "exception",
            "error_reason": str(exc)
        }
        
        logs = []
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8").strip()
            if content:
                try:
                    logs = json.loads(content)
                    if not isinstance(logs, list):
                        logs = [logs]
                except json.JSONDecodeError:
                    logs = []
        logs.append(error_entry)
        log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    except Exception as log_err:
        pass

_registry = None

def resolve_option_names(options, observation, my_idx):
    global _registry
    try:
        if _registry is None:
            from cb_agents.card_registry import CardRegistry
            import os
            from pathlib import Path
            agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
            skills_dir = os.path.join(agent_dir, "skills")
            _registry = CardRegistry(skills_dir=skills_dir)
        registry = _registry
    except Exception:
        registry = None

    if not registry:
        return

    try:
        current = get_val(observation, "current", {})
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return

        my_state = players[my_idx]
        hand = get_val(my_state, "hand", [])

        for opt in options:
            opt_type = get_val(opt, "type")
            if opt_type in (7, 8, 9):
                area = get_val(opt, "area", 2)
                index = get_val(opt, "index")
                if area == 2 and index is not None and len(hand) > index:
                    card = hand[index]
                    card_id = get_val(card, "id")
                    if card_id is not None:
                        card_entry = registry.get(card_id)
                        if card_entry:
                            if isinstance(opt, dict):
                                opt["name"] = card_entry.card_name
                            else:
                                try:
                                    setattr(opt, "name", card_entry.card_name)
                                except:
                                    pass
    except Exception as e:
        import sys
        sys.stderr.write(f"[resolve_option_names] Error: {e}\n")

def get_mapped_indices(action_label: str, options: list, game_state: dict = None) -> list:
    """Resolves specific option indexes from action label by matching action types, target index strings, and names."""
    if not action_label:
        return []
    if action_label == "pass":
        return [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]
        
    target = action_label.split(":", 1)[1] if ":" in action_label else ""
    my_hand = game_state.get("my_hand", []) if game_state else []
    
    if action_label.startswith("target:"):
        tgt_id = target
        tgt_slot = 0
        active = game_state.get("my_active_pokemon", {}) if game_state else {}
        if isinstance(active, dict) and str(active.get("id")) == tgt_id:
            tgt_slot = 0
        else:
            bench = game_state.get("my_bench", []) if game_state else []
            for idx, p in enumerate(bench):
                if isinstance(p, dict) and str(p.get("id")) == tgt_id:
                    tgt_slot = idx + 1
                    break
        
        for i, opt in enumerate(options):
            if get_val(opt, "slot") == tgt_slot or get_val(opt, "index") == tgt_slot:
                return [i]
        return [tgt_slot if tgt_slot < len(options) else 0]

    if action_label.startswith("attach_energy:") or action_label.startswith("bench:") or action_label.startswith("play_trainer:") or action_label.startswith("evolve:"):
        card_target = target.split(":")[0] if target else ""
        if card_target:
            target_str = str(card_target)
            for i, opt in enumerate(options):
                opt_type = get_val(opt, "type")
                if opt_type in (7, 8, 9, "Play", "play", "Attach", "attach"):
                    hand_idx = get_val(opt, "index", -1)
                    if hand_idx is not None and isinstance(hand_idx, int) and 0 <= hand_idx < len(my_hand):
                        card_id = str(my_hand[hand_idx])
                        if card_id == target_str:
                            return [i]
            if card_target.isdigit():
                idx = int(card_target)
                if 0 <= idx < len(options):
                    return [idx]

    if action_label.startswith("take_prize:"):
        if target.isdigit():
            idx = int(target)
            if 0 <= idx < len(options):
                return [idx]
        return [0]

    if target.isdigit():
        idx = int(target)
        if 0 <= idx < len(options):
            return [idx]

    mapped_indices = []
    if action_label.startswith("attack:"):
        if target.isdigit():
            idx = int(target)
            if 0 <= idx < len(options):
                return [idx]
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (12, 13, "Attack", "attack")]
    elif action_label.startswith("attach_energy:"):
        parts = action_label.split(":")
        energy_name = parts[1] if len(parts) > 1 else ""
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (8, 9, "Attach", "attach", "Energy", "energy") and (not energy_name or str(get_val(opt, "name", "")).lower() == energy_name.lower())]
        if not mapped_indices:
            mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (8, 9, "Attach", "attach", "Energy", "energy")]
    elif action_label.startswith("bench:") or action_label.startswith("evolve:"):
        poke_name = action_label.split(":", 1)[1] if ":" in action_label else ""
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, 8, "Play", "play") and (not poke_name or str(get_val(opt, "name", "")).lower() == poke_name.lower())]
        if not mapped_indices:
            mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, 8, "Play", "play")]
    elif action_label.startswith("play_trainer:"):
        trainer_name = action_label.split(":", 1)[1] if ":" in action_label else ""
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play", "Trainer", "trainer") and (not trainer_name or str(get_val(opt, "name", "")).lower() == trainer_name.lower())]
        if not mapped_indices:
            mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play", "Trainer", "trainer")]
    elif action_label.startswith("retreat:"):
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (10, 12, "Retreat", "retreat")]
    elif action_label.startswith("ability:"):
        ability_name = action_label.split(":", 1)[1] if ":" in action_label else ""
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (9, 11, 15, "Ability", "ability") and (not ability_name or str(get_val(opt, "name", "")).lower() == ability_name.lower())]
        if not mapped_indices:
            mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (9, 11, 15, "Ability", "ability")]
            
    if not mapped_indices:
        mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]
        
    return mapped_indices


def make_smart_choice(select, observation, fallback_action):
    global _registry
    try:
        options = get_val(select, "option", [])
        if not options:
            return fallback_action
            
        max_count = get_val(select, "maxCount", 1)
        sel_type = get_val(select, "type")
        
        # Resolve skills_dir for CardRegistry
        try:
            if _registry is None:
                from cb_agents.card_registry import CardRegistry
                import os
                from pathlib import Path
                agent_dir = str(Path(__file__).parent.resolve()) if "__file__" in globals() and globals()["__file__"] else os.getcwd()
                skills_dir = os.path.join(agent_dir, "skills")
                _registry = CardRegistry(skills_dir=skills_dir)
            registry = _registry
        except Exception:
            registry = None

        if registry is None:
            return fallback_action

        # Detect if this is likely a hand discard choice (cost for trainer or energy discard)
        is_discard = False
        if sel_type in (1, 2, 4):
            try:
                if sel_type == 4 or str(get_val(select, "context", "")).lower() in ("discard", "energy_discard"):
                    is_discard = True
                else:
                    # Check if all options point to cards in our hand
                    current = get_val(observation, "current")
                    my_idx = get_val(current, "yourIndex", 0)
                    players = get_val(current, "players", [])
                    if len(players) > my_idx:
                        my_hand_ids = [get_val(c, "id") for c in get_val(players[my_idx], "hand", []) if c and get_val(c, "id") is not None]
                        
                        option_card_ids = []
                        for opt in options:
                            opt_id = get_val(opt, "id")
                            if opt_id is None:
                                # Resolve coordinate
                                area = get_val(opt, "area")
                                index = get_val(opt, "index")
                                p_idx = get_val(opt, "playerIndex", 0)
                                if p_idx == my_idx and area == 2: # Hand
                                    hand = get_val(players[my_idx], "hand", [])
                                    if len(hand) > index:
                                        opt_id = get_val(hand[index], "id")
                            if opt_id is not None:
                                option_card_ids.append(opt_id)
                        
                        if option_card_ids and all(oid in my_hand_ids for oid in option_card_ids):
                            is_discard = True
            except Exception:
                pass

        def resolve_instance(val):
            if isinstance(val, list):
                return val[0] if len(val) > 0 else None
            return val

        # Collect board Pokemon names for evolution synergy mapping
        board_pokemon_names = set()
        try:
            current = get_val(observation, "current")
            my_idx = get_val(current, "yourIndex", 0)
            players = get_val(current, "players", [])
            if len(players) > my_idx:
                my_state = players[my_idx]
                act = resolve_instance(get_val(my_state, "active"))
                if act:
                    act_name = get_val(act, "name") or get_val(get_val(act, "card"), "name")
                    if act_name: board_pokemon_names.add(str(act_name).lower())
                for b in get_val(my_state, "bench", []):
                    b_resolved = resolve_instance(b)
                    if b_resolved:
                        b_name = get_val(b_resolved, "name") or get_val(get_val(b_resolved, "card"), "name")
                        if b_name: board_pokemon_names.add(str(b_name).lower())
        except Exception:
            pass

        # Score each option
        scored_options = []
        for idx, opt in enumerate(options):
            card_id = get_val(opt, "id")
            card_name = get_val(opt, "name", "")
            
            # If coordinates are present instead of name/id, resolve them
            if card_id is None and not card_name:
                try:
                    area = get_val(opt, "area")
                    index = get_val(opt, "index")
                    p_idx = get_val(opt, "playerIndex", 0)
                    current = get_val(observation, "current")
                    players = get_val(current, "players", [])
                    if len(players) > p_idx:
                        p_state = players[p_idx]
                        if area == 2: # Hand
                            hand = get_val(p_state, "hand", [])
                            if len(hand) > index:
                                card_id = get_val(hand[index], "id")
                        elif area == 12: # Bench
                            bench = get_val(p_state, "bench", [])
                            if len(bench) > index:
                                bench_item = resolve_instance(bench[index])
                                if bench_item is not None:
                                    card_id = get_val(bench_item, "id")
                        elif area == 4: # Active
                            active = get_val(p_state, "active", [])
                            if len(active) > index:
                                active_item = resolve_instance(active[index])
                                if active_item is not None:
                                    card_id = get_val(active_item, "id")
                except Exception:
                    pass

            card = None
            if card_id is not None:
                card = registry.get_full_skill(card_id)
            if card is None and card_name:
                card = registry.get_full_skill(card_name)
                
            score = 0.0
            if card:
                score = getattr(card, "utility_score", 0.0)
                
                # 1. Boost based on learned rules from Kaggle champions
                card_id_int = getattr(card, "card_id", None)
                if card_id_int is not None:
                    dos_set = getattr(registry, "_learned_dos_set", None)
                    if dos_set is None and hasattr(registry, "learned_dos"):
                        dos_data = getattr(registry, "learned_dos", {})
                        if isinstance(dos_data, dict):
                            dos_list = dos_data.get("deck_dos", [])
                            dos_set = {int(x.get("card_id")) for x in dos_list if isinstance(x, dict) and "card_id" in x}
                        else:
                            dos_set = set()
                        registry._learned_dos_set = dos_set
                    donts_set = getattr(registry, "_learned_donts_set", None)
                    if donts_set is None and hasattr(registry, "learned_donts"):
                        donts_data = getattr(registry, "learned_donts", {})
                        if isinstance(donts_data, dict):
                            donts_list = donts_data.get("deck_donts", [])
                            donts_set = {int(x.get("card_id")) for x in donts_list if isinstance(x, dict) and "card_id" in x}
                        else:
                            donts_set = set()
                        registry._learned_donts_set = donts_set

                    if dos_set and int(card_id_int) in dos_set:
                        score += 12.0
                    if donts_set and int(card_id_int) in donts_set:
                        score -= 12.0
                
                # 2. Boost if evolution predecessor is on board
                predecessor = registry.get_evolution_predecessor(getattr(card, "card_name", ""))
                if predecessor and predecessor.lower() in board_pokemon_names:
                    score += 15.0

                # 3. Energy Requirement / Active priority boost
                if sel_type in (1, 4) or str(get_val(select, "context", "")).lower() in ("energy", "attach"):
                    try:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        p_idx = get_val(opt, "playerIndex", 0)
                        current = get_val(observation, "current")
                        my_idx = get_val(current, "yourIndex", 0)
                        if p_idx == my_idx:
                            players = get_val(current, "players", [])
                            my_state = players[my_idx]
                            instance = None
                            if area == 4: # Active
                                instance = resolve_instance(get_val(my_state, "active"))
                            elif area == 12: # Bench
                                bench = get_val(my_state, "bench", [])
                                if len(bench) > index:
                                    instance = resolve_instance(bench[index])
                            if instance:
                                attached = get_val(instance, "attached", [])
                                attached_count = len(attached) if isinstance(attached, list) else 0
                                required = getattr(card, "energy_cost", 0)
                                if attached_count < required:
                                    # Avoid attaching energy to low-HP or non-attacking support/setup Pokemon
                                    target_name = ""
                                    target_id = get_val(instance, "id")
                                    if target_id is not None and registry:
                                        target_card = registry.get_full_skill(target_id)
                                        if target_card:
                                            target_name = getattr(target_card, "card_name", "").lower()
                                    
                                    is_passive_support = any(s in target_name for s in {"dunsparce", "bidoof", "snom", "remoraid", "jirachi", "manaphy"})
                                    target_hp = get_val(instance, "hp", 100)
                                    target_max_hp = get_val(instance, "maxHp", 100)
                                    is_low_hp = target_hp <= 40 and target_max_hp <= 130
                                    
                                    if is_passive_support or is_low_hp:
                                        boost = -15.0
                                    else:
                                        boost = 10.0 * (required - attached_count)
                                        if area == 4:
                                            boost += 5.0
                                    score += boost
                    except Exception:
                        pass
                
                # 4. Support Pokemon early match boost
                try:
                    current = get_val(observation, "current")
                    turn = get_val(current, "turn", 1)
                    if turn <= 5:
                        support_names = {"bidoof", "bibarel", "snom", "frosmoth", "remoraid", "octillery", "dunsparce", "jirachi", "manaphy", "mew"}
                        card_name_lower = getattr(card, "card_name", "").lower()
                        if any(s in card_name_lower for s in support_names):
                            score += 15.0
                except Exception:
                    pass
                
                if sel_type == 3:
                    score += getattr(card, "ev_score", 0.0) + (getattr(card, "damage_output", 0) * 0.01)
            scored_options.append((idx, score))

        # Value Network One-Step Lookahead Rescoring
        orch = globals().get("orchestrator")
        value_net = getattr(getattr(orch, "mcts", None), "value_network", None) if orch else None
        if value_net:
            try:
                import sys
                current_obs = get_val(observation, "current")
                players_list = get_val(current_obs, "players", [])
                my_idx_val = get_val(current_obs, "yourIndex", 0)
                my_state_dict = players_list[my_idx_val] if len(players_list) > my_idx_val else {}
                choice_ctx = str(get_val(select, "context", "")).lower()
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = get_val(opt, "id")
                    hyp_state = my_state_dict.copy() if isinstance(my_state_dict, dict) else {}
                    if is_discard and cid is not None:
                        cid_str = str(cid)
                        if cid_str in hyp_state.get("my_hand", []):
                            hand_copy = list(hyp_state["my_hand"])
                            hand_copy.remove(cid_str)
                            hyp_state["my_hand"] = hand_copy
                    elif (choice_ctx in ("draw", "search", "take")) and cid is not None:
                        cid_str = str(cid)
                        hand_copy = list(hyp_state.get("my_hand", []))
                        hand_copy.append(cid_str)
                        hyp_state["my_hand"] = hand_copy
                    
                    val_score = value_net.evaluate(hyp_state)
                    scored_options[i] = (idx, base_score + 10.0 * val_score)
            except Exception as val_err:
                import sys
                sys.stderr.write(f"[smart_choice] Value net evaluation failed: {val_err}\n")

        # Context-aware rescoring for discards: learned_dos +12 dominates utility (0-0.86)
        # so trainers always outscore Pokemon — but Pokemon win the game. Fix the balance.
        if is_discard:
            try:
                current = get_val(observation, "current")
                my_idx = get_val(current, "yourIndex", 0)
                players = get_val(current, "players", [])
                my_state = players[my_idx] if len(players) > my_idx else {}
                bench_slots = len(get_val(my_state, "bench", []))
                active_poke = get_val(my_state, "active", None)
                has_active = bool(active_poke and len(active_poke) > 0 and active_poke[0])
                my_hand = get_val(my_state, "hand", [])
                hand_ids = [get_val(c, "id") for c in my_hand if c]
                for i in range(len(scored_options)):
                    idx, base_score = scored_options[i]
                    opt = options[idx]
                    cid = get_val(opt, "id")
                    if cid is None:
                        area = get_val(opt, "area")
                        index = get_val(opt, "index")
                        if area == 2 and len(my_hand) > index:
                            cid = get_val(my_hand[index], "id")
                    if cid is not None:
                        card = registry.get_full_skill(cid)
                        if card:
                            ct = getattr(card, "card_type", None)
                            ct_name = ct.name if ct else ""
                            card_id_int = int(cid) if not isinstance(cid, int) else cid
                            if ct_name == "POKEMON":
                                count_in_hand = sum(1 for hid in hand_ids if str(hid) == str(cid))
                                is_last_copy = count_in_hand <= 1
                                bench_needed = (6 - bench_slots) if has_active else (6 - bench_slots - 1)
                                if bench_needed > 0 and is_last_copy:
                                    base_score += 25.0  # Strong survival bonus for last Pokemon copy
                                elif bench_needed > 0:
                                    base_score += 10.0
                            elif ct_name == "ENERGY":
                                total_on_board = 0
                                if active_poke and len(active_poke) > 0:
                                    total_on_board += len(get_val(active_poke[0], "attached", []))
                                for b in get_val(my_state, "bench", []):
                                    if b and len(b) > 0:
                                        total_on_board += len(get_val(b[0], "attached", []))
                                if total_on_board >= 8:
                                    base_score -= 8.0  # Excess energy: more likely to discard
                                elif total_on_board >= 5:
                                    base_score -= 3.0
                            elif ct_name == "TRAINER":
                                if card_id_int in registry.learned_dos:
                                    base_score -= 6.0  # Reduce learned_dos bonus for discards
                            scored_options[i] = (idx, base_score)
            except Exception:
                pass
        
        # Sort options: lowest scoring first for discards, highest first otherwise
        if is_discard:
            scored_options.sort(key=lambda x: x[1])
        else:
            scored_options.sort(key=lambda x: x[1], reverse=True)

        selected = [idx for idx, _ in scored_options[:max_count]]
        
        # Ensure we return exactly max_count unique indices
        if len(selected) < max_count:
            for idx in range(len(options)):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
        return selected
    except Exception as e:
        import sys
        sys.stderr.write(f"[smart_choice] Exception during choice: {e}\n")
        return fallback_action

def agent(observation, configuration=None):
    """
    Main Actuation Agent loop parsed by Kaggle Match runtimes.
    """
    # Safe defaults
    DEFAULT_DECK_FALLBACK = [
        957, 957, 957, 979, 979, 979, 37, 37, 37, 210,
        210, 210, 1121, 1227, 1227, 1227, 1227, 1152, 1152, 1152,
        1152, 1210, 1210, 1210, 1194, 1194, 1194, 1211, 1198, 1256,
        1097, 1097, 1097, 1097, 1182, 1182, 1182, 1182, 1102, 1086,
        1086, 1086, 1086, 1123, 1081, 1122, 6, 6, 6, 6,
        6, 6, 6, 6, 4, 4, 4, 4, 4, 4
    ]
    fallback_action = [0]
    
    try:
        if observation is None:
            return DEFAULT_DECK_FALLBACK
            
        legal_actions = get_val(observation, "legal_actions")
        select = get_val(observation, "select")
        
        # Check if legacy mock unit test is running
        if legal_actions and select is None:
            return [legal_actions[0]]

        # Step 0: If select is None, we must submit the deck (list of 60 integers) at step 0, and [] otherwise
        if select is None:
            if get_val(observation, "step", 0) == 0:
                compile_extension_on_kaggle(configuration)
                # Try to load deck dynamically from Kaggle path first
                loaded_deck = load_deck_on_kaggle(configuration)
                if loaded_deck:
                    return loaded_deck
                # Try to return the global DEFAULT_DECK if it is loaded, otherwise fallback
                try:
                    if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                        return globals()["DEFAULT_DECK"]
                except Exception:
                    pass
                return DEFAULT_DECK_FALLBACK
            return []

        options = get_val(select, "option", [])
        max_count = get_val(select, "maxCount", 1)
        fallback_action = list(range(min(max_count, len(options)))) if options else [0]

        if "orchestrator" not in globals() or globals()["orchestrator"] is None:
            return fallback_action

        orch = globals()["orchestrator"]

        current = get_val(observation, "current")
        if not current:
            return fallback_action

        # Parse active player state
        my_idx = get_val(current, "yourIndex", 0)
        players = get_val(current, "players", [])
        if len(players) <= my_idx:
            return fallback_action

        # Dynamically resolve card names for Trainer, Bench and Energy options in hand
        resolve_option_names(options, observation, my_idx)

        def _normalize_pokemon(p):
            if not p or not isinstance(p, dict):
                return p
            p_copy = p.copy()
            attached = []
            energy_cards = p_copy.get("energyCards", [])
            if isinstance(energy_cards, list):
                for ec in energy_cards:
                    if isinstance(ec, dict) and "id" in ec:
                        attached.append(str(ec["id"]))
                    elif isinstance(ec, (int, str)):
                        attached.append(str(ec))
            p_copy["attached"] = attached
            return p_copy

        my_state = players[my_idx]
        opp_state = players[1 - my_idx] if len(players) > 1 else {}

        def _get_active(state):
            val = get_val(state, "active")
            if not val: return None
            if isinstance(val, list): return val[0]
            return val

        # Safely convert CABT board state to simplified game_state dict expected by Orchestrator
        game_state = {
            "my_hand": [get_val(c, "id") for c in get_val(my_state, "hand", []) if c and get_val(c, "id") is not None] if get_val(my_state, "hand") else [],
            "my_deck_count": get_val(my_state, "deckCount", 60),
            "my_prizes": len(get_val(my_state, "prize", [])) if isinstance(get_val(my_state, "prize"), list) else 6,
            "my_active_pokemon": _normalize_pokemon(_get_active(my_state)),
            "my_bench": [_normalize_pokemon(p) for p in get_val(my_state, "bench", [])] if get_val(my_state, "bench") else [],
            
            "opponent_active": _normalize_pokemon(_get_active(opp_state)),
            "opponent_bench": [_normalize_pokemon(p) for p in get_val(opp_state, "bench", [])] if get_val(opp_state, "bench") else [],
            "opponent_bench_count": len(get_val(opp_state, "bench", [])) if get_val(opp_state, "bench") else 0,
            "opponent_prizes": len(get_val(opp_state, "prize", [])) if isinstance(get_val(opp_state, "prize"), list) else 6,
            "opponent_discard": [get_val(c, "id") for c in get_val(opp_state, "discard", []) if c and get_val(c, "id") is not None] if get_val(opp_state, "discard") else [],
            "opponent_deck_count": get_val(opp_state, "deckCount", 60),
            "opponent_revealed": [],
            "opponent_last_play": None,
            
            "turn_number": get_val(current, "turn", 1),
            "time_elapsed": time.time() - _GLOBAL_START_TIME,
            "my_active_hp": 100,
            "opponent_active_hp": 100,
            "bench_has_attacker": False
        }

        # Parse legal candidates from options using exact option index strings (matching game_adapter.py)
        game_state["legal_attacks"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (12, 13, "Attack", "attack")]
        game_state["legal_attachments"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (8, 9, "Attach", "attach", "Energy", "energy")]
        
        legal_bench = []
        legal_evolutions = []
        my_hand = game_state.get("my_hand", [])
        for i, opt in enumerate(options):
            if get_val(opt, "type") in (7, 8, "Play", "play"):
                is_evo = False
                hand_idx = get_val(opt, "index")
                name = get_val(opt, "name", "")
                if hand_idx is not None and isinstance(hand_idx, int) and 0 <= hand_idx < len(my_hand):
                    card_id = my_hand[hand_idx]
                    if _registry and card_id:
                        try:
                            card = _registry.get_full_skill(card_id)
                            if card:
                                from cb_agents.card_types import CardStage
                                if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage:
                                    is_evo = True
                        except Exception:
                            pass
                elif _registry is not None and name:
                    try:
                        card = _registry.get_full_skill(name)
                        if card:
                            from cb_agents.card_types import CardStage
                            if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage:
                                is_evo = True
                    except Exception:
                        pass
                if is_evo:
                    legal_evolutions.append(str(i))
                else:
                    legal_bench.append(str(i))
                    
        game_state["legal_bench"] = legal_bench
        game_state["legal_evolutions"] = legal_evolutions
        game_state["legal_trainers"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (7, "Play", "play", "Trainer", "trainer")]
        game_state["legal_retreats"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (10, 12, "Retreat", "retreat")]
        game_state["legal_abilities"] = [str(i) for i, opt in enumerate(options) if get_val(opt, "type") in (9, 11, 15, "Ability", "ability")]

        # Parse detailed active HP if present
        my_active = get_val(my_state, "active")
        if my_active and isinstance(my_active, list) and len(my_active) > 0:
            active_pokemon = my_active[0]
            if active_pokemon:
                game_state["my_active_hp"] = get_val(active_pokemon, "hp", 100)

        opp_active = get_val(opp_state, "active")
        if opp_active and isinstance(opp_active, list) and len(opp_active) > 0:
            active_pokemon = opp_active[0]
            if active_pokemon:
                game_state["opponent_active_hp"] = get_val(active_pokemon, "hp", 100)

        # Check if we are at the Main Turn Menu (SelectType 0, Context 0)
        sel_type = get_val(select, "type")
        sel_ctx = get_val(select, "context")

        if sel_type == 0 and sel_ctx == 0:
            # Call orchestrator to determine action strategy string
            decision = orch.run_turn(game_state)
            action_label = (decision.primary_action.lower() 
                            if hasattr(decision, "primary_action") 
                            else str(decision).lower())

            # Resolve card names into all options dynamically
            if _registry is not None:
                from cb_agents.option_resolver import resolve_option_names
                my_idx = get_val(get_val(observation, "current", {}), "yourIndex", 0)
                resolve_option_names(options, observation, my_idx, _registry)

            # Map orchestrator's prefix action labels to actual select options using get_mapped_indices
            mapped_indices = get_mapped_indices(action_label, options, game_state)

            # If multiple candidate options exist, use smart choice heuristic to rank within those candidates
            if len(mapped_indices) > 1:
                smart_order = make_smart_choice(select, observation, fallback_action)
                # Sort mapped_indices based on smart_order ranking
                mapped_indices.sort(key=lambda idx: smart_order.index(idx) if idx in smart_order else 999)
            # If prefix matching yielded no indices and action is not explicitly PASS,
            # query smart choice over all non-pass legal options first
            if not mapped_indices and action_label != "pass":
                non_pass_opts = [i for i, opt in enumerate(options) if get_val(opt, "type") not in (14, "End", "pass")]
                if non_pass_opts:
                    smart_cand = make_smart_choice(select, observation, fallback_action)
                    if smart_cand:
                        mapped_indices = [idx for idx in smart_cand if idx in non_pass_opts]
                if not mapped_indices:
                    mapped_indices = non_pass_opts

            # If still nothing, or action is explicitly PASS, look for pass/done (Type 14)
            if not mapped_indices or action_label == "pass":
                mapped_indices = [i for i, opt in enumerate(options) if get_val(opt, "type") in (14, "End", "pass")]

            if not mapped_indices:
                mapped_indices = [0]

            selected = []
            for idx in (mapped_indices + list(range(len(options)))):
                if idx not in selected:
                    selected.append(idx)
                    if len(selected) == max_count:
                        break
            return selected
        else:
            return make_smart_choice(select, observation, fallback_action)

    except Exception as e:
        import sys
        sys.stderr.write(f"Agent execution crashed internally: {e}\n")
        try:
            _log_action_exception(e)
        except Exception:
            pass
        
        # Determine whether to return fallback deck or fallback action
        try:
            if observation is None or get_val(observation, "select") is None:
                if "DEFAULT_DECK" in globals() and len(globals()["DEFAULT_DECK"]) == 60:
                    return globals()["DEFAULT_DECK"]
                return DEFAULT_DECK_FALLBACK
        except Exception:
            pass
        return fallback_action


