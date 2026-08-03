import sys
import copy
import functools
import logging
import random
import re
import subprocess
import time
import uuid
from typing import Any, Optional, Tuple, Sequence, TextIO
_PluggyPlugin = Any
ExitCode = Any
DebugHandler = Any
from io import TextIOWrapper
import math
import click
import argparse
import os
import typing
from typing import *
import torch
import numpy as np
import json
import pickle
import ast
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", type=int)
    parser.add_argument("--read-fd", type=int)
    parser.add_argument("--write-fd", type=int)
    args = parser.parse_args()
    read_pipe = os.fdopen(args.read_fd, "rb")
    write_pipe = os.fdopen(args.write_fd, "wb")

    try:
        # Ensures the subprocess exits if the parent crashes:
        _async_compile_initializer(args.parent)
        TuningProcess.process_main(read_pipe, write_pipe)
    except Exception:
        log.exception("Uncaught exception in autotune subprocess")
    finally:
        read_pipe.close()
        write_pipe.close()


def main():
    utils_pkg = ROOT / 'utils'
    strategies_pkg = ROOT / 'strategies'
    ensure_package(utils_pkg)
    ensure_package(strategies_pkg)

    py_files = get_py_files()
    func_usage = {}
    for py in py_files:
        for func in parse_functions(py):
            func_usage.setdefault(func, set()).add(str(py))
        for call in find_function_calls(py):
            if call in func_usage:
                func_usage[call].add(str(py))
    # Identify functions used in >=3 distinct files
    candidates = {f: files for f, files in func_usage.items() if len(files) >= 3}
    # Move candidate functions to utils package
    for func, files in candidates.items():
        src_path = Path(next(iter(files)))
        module_name = snake_case(func)
        move_function_to_module(func, src_path, utils_pkg, module_name)
    # Rename large python files (>150 lines) to snake_case
    for py in py_files:
        if count_lines(py) > 150:
            new_name = snake_case(py.stem) + py.suffix
            new_path = py.with_name(new_name)
            if new_path != py:
                py.rename(new_path)
    # Rename C++ sources to snake_case
    for cpp in ROOT.rglob('*.cpp'):
        new_name = snake_case(cpp.stem) + cpp.suffix
        if new_name != cpp.name:
            cpp.rename(cpp.with_name(new_name))
    for hpp in ROOT.rglob('*.hpp'):
        new_name = snake_case(hpp.stem) + hpp.suffix
        if new_name != hpp.name:
            hpp.rename(hpp.with_name(new_name))
    # Ensure build_submission includes utils and strategies
    build_file = ROOT / 'build_submission.py'
    if build_file.exists():
        with open(build_file, 'a', encoding='utf-8') as f:
            f.write('\n# Include utils and strategies in submission package\n')
    print('Automated refactor completed.')


def main():
    # Use the full MCTS + C++ + value-network pipeline during training.
    # FAST_SIM_MODE is only activated on Kaggle when the C++ extension is missing.
    os.environ.pop("FAST_SIM_MODE", None)  # ensure it is unset locally
    
    last_iter = get_last_iteration_id()
    start_iter = last_iter + 1
    num_iters = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 100
    end_iter = last_iter + num_iters
    logger.info(f"Starting fast guided iterations from {start_iter} to {end_iter} ({num_iters} iterations)")
    
    for i in range(start_iter, end_iter + 1):
        pct = (i - start_iter) / (end_iter - start_iter + 1) * 100
        forced_archetype = get_archetype_for_iteration(i)
        forced_escalation = {"deck_architect": True, "builder_agent": False} if (i % 100 == 0 or i % 10 == 0) else None
        logger.info("\n" + "=" * 60)
        logger.info(f"  ITERATION {i}  [{pct:.0f}% complete]  archetype={forced_archetype}")
        if forced_escalation:
            logger.info(f"  Escalation: {forced_escalation}")
        logger.info("=" * 60)
        
        if i % 50 == 0: execute_refactor_step(i)
            
        try:
            run_iteration(iteration_id=i, forced_archetype=forced_archetype, forced_escalation=forced_escalation)
        except Exception as e:
            logger.error(f"Error during iteration {i}: {e}", exc_info=True)
            break

        orig_fast = os.environ.get("FAST_SIM_MODE")
        os.environ["FAST_SIM_MODE"] = "false"
        try:
            execute_ppo_step(i)
            update_league_from_iteration(i)
        finally:
            if orig_fast is not None:
                os.environ["FAST_SIM_MODE"] = orig_fast
            else:
                del os.environ["FAST_SIM_MODE"]
            
        should_build = (i == end_iter)
        eval_report_path = Path("logs/eval_report.json")
        if eval_report_path.exists():
            try:
                report_data = json.loads(eval_report_path.read_text(encoding="utf-8"))
                if report_data.get("version_scores", {}).get("best_version", "player_a") == "player_b":
                    should_build = True
                    logger.info(f"Iteration {i} achieved a new high score! Triggering build.")
            except Exception as e:
                logger.warning(f"Could not read eval_report.json: {e}")

        if should_build:
            logger.info("Building latest submission tarball...")
            try: subprocess.run([sys.executable, "build_submission.py"], check=True)
            except Exception as e: logger.error(f"Failed to auto-build submission: {e}")


def main():
    print("Collecting files...")
    files = get_codebase_files()
    
    # Process a few batches for efficiency to not blow up API costs
    batches = read_files_in_batches(files)[:3]
    
    print(f"Running LLM audit on {len(batches)} batches...")
    report = []
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i, batch in enumerate(batches):
            print(f"Dispatching Batch {i+1}...")
            future1 = executor.submit(agent_1_architect, batch)
            future2 = executor.submit(agent_2_resilience, batch)
            
            report.append(f"### Batch {i+1}\n")
            report.append(f"**Agent 1 (Architecture):**\n{future1.result()}\n")
            report.append(f"**Agent 2 (Resilience):**\n{future2.result()}\n")
            
    # Save the report to artifacts
    report_path = r"C:\Users\subhy\.gemini\antigravity-ide\brain\6cb59a4d-8fcc-45d4-b8d7-47815660574e\llm_audit_summary.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# LLM Subagent Audit Report\n\n" + "\n".join(report))
        
    print(f"Audit complete. Report saved to {report_path}")


def main():
    files = []
    for d in ['distributed', 'router', 'tests', 'run_guided_helpers', 'numpy_forward', 'run_audit_pipeline']:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.py")):
                files.append(f)
    
    count = 0
    for f in sorted(files):
        try:
            lines = len(f.read_text(encoding='utf-8').splitlines())
            if lines <= TARGET:
                continue
            if refactor_file(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.relative_to(ROOT)}: {e}")
            import traceback; traceback.print_exc()
    
    print(f"\nDone. {count} files further refactored.")


def main():
    files = []
    for d in ['distributed', 'router', 'tests', 'run_guided_helpers', 'numpy_forward', 'run_audit_pipeline']:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.py")):
                files.append(f)
    
    # Also handle standalone files in tests
    count = 0
    for f in sorted(files):
        try:
            lines = len(f.read_text(encoding='utf-8').splitlines())
            if lines <= TARGET:
                continue
            # Skip files we've already generated as _helpers
            if f.name.endswith('_helpers.py'):
                continue
            if fix_and_split(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.relative_to(ROOT)}: {e}")
    
    print(f"\nDone. {count} files fixed/split.")


def main():
    files = _find_all_over_50()
    print(f"Found {len(files)} files over {LINE_LIMIT} lines to refactor.")
    
    refactored_count = 0
    created_count = 0
    
    for fpath, lcount in files:
        print(f"\nProcessing: {fpath.relative_to(ROOT)} ({lcount} lines)")
        result = refactor_file(fpath)
        if result:
            refactored_count += 1
            for name, (_, helpers) in result.items():
                if helpers:
                    created_count += len(helpers)
    
    print(f"\n{'='*60}")
    print(f"Summary: Refactored {refactored_count} files, created {created_count} helper sub-files.")
    
    # Check remaining
    remaining = _find_all_over_50()
    if remaining:
        print(f"Remaining files over {LINE_LIMIT} lines: {len(remaining)}")
        for f, l in remaining[:10]:
            print(f"  {f.relative_to(ROOT)} ({l} lines)")
    else:
        print(f"ALL files are now ≤ {LINE_LIMIT} lines!")


def main():
    files = []
    for d in SCAN_DIRS:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.py")):
                rel = f.relative_to(ROOT)
                # Skip __init__.py, _setup.py, _helpers files
                if f.name == "__init__.py":
                    continue
                if f.name == "_setup.py":
                    continue
                if f.stem.endswith("_helpers"):
                    continue
                files.append(f)

    count = 0
    for fp in sorted(files):
        try:
            text = fp.read_text(encoding='utf-8')
            lines = text.splitlines()
            if len(lines) <= TARGET:
                continue

            rel = fp.relative_to(ROOT)
            print(f"  {rel} ({len(lines)} lines)...", end='')

            tree = ast.parse(text)
            ok = False

            if is_pkg_file(fp):
                # Try extracting defs to _prefixed files
                ok = refactor_pkg_file(fp, text, lines, tree)
                if not ok:
                    # Try splitting large single def
                    ok = split_large_def(fp, text, lines, tree)
            else:
                # Convert standalone to package
                ok = refactor_standalone(fp, text, lines, tree)
                if not ok:
                    ok = split_large_def(fp, text, lines, tree)

            if ok:
                print(" OK")
                count += 1
            else:
                print(" SKIP (can't split)")
        except SyntaxError:
            print(f"  {fp.relative_to(ROOT)}: syntax error")
        except Exception as e:
            print(f"  {fp.relative_to(ROOT)}: ERROR {e}")
            import traceback
            traceback.print_exc()

    print(f"\nRefactored: {count} files")


def main():
    src_dir = ROOT / 'src'
    files = sorted(src_dir.glob("*.cpp"))
    count = 0
    for f in files:
        try:
            if refactor_cpp(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.name}: {e}")
            import traceback; traceback.print_exc()
    print(f"\nProcessed {count}/{len(files)} files.")


def main():
    dirs = ['cb_agents','factory','factory/teams','distributed','router','visualizer','tests','run_guided_helpers']
    files = []
    for d in dirs:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.glob("*.py")):
                files.append(f)
    for f in sorted(ROOT.glob("*.py")):
        if f.name.startswith('_') or f.name == 'simple_agent.py':
            continue
        files.append(f)

    count = 0
    for f in files:
        try:
            if refactor_file(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.name}: {e}")
            import traceback; traceback.print_exc()

    print(f"\nProcessed {count}/{len(files)} files.")


def main():
    logger.info(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    
    # Clear any stale queues on start
    # r.delete("ptcg:experience_queue")
    
    # Store initial model weights
    initial_weights = {"dummy_weights": [0.0, 0.0, 0.0]}
    r.set("ptcg:latest_weights", pickle.dumps(initial_weights))
    r.set("ptcg:latest_archetype", "aggro")
    
    batch_size = 5
    batch_experiences = []
    
    logger.info("Learner initialized. Awaiting experiences from workers...")
    while True:
        # Block until an experience is pushed to the queue
        _, payload = r.blpop("ptcg:experience_queue")
        
        try:
            experience = pickle.loads(payload)  # nosec B301
            batch_experiences.append(experience)
            logger.info(f"Received experience payload. Batch progress: {len(batch_experiences)}/{batch_size}")
            
            if len(batch_experiences) >= batch_size:
                # Run Optimization update step
                new_weights = update_model_weights(None, batch_experiences)
                
                # Push the updated weights back to Redis
                r.set("ptcg:latest_weights", pickle.dumps(new_weights))
                logger.info("Updated weights pushed to Redis.")
                
                # Clear batch
                batch_experiences = []
                
        except Exception as e:
            logger.error(f"Error processing experience payload: {e}", exc_info=True)


def main():
    os.environ["IS_WORKER"] = "true"
    r = None
    if redis is not None:
        try:
            client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, socket_timeout=2)
            client.ping()
            r = client
            logger.info(f"Connected to central Redis at {REDIS_HOST}:{REDIS_PORT}")
        except Exception as e:
            logger.warning(f"Redis unavailable ({e}). Operating in local multi-process self-play worker mode.")
    
    runner = GameRunner()
    
    logger.info("Rollout worker started. Beginning loop...")
    while True:
        # 1. Fetch latest policy configuration/weights from central node
        archetype, weights = load_latest_config(r)
        
        # 2. Run simulation
        logger.info(f"Running simulation with archetype: {archetype}")
        try:
            # Simulate a match
            iteration_result = runner.run_iteration(
                iteration_id=0,
                version_n1="base_v0",
                version_n2="new_v0",
                deck_base=DEFAULT_DECK,
                deck_new=DEFAULT_DECK,
                reasoning_base={},
                reasoning_new={}
            )
            
            # 3. Serialize and push rollout trajectories to central queue
            if r:
                payload = pickle.dumps({
                    "archetype": archetype,
                    "result": iteration_result,
                    "timestamp": time.time()
                })
                r.rpush("ptcg:experience_queue", payload)
                logger.info("Successfully pushed rollout trajectory to experience queue.")
            else:
                logger.info("Simulation completed cleanly in local worker mode.")
            
        except Exception as e:
            logger.error(f"Error during simulation run: {e}", exc_info=True)
            time.sleep(5)  # Backoff on error


def main():
    import sys
    import os


    has_force_master_arg = False
    if "--force-master" in sys.argv:
        has_force_master_arg = True
    elif "--force" in sys.argv:
        try:
            idx = sys.argv.index("--force")
            if idx + 1 < len(sys.argv) and sys.argv[idx + 1] == "master":
                has_force_master_arg = True
        except ValueError:
            pass

    if has_force_master_arg or os.environ.get("FORCE_MASTER") == "1":
        logger.info("[OVERRIDE] Force Master Mode detected. Bypassing discovery and forcing Master Mode.")
        from factory.orchestrator_master import run_master_loop
        while True:
            try:
                run_master_loop(enable_distributed=True)
            except KeyboardInterrupt:
                logger.info("Force Master loop terminated by user.")
                break
            except Exception as e:
                logger.error(f"Master loop crashed: {e}")
                time.sleep(5)
        return

    logger.info("Orchestration Agent (Auto-Discovery Mode) started.")
    from distributed.discovery import WorkerListener
    from distributed.election import run_election
    from factory.orchestrator_master import run_master_loop
    from factory.orchestrator_worker import run_worker_loop
    
    last_seen_master_time = None
    last_known_master_ip = None

    while True:
        try:
            listener = WorkerListener(interface_type="wifi")
            logger.info("[DISCOVERY] Listening for master...")
            master_ip, master_version = listener.listen_for_master()
            
            if master_ip:
                logger.info(f"[DISCOVERY] Found master at {master_ip}. Becoming worker.")
                last_seen_master_time = time.time()
                last_known_master_ip = master_ip
                
                try:
                    from distributed.code_sync import sync_code, restart_process
                    if master_version and sync_code(master_version):
                        restart_process()
                except Exception as sync_e:
                    logger.warning(f"[SYNC] Code synchronization failed: {sync_e}")
                    
                run_worker_loop(master_ip, master_version)
            else:
                grace_period = 300  # 5 minutes
                if last_known_master_ip and last_seen_master_time and (time.time() - last_seen_master_time < grace_period):
                    logger.info(f"[DISCOVERY] Master beacons temporarily missing. Last seen master: {last_known_master_ip}. Retrying direct connect...")
                    try:
                        run_worker_loop(last_known_master_ip, None)
                    except Exception as loop_err:
                        logger.warning(f"Failed direct reconnect: {loop_err}")
                    time.sleep(5)
                else:
                    logger.info("[ELECTION] No master found and grace period expired. Running election...")
                    is_master, winner_ip = run_election(timeout=10)
                    
                    if is_master:
                        logger.info(f"[MASTER] Elected as master ({winner_ip}).")
                        run_master_loop(enable_distributed=True)
                    else:
                        logger.info(f"[WORKER] Master is {winner_ip}. Waiting for beacon...")
                        m_ip, m_version = listener.listen_for_master()
                        
                        try:
                            from distributed.code_sync import sync_code, restart_process
                            if m_version and sync_code(m_version):
                                restart_process()
                        except Exception as sync_e:
                            logger.warning(f"[SYNC] Code synchronization failed: {sync_e}")
                            
                        run_worker_loop(winner_ip, m_version)
        except KeyboardInterrupt:
            logger.info("Orchestration Agent received KeyboardInterrupt (Ctrl+C). Terminating immediately...")
            os._exit(0)
        except Exception as e:
            logger.error(f"Critical error in Orchestration Agent loop: {e}")
            time.sleep(5)


def main():
    import sys, json

    path = sys.argv[1] if len(sys.argv) > 1 else "logs/model_weights.pth"
    print(f"[numpy_forward] Loading: {path}")

    try:
        state_dict = load_pth(path)
    except FileNotFoundError:
        print(f"[numpy_forward] ERROR: {path} not found.")
        print("  Provide a path or place model_weights.pth in logs/")
        sys.exit(1)

    print(f"[numpy_forward] Loaded {len(state_dict)} keys:")
    for k, v in state_dict.items():
        print(f"    {k}: {v.shape}  dtype={v.dtype}  "
              f"range=[{v.min():.4f}, {v.max():.4f}]")

    # Auto-detect architecture from key names
    if "model.0.weight" in state_dict:
        model = PTCGValueMLPNumpy(state_dict)
        model_type = "PTCGValueMLP"
    elif "base.0.weight" in state_dict:
        model = ActorCriticNumpy(state_dict)
        model_type = "ActorCritic"
    else:
        print("[numpy_forward] Unknown architecture – keys:",
              list(state_dict.keys()))
        sys.exit(1)

    print(f"[numpy_forward] Architecture: {model_type}")
    input_dim = state_dict[list(state_dict.keys())[0]].shape[1]
    print(f"[numpy_forward] Input dim: {input_dim}")

    # Demo forward pass with dummy input
    dummy_x = np.random.randn(1, input_dim).astype(np.float32)
    if model_type == "PTCGValueMLP":
        output = model.forward(dummy_x)
        print(f"\n  Dummy input -> value: {output:.6f}")
    else:
        logits, value = model.forward(dummy_x)
        print(f"\n  Dummy input -> value: {value.item():.6f}, "
              f"logits shape: {logits.shape}")

    # Try demo with state_to_tensor if game state provided
    state_file = Path("logs/latest_state.json")
    if state_file.exists():
        with open(state_file) as f:
            game_state = json.load(f)
        x = state_to_tensor(game_state)
        if model_type == "PTCGValueMLP":
            val = model.forward(x.reshape(1, -1))
            print(f"\n  Real game state -> value: {val:.6f}")
        else:
            print(f"\n  Real game state shape: {x.shape}")


def main():
    check_and_install_dependencies()
    print("[INFO] Starting PTCG Agent Orchestrator...")
    try:
        from factory.orchestration_agent import main as orch_main
        orch_main()
    except KeyboardInterrupt:
        print("\n[INFO] Process terminated by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)


def main():
    logger.info("--- Starting Automated Auditor-Coder Pipeline ---")
    issues = run_auditor()
    
    if not issues:
        logger.info("Auditor Agent found no critical issues. Codebase is clean!")
        return

    logger.warning(f"Auditor Agent flagged {len(issues)} critical issues.")
    
    for idx, issue in enumerate(issues):
        logger.info(f"Processing issue {idx+1}/{len(issues)}...")
        fixed = invoke_coder_agent(issue)
        if fixed:
            valid = run_validator()
            if not valid:
                logger.error(f"Fix for {issue['file']} broke the tests.")
                # Revert logic would go here
    
    logger.info("--- Pipeline Finished ---")


def main():
    # Use the full MCTS + C++ + value-network pipeline during training.
    # FAST_SIM_MODE is only activated on Kaggle when the C++ extension is missing.
    os.environ.pop("FAST_SIM_MODE", None)  # ensure it is unset locally
    
    last_iter = get_last_iteration_id()
    start_iter = last_iter + 1
    num_iters = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 100
    end_iter = last_iter + num_iters
    logger.info(f"Starting fast guided iterations from {start_iter} to {end_iter} ({num_iters} iterations)")
    
    for i in range(start_iter, end_iter + 1):
        pct = (i - start_iter) / (end_iter - start_iter + 1) * 100
        forced_archetype = get_archetype_for_iteration(i)
        forced_escalation = {"deck_architect": True, "builder_agent": False} if (i % 100 == 0 or i % 10 == 0) else None
        logger.info("\n" + "=" * 60)
        logger.info(f"  ITERATION {i}  [{pct:.0f}% complete]  archetype={forced_archetype}")
        if forced_escalation:
            logger.info(f"  Escalation: {forced_escalation}")
        logger.info("=" * 60)
        
        if i % 50 == 0: execute_refactor_step(i)
            
        try:
            run_iteration(iteration_id=i, forced_archetype=forced_archetype, forced_escalation=forced_escalation)
        except Exception as e:
            logger.error(f"Error during iteration {i}: {e}", exc_info=True)
            break

        orig_fast = os.environ.get("FAST_SIM_MODE")
        os.environ["FAST_SIM_MODE"] = "false"
        try:
            execute_ppo_step(i)
            update_league_from_iteration(i)
        finally:
            if orig_fast is not None:
                os.environ["FAST_SIM_MODE"] = orig_fast
            else:
                del os.environ["FAST_SIM_MODE"]
            
        should_build = (i == end_iter)
        eval_report_path = Path("logs/eval_report.json")
        if eval_report_path.exists():
            try:
                report_data = json.loads(eval_report_path.read_text(encoding="utf-8"))
                if report_data.get("version_scores", {}).get("best_version", "player_a") == "player_b":
                    should_build = True
                    logger.info(f"Iteration {i} achieved a new high score! Triggering build.")
            except Exception as e:
                logger.warning(f"Could not read eval_report.json: {e}")

        if should_build:
            logger.info("Building latest submission tarball...")
            try: subprocess.run([sys.executable, "build_submission.py"], check=True)
            except Exception as e: logger.error(f"Failed to auto-build submission: {e}")


def main():
    pdf_path = "skills/card_pool_reference.pdf"
    output_dir = "visualizer/images"
    os.makedirs(output_dir, exist_ok=True)

    print("Opening PDF...")
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Total pages: {total_pages}")

    # Map card IDs to PDF pages
    # First, let's parse the index pages. We know index pages are pages 0 to 38.
    card_to_page = {}
    
    print("Parsing index pages...")
    for page_idx in range(39):
        page = doc[page_idx]
        text_lines = [line.strip() for line in page.get_text().split("\n") if line.strip()]
        links = page.get_links()

        # Let's filter links pointing to a page in the document (kind=1)
        target_links = [l for l in links if l.get("kind") == 1]
        
        # Parse the rows. Each row has: Card ID, Name, Expansion, Coll No, View Image
        # We can find integers in text_lines that represent Card IDs.
        # Let's match the number of target links with the sequence of Card IDs.
        # In the page text, Card ID is followed by the name, expansion, etc.
        # Let's find all rows by looking for 'View Image'
        view_image_indices = [i for i, line in enumerate(text_lines) if line == "View Image"]
        
        for idx, view_idx in enumerate(view_image_indices):
            # The Card ID should be 4 positions before 'View Image'
            card_id_idx = view_idx - 4
            if card_id_idx >= 0:
                card_id_str = text_lines[card_id_idx]
                # Verify it is a valid integer Card ID
                if card_id_str.isdigit():
                    card_id = int(card_id_str)
                    if idx < len(target_links):
                        target_page = target_links[idx].get("page")
                        if target_page:
                            card_to_page[card_id] = target_page

    print(f"Mapped {len(card_to_page)} cards to pages.")

    # Extract images from mapped pages
    print("Extracting images...")
    extracted_count = 0
    for card_id, page_num in card_to_page.items():
        if page_num >= total_pages:
            continue
            
        page = doc[page_num]
        image_list = page.get_images()
        
        if image_list:
            # Get the first image on the page
            xref = image_list[0][0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            output_filename = f"card_{card_id}.{image_ext}"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            
            extracted_count += 1
            if extracted_count % 100 == 0:
                print(f"Extracted {extracted_count} images...")

    print(f"Completed! Extracted {extracted_count} card images to {output_dir}")


def main():
    import sys
    import os


    has_force_master_arg = False
    if "--force-master" in sys.argv:
        has_force_master_arg = True
    elif "--force" in sys.argv:
        try:
            idx = sys.argv.index("--force")
            if idx + 1 < len(sys.argv) and sys.argv[idx + 1] == "master":
                has_force_master_arg = True
        except ValueError:
            pass

    if has_force_master_arg or os.environ.get("FORCE_MASTER") == "1":
        logger.info("[OVERRIDE] Force Master Mode detected. Bypassing discovery and forcing Master Mode.")
        from factory.orchestrator_master import run_master_loop
        while True:
            try:
                run_master_loop(enable_distributed=True)
            except Exception as e:
                logger.error(f"Master loop crashed: {e}")
                time.sleep(5)
        return

    logger.info("Orchestration Agent (Auto-Discovery Mode) started.")
    from distributed.discovery import WorkerListener
    from distributed.election import run_election
    from factory.orchestrator_master import run_master_loop
    from factory.orchestrator_worker import run_worker_loop
    
    last_seen_master_time = None
    last_known_master_ip = None

    while True:
        try:
            listener = WorkerListener(interface_type="wifi")
            logger.info("[DISCOVERY] Listening for master...")
            master_ip, master_version = listener.listen_for_master()
            
            if master_ip:
                logger.info(f"[DISCOVERY] Found master at {master_ip}. Becoming worker.")
                last_seen_master_time = time.time()
                last_known_master_ip = master_ip
                
                try:
                    from distributed.code_sync import sync_code, restart_process
                    if master_version and sync_code(master_version):
                        restart_process()
                except Exception as sync_e:
                    logger.warning(f"[SYNC] Code synchronization failed: {sync_e}")
                    
                run_worker_loop(master_ip, master_version)
            else:
                grace_period = 300  # 5 minutes
                if last_known_master_ip and last_seen_master_time and (time.time() - last_seen_master_time < grace_period):
                    logger.info(f"[DISCOVERY] Master beacons temporarily missing. Last seen master: {last_known_master_ip}. Retrying direct connect...")
                    try:
                        run_worker_loop(last_known_master_ip, None)
                    except Exception as loop_err:
                        logger.warning(f"Failed direct reconnect: {loop_err}")
                    time.sleep(5)
                else:
                    logger.info("[ELECTION] No master found and grace period expired. Running election...")
                    is_master, winner_ip = run_election(timeout=10)
                    
                    if is_master:
                        logger.info(f"[MASTER] Elected as master ({winner_ip}).")
                        run_master_loop(enable_distributed=True)
                    else:
                        logger.info(f"[WORKER] Master is {winner_ip}. Waiting for beacon...")
                        m_ip, m_version = listener.listen_for_master()
                        
                        try:
                            from distributed.code_sync import sync_code, restart_process
                            if m_version and sync_code(m_version):
                                restart_process()
                        except Exception as sync_e:
                            logger.warning(f"[SYNC] Code synchronization failed: {sync_e}")
                            
                        run_worker_loop(winner_ip, m_version)
        except Exception as e:
            logger.error(f"Critical error in Orchestration Agent loop: {e}")
            time.sleep(5)


def main():
    server = MasterServer()
    server.start()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print the version and exit.",
    )
    parser.add_argument(
        "--includes",
        action="store_true",
        help="Include flags for both pybind11 and Python headers.",
    )
    parser.add_argument(
        "--cmakedir",
        action="store_true",
        help="Print the CMake module directory, ideal for setting -Dpybind11_ROOT in CMake.",
    )
    parser.add_argument(
        "--pkgconfigdir",
        action="store_true",
        help="Print the pkgconfig directory, ideal for setting $PKG_CONFIG_PATH.",
    )
    args = parser.parse_args()
    if not sys.argv[1:]:
        parser.print_help()
    if args.includes:
        print_includes()
    if args.cmakedir:
        print(get_cmake_dir())
    if args.pkgconfigdir:
        print(get_pkgconfig_dir())


def main() -> None:
    from argparse import ArgumentParser, RawDescriptionHelpFormatter

    VERSION = None
    if '--version' in sys.argv:
        # We cannot import sympy before this is run, because flags like -C and
        # -t set environment variables that must be set before SymPy is
        # imported. The only thing we need to import it for is to get the
        # version, which only matters with the --version flag.
        import sympy
        VERSION = sympy.__version__

    usage = 'isympy [options] -- [ipython options]'
    parser = ArgumentParser(
        usage=usage,
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument('--version', action='version', version=VERSION)

    parser.add_argument(
        '-c', '--console',
        dest='console',
        action='store',
        default=None,
        choices=['ipython', 'python'],
        metavar='CONSOLE',
        help='select type of interactive session: ipython | python; defaults '
        'to ipython if IPython is installed, otherwise python')

    parser.add_argument(
        '-p', '--pretty',
        dest='pretty',
        action='store',
        default=None,
        metavar='PRETTY',
        choices=['unicode', 'ascii', 'no'],
        help='setup pretty printing: unicode | ascii | no; defaults to '
        'unicode printing if the terminal supports it, otherwise ascii')

    parser.add_argument(
        '-t', '--types',
        dest='types',
        action='store',
        default=None,
        metavar='TYPES',
        choices=['gmpy', 'gmpy1', 'python'],
        help='setup ground types: gmpy | gmpy1 | python; defaults to gmpy if gmpy2 '
        'or gmpy is installed, otherwise python')

    parser.add_argument(
        '-o', '--order',
        dest='order',
        action='store',
        default=None,
        metavar='ORDER',
        choices=['lex', 'grlex', 'grevlex', 'rev-lex', 'rev-grlex', 'rev-grevlex', 'old', 'none'],
        help='setup ordering of terms: [rev-]lex | [rev-]grlex | [rev-]grevlex | old | none; defaults to lex')

    parser.add_argument(
        '-q', '--quiet',
        dest='quiet',
        action='store_true',
        default=False,
        help='print only version information at startup')

    parser.add_argument(
        '-d', '--doctest',
        dest='doctest',
        action='store_true',
        default=False,
        help='use the doctest format for output (you can just copy and paste it)')

    parser.add_argument(
        '-C', '--no-cache',
        dest='cache',
        action='store_false',
        default=True,
        help='disable caching mechanism')

    parser.add_argument(
        '-a', '--auto-symbols',
        dest='auto_symbols',
        action='store_true',
        default=False,
        help='automatically construct missing symbols')

    parser.add_argument(
        '-i', '--int-to-Integer',
        dest='auto_int_to_Integer',
        action='store_true',
        default=False,
        help="automatically wrap int literals with Integer")

    parser.add_argument(
        '-I', '--interactive',
        dest='interactive',
        action='store_true',
        default=False,
        help="equivalent to -a -i")

    parser.add_argument(
        '-D', '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='enable debugging output')

    (options, ipy_args) = parser.parse_known_args()
    if '--' in ipy_args:
        ipy_args.remove('--')

    if not options.cache:
        os.environ['SYMPY_USE_CACHE'] = 'no'

    if options.types:
        os.environ['SYMPY_GROUND_TYPES'] = options.types

    if options.debug:
        os.environ['SYMPY_DEBUG'] = str(options.debug)

    if options.doctest:
        options.pretty = 'no'
        options.console = 'python'

    session = options.console

    if session is not None:
        ipython = session == 'ipython'
    else:
        try:
            import IPython # noqa: F401
            ipython = True
        except ImportError:
            if not options.quiet:
                from sympy.interactive.session import no_ipython
                print(no_ipython)
            ipython = False

    args = {
        'pretty_print': True,
        'use_unicode':  None,
        'use_latex':    None,
        'order':        None,
        'argv':         ipy_args,
    }

    if options.pretty == 'unicode':
        args['use_unicode'] = True
    elif options.pretty == 'ascii':
        args['use_unicode'] = False
    elif options.pretty == 'no':
        args['pretty_print'] = False

    if options.order is not None:
        args['order'] = options.order

    args['quiet'] = options.quiet
    args['auto_symbols'] = options.auto_symbols or options.interactive
    args['auto_int_to_Integer'] = options.auto_int_to_Integer or options.interactive

    from sympy.interactive import init_session
    init_session(ipython, **args)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    opar = optparse.OptionParser()
    opar.add_option("-d", "--dot", dest="dot",
                    help="output a graphviz dot file", action="store_true")
    opar.add_option("-m", "--min", dest="threshold",
                    help="minimum complexity for output", type="int",
                    default=1)

    options, args = opar.parse_args(argv)

    code = _read(args[0])
    tree = compile(code, args[0], "exec", ast.PyCF_ONLY_AST)
    visitor = PathGraphingAstVisitor()
    visitor.preorder(tree, visitor)

    if options.dot:
        print('graph {')
        for graph in visitor.graphs.values():
            if (not options.threshold or
                    graph.complexity() >= options.threshold):
                graph.to_dot()
        print('}')
    else:
        for graph in visitor.graphs.values():
            if graph.complexity() >= options.threshold:
                print(graph.name, graph.complexity())


def main(argv: list[str]) -> None:
    arg_parser = ArgumentParser(
        description="aiohttp.web Application server", prog="aiohttp.web"
    )
    arg_parser.add_argument(
        "entry_func",
        help=(
            "Callable returning the `aiohttp.web.Application` instance to "
            "run. Should be specified in the 'module:function' syntax."
        ),
        metavar="entry-func",
    )
    arg_parser.add_argument(
        "-H",
        "--hostname",
        help="TCP/IP hostname to serve on (default: localhost)",
        default=None,
    )
    arg_parser.add_argument(
        "-P",
        "--port",
        help="TCP/IP port to serve on (default: %(default)r)",
        type=int,
        default=8080,
    )
    arg_parser.add_argument(
        "-U",
        "--path",
        help="Unix file system path to serve on. Can be combined with hostname "
        "to serve on both Unix and TCP.",
    )
    args, extra_argv = arg_parser.parse_known_args(argv)

    # Import logic
    mod_str, _, func_str = args.entry_func.partition(":")
    if not func_str or not mod_str:
        arg_parser.error("'entry-func' not in 'module:function' syntax")
    if mod_str.startswith("."):
        arg_parser.error("relative module names not supported")
    try:
        module = import_module(mod_str)
    except ImportError as ex:
        arg_parser.error(f"unable to import {mod_str}: {ex}")
    try:
        func = getattr(module, func_str)
    except AttributeError:
        arg_parser.error(f"module {mod_str!r} has no attribute {func_str!r}")

    # Compatibility logic
    if args.path is not None and not hasattr(socket, "AF_UNIX"):
        arg_parser.error(
            "file system paths not supported by your operating environment"
        )

    logging.basicConfig(level=logging.DEBUG)

    if args.path and args.hostname is None:
        host = port = None
    else:
        host = args.hostname or "localhost"
        port = args.port

    app = func(extra_argv)
    run_app(app, host=host, port=port, path=args.path)
    arg_parser.exit(message="Stopped\n")


def main() -> None:
    args = get_args()
    sess = get_session()

    # Make a request to get a response
    resp = sess.get(args.url)

    # Turn on logging
    setup_logging()

    # try setting the cache
    cache_controller: CacheController = (
        sess.cache_controller  # type: ignore[attr-defined]
    )
    cache_controller.cache_response(resp.request, resp.raw)

    # Now try to get it
    if cache_controller.cached_request(resp.request):
        print("Cached!")
    else:
        print("Not cached :(")


def main() -> None:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    parser = argparse.ArgumentParser(description="OS distro info tool")
    parser.add_argument(
        "--json", "-j", help="Output in machine readable format", action="store_true"
    )

    parser.add_argument(
        "--root-dir",
        "-r",
        type=str,
        dest="root_dir",
        help="Path to the root filesystem directory (defaults to /)",
    )

    args = parser.parse_args()

    if args.root_dir:
        dist = LinuxDistribution(
            include_lsb=False,
            include_uname=False,
            include_oslevel=False,
            root_dir=args.root_dir,
        )
    else:
        dist = _distro

    if args.json:
        logger.info(json.dumps(dist.info(), indent=4, sort_keys=True))
    else:
        logger.info("Name: %s", dist.name(pretty=True))
        distribution_version = dist.version(pretty=True)
        logger.info("Version: %s", distribution_version)
        distribution_codename = dist.codename()
        logger.info("Codename: %s", distribution_codename)


def main():
    if len(sys.argv) == 2:
        definition = sys.argv[1]
    else:
        definition = sys.stdin.read()

    definition = json.loads(definition)
    code = compile_to_code(definition)
    print(code)


def main() -> None:
    cli.main()


def main():
    """Show this help"""
    path = fontTools.__path__
    descriptions = {}
    for pkg in sorted(
        mod.name
        for mod in pkgutil.walk_packages([fontTools.__path__[0]], prefix="fontTools.")
    ):
        try:
            imports = __import__(pkg, globals(), locals(), ["main"])
        except ImportError as e:
            continue
        try:
            description = imports.main.__doc__
            # Cython modules seem to return "main()" as the docstring
            if description and description != "main()":
                pkg = pkg.replace("fontTools.", "").replace(".__main__", "")
                # show the docstring's first line only
                descriptions[pkg] = description.splitlines()[0]
        except AttributeError as e:
            pass
    for pkg, description in descriptions.items():
        print("fonttools %-25s %s" % (pkg, description), file=sys.stderr)


def main(args=None):
    """Convert OpenType fonts to XML and back"""
    from fontTools import configLogger

    if args is None:
        args = sys.argv[1:]
    try:
        jobs, options = parseOptions(args)
    except getopt.GetoptError as e:
        print("%s\nERROR: %s" % (__doc__, e), file=sys.stderr)
        sys.exit(2)

    configLogger(level=options.logLevel)

    try:
        process(jobs, options)
    except KeyboardInterrupt:
        log.error("(Cancelled.)")
        sys.exit(1)
    except SystemExit:
        raise
    except TTLibError as e:
        log.error(e)
        sys.exit(1)
    except:
        log.exception("Unhandled exception has occurred")
        sys.exit(1)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    # TODO Handle library-wide options. Eg.:
    # --unicodedata
    # --verbose / other logging stuff

    # TODO Allow a way to run arbitrary modules? Useful for setting
    # library-wide options and calling another library. Eg.:
    #
    #   $ fonttools --unicodedata=... fontmake ...
    #
    # This allows for a git-like command where thirdparty commands
    # can be added.  Should we just try importing the fonttools
    # module first and try without if it fails?

    if len(sys.argv) < 2:
        sys.argv.append("help")
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        sys.argv[1] = "help"
    mod = "fontTools." + sys.argv[1]
    sys.argv[1] = sys.argv[0] + " " + sys.argv[1]
    del sys.argv[0]

    import runpy

    runpy.run_module(mod, run_name="__main__")


def main(args):
    """Mount filesystem from chained URL to MOUNT_POINT.

    Examples:

    python3 -m fsspec.fuse memory /usr/share /tmp/mem

    python3 -m fsspec.fuse local /tmp/source /tmp/local \\
            -l /tmp/fsspecfuse.log

    You can also mount chained-URLs and use special settings:

    python3 -m fsspec.fuse 'filecache::zip::file://data.zip' \\
            / /tmp/zip \\
            -o 'filecache-cache_storage=/tmp/simplecache'

    You can specify the type of the setting by using `[int]` or `[bool]`,
    (`true`, `yes`, `1` represents the Boolean value `True`):

    python3 -m fsspec.fuse 'simplecache::ftp://ftp1.at.proftpd.org' \\
            /historic/packages/RPMS /tmp/ftp \\
            -o 'simplecache-cache_storage=/tmp/simplecache' \\
            -o 'simplecache-check_files=false[bool]' \\
            -o 'ftp-listings_expiry_time=60[int]' \\
            -o 'ftp-username=anonymous' \\
            -o 'ftp-password=xieyanbo'
    """

    class RawDescriptionArgumentParser(argparse.ArgumentParser):
        def format_help(self):
            usage = super().format_help()
            parts = usage.split("\n\n")
            parts[1] = self.description.rstrip()
            return "\n\n".join(parts)

    parser = RawDescriptionArgumentParser(prog="fsspec.fuse", description=main.__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("url", type=str, help="fs url")
    parser.add_argument("source_path", type=str, help="source directory in fs")
    parser.add_argument("mount_point", type=str, help="local directory")
    parser.add_argument(
        "-o",
        "--option",
        action="append",
        help="Any options of protocol included in the chained URL",
    )
    parser.add_argument(
        "-l", "--log-file", type=str, help="Logging FUSE debug info (Default: '')"
    )
    parser.add_argument(
        "-f",
        "--foreground",
        action="store_false",
        help="Running in foreground or not (Default: False)",
    )
    parser.add_argument(
        "-t",
        "--threads",
        action="store_false",
        help="Running with threads support (Default: False)",
    )
    parser.add_argument(
        "-r",
        "--ready-file",
        action="store_false",
        help="The `.fuse_ready` file will exist after FUSE is ready. "
        "(Debugging purpose, Default: False)",
    )
    args = parser.parse_args(args)

    kwargs = {}
    for item in args.option or []:
        key, sep, value = item.partition("=")
        if not sep:
            parser.error(message=f"Wrong option: {item!r}")
        val = value.lower()
        if val.endswith("[int]"):
            value = int(value[: -len("[int]")])
        elif val.endswith("[bool]"):
            value = val[: -len("[bool]")] in ["1", "yes", "true"]

        if "-" in key:
            fs_name, setting_name = key.split("-", 1)
            if fs_name in kwargs:
                kwargs[fs_name][setting_name] = value
            else:
                kwargs[fs_name] = {setting_name: value}
        else:
            kwargs[key] = value

    if args.log_file:
        logging.basicConfig(
            level=logging.DEBUG,
            filename=args.log_file,
            format="%(asctime)s %(message)s",
        )

        class LoggingFUSEr(FUSEr, LoggingMixIn):
            pass

        fuser = LoggingFUSEr
    else:
        fuser = FUSEr

    fs, url_path = url_to_fs(args.url, **kwargs)
    logger.debug("Mounting %s to %s", url_path, str(args.mount_point))
    run(
        fs,
        args.source_path,
        args.mount_point,
        foreground=args.foreground,
        threads=args.threads,
        ready_file=args.ready_file,
        ops_class=fuser,
    )


def main(
    url: str,
    method: str,
    params: list[tuple[str, str]],
    content: str,
    data: list[tuple[str, str]],
    files: list[tuple[str, click.File]],
    json: str,
    headers: list[tuple[str, str]],
    cookies: list[tuple[str, str]],
    auth: tuple[str, str] | None,
    proxy: str,
    timeout: float,
    follow_redirects: bool,
    verify: bool,
    http2: bool,
    download: typing.BinaryIO | None,
    verbose: bool,
) -> None:
    """
    An HTTP command line client.
    Sends a request and displays the response.
    """
    if not method:
        method = "POST" if content or data or files or json else "GET"

    try:
        with Client(proxy=proxy, timeout=timeout, http2=http2, verify=verify) as client:
            with client.stream(
                method,
                url,
                params=list(params),
                content=content,
                data=dict(data),
                files=files,  # type: ignore
                json=json,
                headers=headers,
                cookies=dict(cookies),
                auth=auth,
                follow_redirects=follow_redirects,
                extensions={"trace": functools.partial(trace, verbose=verbose)},
            ) as response:
                if download is not None:
                    download_response(response, download)
                else:
                    response.read()
                    if response.content:
                        print_response(response)

    except RequestError as exc:
        console = rich.console.Console()
        console.print(f"[red]{type(exc).__name__}[/red]: {exc}")
        sys.exit(1)

    sys.exit(0 if response.is_success else 1)


def main(argv: Optional[list[str]] = None) -> int:
    """Entry point for ``python -m idna``.

    When more than one domain is supplied (via positional arguments or
    piped stdin) and no mode flag is given, the first input determines
    the direction and that mode is applied uniformly to the rest.

    :param argv: Argument list excluding the program name. Defaults to
        :data:`sys.argv` when ``None``.
    :returns: ``0`` on success, ``1`` if any conversion fails.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)
    uts46 = not args.strict

    if args.domain:
        domains: Iterable[str] = args.domain
    elif not sys.stdin.isatty():
        domains = _iter_stdin(sys.stdin)
    else:
        parser.error("a domain argument is required when stdin is a terminal")

    iterator = iter(domains)
    first = next(iterator, None)
    if first is None:
        return 0

    mode = args.mode or ("decode" if _looks_like_alabel(first) else "encode")

    results = [_convert_one(domain, mode, uts46) for domain in chain([first], iterator)]
    return 0 if all(results) else 1


def main(argv: Sequence[str] | None = None, stdin: TextIOWrapper | None = None) -> None:
    arguments = parse_args(argv)
    if arguments.get("show_version"):
        print(ASCII_ART)
        return

    show_config: bool = arguments.pop("show_config", False)
    show_files: bool = arguments.pop("show_files", False)
    if show_config and show_files:
        sys.exit("Error: either specify show-config or show-files not both.")

    if "settings_path" in arguments:
        if os.path.isfile(arguments["settings_path"]):
            arguments["settings_file"] = os.path.abspath(arguments["settings_path"])
            arguments["settings_path"] = os.path.dirname(arguments["settings_file"])
        else:
            arguments["settings_path"] = os.path.abspath(arguments["settings_path"])

    if "virtual_env" in arguments:
        venv = arguments["virtual_env"]
        arguments["virtual_env"] = os.path.abspath(venv)
        if not os.path.isdir(arguments["virtual_env"]):
            warn(f"virtual_env dir does not exist: {arguments['virtual_env']}", stacklevel=2)

    file_names = arguments.pop("files", [])
    if not file_names and not show_config:
        print(QUICK_GUIDE)
        if arguments:
            sys.exit("Error: arguments passed in without any paths or content.")
        return
    if "settings_path" not in arguments:
        arguments["settings_path"] = (
            arguments.get("filename", None) or os.getcwd()
            if file_names == ["-"]
            else os.path.abspath(file_names[0] if file_names else ".")
        )
        if not os.path.isdir(arguments["settings_path"]):
            arguments["settings_path"] = os.path.dirname(arguments["settings_path"])

    config_dict = arguments.copy()
    ask_to_apply = config_dict.pop("ask_to_apply", False)
    jobs = config_dict.pop("jobs", None)
    check = config_dict.pop("check", False)
    show_diff = config_dict.pop("show_diff", False)
    write_to_stdout = config_dict.pop("write_to_stdout", False)
    deprecated_flags = config_dict.pop("deprecated_flags", False)
    remapped_deprecated_args = config_dict.pop("remapped_deprecated_args", False)
    stream_filename = config_dict.pop("filename", None)
    ext_format = config_dict.pop("ext_format", None)
    allow_root = config_dict.pop("allow_root", None)
    resolve_all_configs = config_dict.pop("resolve_all_configs", False)
    wrong_sorted_files = False
    all_attempt_broken = False
    no_valid_encodings = False

    config_trie: Trie | None = None
    if resolve_all_configs:
        config_trie = find_all_configs(config_dict.pop("config_root", "."))

    if "src_paths" in config_dict:
        config_dict["src_paths"] = {
            Path(src_path).resolve() for src_path in config_dict.get("src_paths", ())
        }

    config = Config(**config_dict)
    if show_config:
        print(json.dumps(config.__dict__, indent=4, separators=(",", ": "), default=_preconvert))
        return
    if file_names == ["-"]:
        file_path = Path(stream_filename) if stream_filename else None
        if show_files:
            sys.exit("Error: can't show files for streaming input.")

        input_stream = sys.stdin if stdin is None else stdin
        if check:
            incorrectly_sorted = not api.check_stream(
                input_stream=input_stream,
                config=config,
                show_diff=show_diff,
                file_path=file_path,
                extension=ext_format,
            )

            wrong_sorted_files = incorrectly_sorted
        else:
            try:
                api.sort_stream(
                    input_stream=input_stream,
                    output_stream=sys.stdout,
                    config=config,
                    show_diff=show_diff,
                    file_path=file_path,
                    extension=ext_format,
                    raise_on_skip=False,
                )
            except FileSkipped:
                sys.stdout.write(input_stream.read())
    elif "/" in file_names and not allow_root:
        printer = create_terminal_printer(
            color=config.color_output, error=config.format_error, success=config.format_success
        )
        printer.error("it is dangerous to operate recursively on '/'")
        printer.error("use --allow-root to override this failsafe")
        sys.exit(1)
    else:
        if stream_filename:
            printer = create_terminal_printer(
                color=config.color_output, error=config.format_error, success=config.format_success
            )
            printer.error("Filename override is intended only for stream (-) sorting.")
            sys.exit(1)
        skipped: list[str] = []
        broken: list[str] = []

        if config.filter_files:
            filtered_files = []
            for file_name in file_names:
                if config.is_skipped(Path(file_name)):
                    skipped.append(str(Path(file_name).resolve()))
                else:
                    filtered_files.append(file_name)
            file_names = filtered_files

        file_names = files.find(file_names, config, skipped, broken)
        if show_files:
            for file_name in file_names:
                print(file_name)
            return
        num_skipped = 0
        num_broken = 0
        num_invalid_encoding = 0
        if config.verbose:
            print(ASCII_ART)

        if jobs:
            import multiprocessing.pool  # noqa: PLC0415

            executor_ctx: multiprocessing.pool.Pool | AbstractContextManager[None] = (
                multiprocessing.pool.Pool(jobs if jobs > 0 else multiprocessing.cpu_count())
            )
        else:
            executor_ctx = nullcontext()

        with executor_ctx as executor:
            if executor is not None:
                attempt_iterator = executor.imap(
                    functools.partial(
                        sort_imports,
                        config=config,
                        check=check,
                        ask_to_apply=ask_to_apply,
                        show_diff=show_diff,
                        write_to_stdout=write_to_stdout,
                        extension=ext_format,
                        config_trie=config_trie,
                    ),
                    file_names,
                )
            else:
                # https://github.com/python/typeshed/pull/2814
                attempt_iterator = (
                    sort_imports(  # type: ignore
                        file_name,
                        config=config,
                        check=check,
                        ask_to_apply=ask_to_apply,
                        show_diff=show_diff,
                        write_to_stdout=write_to_stdout,
                        extension=ext_format,
                        config_trie=config_trie,
                    )
                    for file_name in file_names
                )

            # If any files passed in are missing considered as error, should be removed
            is_no_attempt = True
            any_encoding_valid = False
            for sort_attempt in attempt_iterator:
                if not sort_attempt:
                    continue  # pragma: no cover - shouldn't happen, satisfies type constraint
                incorrectly_sorted = sort_attempt.incorrectly_sorted
                if arguments.get("check", False) and incorrectly_sorted:
                    wrong_sorted_files = True
                if sort_attempt.skipped:
                    num_skipped += (
                        1  # pragma: no cover - shouldn't happen, due to skip in iter_source_code
                    )

                if not sort_attempt.supported_encoding:
                    num_invalid_encoding += 1
                else:
                    any_encoding_valid = True

                is_no_attempt = False

        num_skipped += len(skipped)
        if num_skipped and not config.quiet:
            if config.verbose:
                for was_skipped in skipped:
                    print(
                        f"{was_skipped} was skipped as it's listed in 'skip' setting, "
                        "matches a glob in 'skip_glob' setting, or is in a .gitignore file with "
                        "--skip-gitignore enabled."
                    )
            print(f"Skipped {num_skipped} files")

        num_broken += len(broken)
        if num_broken and not config.quiet:
            if config.verbose:
                for was_broken in broken:
                    warn(
                        f"{was_broken} was broken path, make sure it exists correctly", stacklevel=2
                    )
            print(f"Broken {num_broken} paths")

        if num_broken > 0 and is_no_attempt:
            all_attempt_broken = True
        if num_invalid_encoding > 0 and not any_encoding_valid:
            no_valid_encodings = True

    if not config.quiet and (remapped_deprecated_args or deprecated_flags):
        if remapped_deprecated_args:
            warn(
                "W0502: The following deprecated single dash CLI flags were used and translated: "
                f"{', '.join(remapped_deprecated_args)}!",
                stacklevel=2,
            )
        if deprecated_flags:
            warn(
                "W0501: The following deprecated CLI flags were used and ignored: "
                f"{', '.join(deprecated_flags)}!",
                stacklevel=2,
            )
        warn(
            "W0500: Please see the 5.0.0 Upgrade guide: "
            "https://pycqa.github.io/isort/docs/upgrade_guides/5.0.0.html",
            stacklevel=2,
        )

    if wrong_sorted_files:
        sys.exit(1)

    if all_attempt_broken:
        sys.exit(1)

    if no_valid_encodings:
        printer = create_terminal_printer(
            color=config.color_output, error=config.format_error, success=config.format_success
        )
        printer.error("No valid encodings.")
        sys.exit(1)


def main(known_args, unknown_flags):
  xprof_options = _parse_xprof_flags(unknown_flags)
  collect_profile(
      known_args.port,
      known_args.duration_in_ms,
      known_args.host,
      known_args.log_dir,
      known_args.no_perfetto_link,
      xprof_options,
  )


def main(args=sys.argv[1:]):  # noqa: D103
    sys.exit(run(arguments=parse_args(args=args)))


def main() -> None:
    """The command entry point."""
    parser = jupyter_parser()
    argv = sys.argv
    subcommand = None
    if "_ARGCOMPLETE" in os.environ:
        argv = _evaluate_argcomplete(parser)
        subcommand = argv[1]
    elif len(argv) > 1 and not argv[1].startswith("-"):
        # Don't parse if a subcommand is given
        # Avoids argparse gobbling up args passed to subcommand, such as `-h`.
        subcommand = argv[1]
    else:
        args, _opts = parser.parse_known_args()
        subcommand = args.subcommand
        if args.version:
            print("Selected Jupyter core packages...")
            for package in [
                "IPython",
                "ipykernel",
                "ipywidgets",
                "jupyter_client",
                "jupyter_core",
                "jupyter_server",
                "jupyterlab",
                "nbclient",
                "nbconvert",
                "nbformat",
                "notebook",
                "qtconsole",
                "traitlets",
            ]:
                try:
                    if package == "jupyter_core":  # We're already here
                        version = __version__
                    else:
                        mod = __import__(package)
                        version = mod.__version__
                except ImportError:
                    version = "not installed"
                print(f"{package:<17}:", version)
            return
        if args.json and not args.paths:
            sys.exit("--json is only used with --paths")
        if args.debug and not args.paths:
            sys.exit("--debug is only used with --paths")
        if args.debug and args.json:
            sys.exit("--debug cannot be used with --json")
        if args.config_dir:
            print(paths.jupyter_config_dir())
            return
        if args.data_dir:
            print(paths.jupyter_data_dir())
            return
        if args.runtime_dir:
            print(paths.jupyter_runtime_dir())
            return
        if args.paths:
            data = {}
            data["runtime"] = [paths.jupyter_runtime_dir()]
            data["config"] = paths.jupyter_config_path()
            data["data"] = paths.jupyter_path()
            if args.json:
                print(json.dumps(data))
            else:
                if args.debug:
                    env = os.environ

                    if paths.use_platform_dirs():
                        print(
                            "JUPYTER_PLATFORM_DIRS is set to a true value, so we use platformdirs to find platform-specific directories"
                        )
                    else:
                        print(
                            "JUPYTER_PLATFORM_DIRS is set to a false value, or is not set, so we use hardcoded legacy paths for platform-specific directories"
                        )

                    if paths.prefer_environment_over_user():
                        print(
                            "JUPYTER_PREFER_ENV_PATH is set to a true value, or JUPYTER_PREFER_ENV_PATH is not set and we detected a virtual environment, making the environment-level path preferred over the user-level path for data and config"
                        )
                    else:
                        print(
                            "JUPYTER_PREFER_ENV_PATH is set to a false value, or JUPYTER_PREFER_ENV_PATH is not set and we did not detect a virtual environment, making the user-level path preferred over the environment-level path for data and config"
                        )

                    # config path list
                    if env.get("JUPYTER_NO_CONFIG"):
                        print(
                            "JUPYTER_NO_CONFIG is set, making the config path list only a single temporary directory"
                        )
                    else:
                        print(
                            "JUPYTER_NO_CONFIG is not set, so we use the full path list for config"
                        )

                    if env.get("JUPYTER_CONFIG_PATH"):
                        print(
                            f"JUPYTER_CONFIG_PATH is set to '{env.get('JUPYTER_CONFIG_PATH')}', which is prepended to the config path list (unless JUPYTER_NO_CONFIG is set)"
                        )
                    else:
                        print(
                            "JUPYTER_CONFIG_PATH is not set, so we do not prepend anything to the config paths"
                        )

                    if env.get("JUPYTER_CONFIG_DIR"):
                        print(
                            f"JUPYTER_CONFIG_DIR is set to '{env.get('JUPYTER_CONFIG_DIR')}', overriding the default user-level config directory"
                        )
                    else:
                        print(
                            "JUPYTER_CONFIG_DIR is not set, so we use the default user-level config directory"
                        )

                    if site.ENABLE_USER_SITE:
                        print(
                            f"Python's site.ENABLE_USER_SITE is True, so we add the user site directory '{site.getuserbase()}'"
                        )
                    else:
                        print(
                            f"Python's site.ENABLE_USER_SITE is not True, so we do not add the Python site user directory '{site.getuserbase()}'"
                        )

                    # data path list
                    if env.get("JUPYTER_PATH"):
                        print(
                            f"JUPYTER_PATH is set to '{env.get('JUPYTER_PATH')}', which is prepended to the data paths"
                        )
                    else:
                        print(
                            "JUPYTER_PATH is not set, so we do not prepend anything to the data paths"
                        )

                    if env.get("JUPYTER_DATA_DIR"):
                        print(
                            f"JUPYTER_DATA_DIR is set to '{env.get('JUPYTER_DATA_DIR')}', overriding the default user-level data directory"
                        )
                    else:
                        print(
                            "JUPYTER_DATA_DIR is not set, so we use the default user-level data directory"
                        )

                    # runtime directory
                    if env.get("JUPYTER_RUNTIME_DIR"):
                        print(
                            f"JUPYTER_RUNTIME_DIR is set to '{env.get('JUPYTER_RUNTIME_DIR')}', overriding the default runtime directory"
                        )
                    else:
                        print(
                            "JUPYTER_RUNTIME_DIR is not set, so we use the default runtime directory"
                        )

                    print()

                for name in sorted(data):
                    path = data[name]
                    print(f"{name}:")
                    for p in path:
                        print("    " + p)
            return

    if not subcommand:
        parser.print_help(file=sys.stderr)
        sys.exit("\nPlease specify a subcommand or one of the optional arguments.")

    try:
        command = _jupyter_abspath(subcommand)
    except Exception as e:
        parser.print_help(file=sys.stderr)
        # special-case alias of "jupyter help" to "jupyter --help"
        if subcommand == "help":
            return
        sys.exit(str(e))

    try:
        _execvp(command, [command, *argv[2:]])
    except OSError as e:
        sys.exit(f"Error executing Jupyter command {subcommand!r}: {e}")


def main() -> None:
    """
    print out useful info
    """
    # pylint: disable=superfluous-parens
    # args = get_args()
    if "_ARGCOMPLETE" in os.environ:
        # No arguments to complete, the script can be slow to run to completion,
        # so in case someone tries to complete jupyter troubleshoot just exit early
        return

    environment_data = get_data()

    print("$PATH:")
    for directory in environment_data["path"].split(os.pathsep):
        print(f"\t{directory}")

    print("\nsys.path:")
    for directory in environment_data["sys_path"]:
        print(f"\t{directory}")

    print("\nsys.executable:")
    print(f"\t{environment_data['sys_exe']}")

    print("\nsys.version:")
    if "\n" in environment_data["sys_version"]:
        for data in environment_data["sys_version"].split("\n"):
            print(f"\t{data}")
    else:
        print(f"\t{environment_data['sys_version']}")

    print("\nplatform.platform():")
    print(f"\t{environment_data['platform']}")

    if environment_data["which"]:
        print("\nwhich -a jupyter:")
        for line in environment_data["which"].split("\n"):
            print(f"\t{line}")

    if environment_data["where"]:
        print("\nwhere jupyter:")
        for line in environment_data["where"].split("\n"):
            print(f"\t{line}")

    if environment_data["pip"]:
        print("\npip list:")
        for package in environment_data["pip"].split("\n"):
            print(f"\t{package}")

    if environment_data["conda"]:
        print("\nconda list:")
        for package in environment_data["conda"].split("\n"):
            print(f"\t{package}")

    if environment_data["conda-env"]:
        print("\nconda env:")
        for package in environment_data["conda-env"].split("\n"):
            print(f"\t{package}")


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--settings-file",
        default=Path(jupyter_core_paths.jupyter_config_dir()) / "labconfig" / "default_setting_overrides.json",
    )
    subparsers = parser.add_subparsers(required=True)
    for subcommand in SUBCOMMANDS:
        subparser = subparsers.add_parser(subcommand.name, help=subcommand.help)
        subparser.set_defaults(subcommand=subcommand)
        subcommand.fill_parser(subparser)
    args = parser.parse_args(sys.argv[1:] or ["--help"])
    return args.subcommand.main(args)


def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="Print the Kaggle CLI version",
        version="Kaggle CLI " + kaggle.__version__,
    )
    parser.add_argument(
        "-W",
        "--no-warn",
        dest="disable_version_warning",
        action="store_true",
        help="Disable out-of-date API version warning",
    )

    subparsers = parser.add_subparsers(title="commands", help=Help.kaggle, dest="command")
    subparsers.required = True
    subparsers.choices = Help.kaggle_choices  # type: ignore[assignment]
    parse_competitions(subparsers)
    parse_datasets(subparsers)
    parse_kernels(subparsers)
    parse_models(subparsers)
    parse_files(subparsers)
    parse_forums(subparsers)
    parse_benchmarks(subparsers)
    parse_config(subparsers)
    parse_auth(subparsers)
    parse_quota(subparsers)
    args = parser.parse_args()
    command_args = {}
    command_args.update(vars(args))
    del command_args["func"]
    del command_args["command"]
    if command_args["disable_version_warning"]:
        KaggleApi.already_printed_version_warning = True
    del command_args["disable_version_warning"]
    error = False
    try:
        out = args.func(**command_args)
    except HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            print_auth_help()
        else:
            print(e, file=sys.stderr)
        out = None
        error = True
    except ApiException as e:
        print(e, file=sys.stderr)
        out = None
        error = True
    except ValueError as e:
        print(e, file=sys.stderr)
        out = None
        error = True
    except KeyboardInterrupt:
        print("User cancelled operation")
        out = None
    if out is not None:
        print(out, end="")

    # This is so that scripts that pick up on error codes can tell when there was a failure
    if error:
        exit(1)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    null_name = args.null or None
    report = analyze(
        Path(args.csv), args.baseline, null_name,
        args.permutations, args.seed,
    )
    if args.out:
        Path(args.out).write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)
    return 0


def main() -> int | None:
    args = parse_args(vars(parser.parse_args()))
    if args.action == "http-server":
        action_http(args)
        return None
    else:
        result = action_handler(args)
        if args.out_path is None:
            print(result)
        else:
            with open(args.out_path, encoding="utf-8", mode="w") as out_file:
                out_file.write(str(result))

        return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert binary cache files to JSON. "
        "Create files in the same directory with extra .json extension."
    )
    parser.add_argument(
        "path", nargs="+", help="mypy cache data file to convert (.data.ff extension)"
    )
    args = parser.parse_args()
    fnams: list[str] = args.path
    for fnam in fnams:
        if fnam.endswith(".data.ff"):
            is_data = True
        elif fnam.endswith(".meta.ff"):
            is_data = False
        else:
            sys.exit(f"error: Expected .data.ff or .meta.ff extension, but got {fnam}")
        with open(fnam, "rb") as f:
            data = f.read()
        if is_data:
            json_data = convert_binary_cache_to_json(data)
        else:
            data_file = fnam.removesuffix(".meta.ff") + ".data.ff"
            json_data = convert_binary_cache_meta_to_json(data, data_file)
        new_fnam = fnam + ".json"
        with open(new_fnam, "w") as f:
            json.dump(json_data, f)
        print(f"{fnam} -> {new_fnam}")


def main(
    *,
    args: list[str] | None = None,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
    clean_exit: bool = False,
) -> None:
    """Main entry point to the type checker.

    Args:
        args: Custom command-line arguments.  If not given, sys.argv[1:] will
            be used.
        clean_exit: Don't hard kill the process on exit. This allows catching
            SystemExit.
    """
    util.check_python_version("mypy")
    t0 = time.time()
    # To log stat() calls: os.stat = stat_proxy
    sys.setrecursionlimit(RECURSION_LIMIT)
    if args is None:
        args = sys.argv[1:]

    # Write an escape sequence instead of raising an exception on encoding errors.
    if isinstance(stdout, TextIOWrapper) and stdout.errors == "strict":
        stdout.reconfigure(errors="backslashreplace")

    fscache = FileSystemCache()
    sources, options = process_options(args, stdout=stdout, stderr=stderr, fscache=fscache)
    if clean_exit:
        options.fast_exit = False

    formatter = util.FancyFormatter(
        stdout, stderr, options.hide_error_codes, hide_success=bool(options.output)
    )

    if options.num_workers:
        # Supporting both parsers would be really tricky, so just support the new one.
        options.native_parser = True
        if options.num_workers < 0:
            fail("error: Number of workers cannot be negative", stderr, options)
        if options.cache_dir == os.devnull:
            fail("error: Cache must be enabled in parallel mode", stderr, options)
        if not options.local_partial_types:
            fail("error: --local-partial-types must be enabled in parallel mode", stderr, options)
        if options.report_dirs:
            fail(
                "error: Reports are not supported in parallel mode yet\n"
                "note: Use -n0 to disable parallel checking",
                stderr,
                options,
            )

    if options.allow_redefinition and not options.local_partial_types:
        fail(
            "error: --local-partial-types must be enabled if using --allow-redefinition",
            stderr,
            options,
        )

    if options.allow_redefinition and options.allow_redefinition_old:
        fail(
            "--allow-redefinition-old and --allow-redefinition should not be used together",
            stderr,
            options,
        )

    if options.install_types and (stdout is not sys.stdout or stderr is not sys.stderr):
        # Since --install-types performs user input, we want regular stdout and stderr.
        fail("error: --install-types not supported in this mode of running mypy", stderr, options)

    if options.non_interactive and not options.install_types:
        fail("error: --non-interactive is only supported with --install-types", stderr, options)

    if options.install_types and not options.incremental:
        fail(
            "error: --install-types not supported with incremental mode disabled", stderr, options
        )

    if options.install_types and options.python_executable is None:
        fail(
            "error: --install-types not supported without python executable or site packages",
            stderr,
            options,
        )

    if options.install_types and not sources:
        install_types(formatter, options, non_interactive=options.non_interactive)
        return

    res, messages, blockers = run_build(sources, options, fscache, t0, stdout, stderr)

    if options.non_interactive:
        missing_pkgs = read_types_packages_to_install(options.cache_dir, after_run=True)
        if missing_pkgs:
            # Install missing type packages and rerun build.
            install_types(formatter, options, after_run=True, non_interactive=True)
            fscache.flush()
            print()
            res, messages, blockers = run_build(sources, options, fscache, t0, stdout, stderr)
        show_messages(messages, stderr, formatter, options)

    if MEM_PROFILE:
        from mypy.memprofile import print_memory_profile

        print_memory_profile()

    code = 0
    n_errors, n_notes, n_files = util.count_stats(messages)
    if messages and n_notes < len(messages):
        code = 2 if blockers else 1
    if options.error_summary:
        if n_errors:
            summary = formatter.format_error(
                n_errors, n_files, len(sources), blockers=blockers, use_color=options.color_output
            )
            stdout.write(summary + "\n")
        # Only notes should also output success
        elif not messages or n_notes == len(messages):
            stdout.write(formatter.format_success(len(sources), options.color_output) + "\n")
        stdout.flush()

    if options.install_types and not options.non_interactive:
        result = install_types(formatter, options, after_run=True, non_interactive=False)
        if result:
            print()
            print("note: Run mypy again for up-to-date results with installed types")
            code = 2

    if options.fast_exit:
        # Exit without freeing objects -- it's faster.
        #
        # NOTE: We don't flush all open files on exit (or run other destructors)!
        util.hard_exit(code)
    elif code:
        sys.exit(code)

    # HACK: keep res alive so that mypyc won't free it before the hard_exit
    list([res])  # noqa: C410


def main(args: list[str] | None = None) -> None:
    mypy.util.check_python_version("stubgen")
    # Make sure that the current directory is in sys.path so that
    # stubgen can be run on packages in the current directory.
    if not ("" in sys.path or "." in sys.path):
        sys.path.insert(0, "")

    options = parse_options(sys.argv[1:] if args is None else args)
    generate_stubs(options)


def main() -> int:
    mypy.util.check_python_version("stubtest")
    return test_stubs(parse_options(sys.argv[1:]))


def main() -> None:
    build_dir = "build"  # can this be overridden??
    try:
        os.mkdir(build_dir)
    except FileExistsError:
        pass

    opt_level = os.getenv("MYPYC_OPT_LEVEL", "3")
    debug_level = os.getenv("MYPYC_DEBUG_LEVEL", "1")
    strict_dunder_typing = bool(int(os.getenv("MYPYC_STRICT_DUNDER_TYPING", "0")))
    # If enabled, compiled code writes a sampled log of executed ops (or events) to
    # mypyc_trace.txt.
    log_trace = bool(int(os.getenv("MYPYC_LOG_TRACE", "0")))

    setup_file = os.path.join(build_dir, "setup.py")
    with open(setup_file, "w") as f:
        f.write(
            setup_format.format(
                sys.argv[1:], opt_level, debug_level, strict_dunder_typing, log_trace
            )
        )

    # We don't use run_setup (like we do in the test suite) because it throws
    # away the error code from distutils, and we don't care about the slight
    # performance loss here.
    env = os.environ.copy()
    base_path = os.path.join(os.path.dirname(__file__), "..")
    env["PYTHONPATH"] = base_path + os.pathsep + env.get("PYTHONPATH", "")
    cmd = subprocess.run([sys.executable, setup_file, "build_ext", "--inplace"], env=env)
    sys.exit(cmd.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print the version and exit.",
    )
    parser.add_argument(
        "--cflags",
        action="store_true",
        help="Compile flag needed when using the NumPy headers.",
    )
    parser.add_argument(
        "--pkgconfigdir",
        action="store_true",
        help=("Print the pkgconfig directory in which `numpy.pc` is stored "
              "(useful for setting $PKG_CONFIG_PATH)."),
    )
    args = parser.parse_args()
    if not sys.argv[1:]:
        parser.print_help()
    if args.cflags:
        print("-I" + get_include())
    if args.pkgconfigdir:
        _path = Path(get_include()) / '..' / 'lib' / 'pkgconfig'
        print(_path.resolve())


def main(args: list[str] | None = None) -> int:
    """This is an internal API only meant for use by pip's own console scripts.

    For additional details, see https://github.com/pypa/pip/issues/7498.
    """
    from pip._internal.utils.entrypoints import _wrapper

    return _wrapper(args)


def main() -> None:
    """Run the main entry point."""
    app_name = "MyApp"
    app_author = "MyCompany"

    print(f"-- platformdirs {__version__} --")  # noqa: T201

    print("-- app dirs (with optional 'version')")  # noqa: T201
    dirs = PlatformDirs(app_name, app_author, version="1.0")
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (without optional 'version')")  # noqa: T201
    dirs = PlatformDirs(app_name, app_author)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (without optional 'appauthor')")  # noqa: T201
    dirs = PlatformDirs(app_name)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (with disabled 'appauthor')")  # noqa: T201
    dirs = PlatformDirs(app_name, appauthor=False)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201


def main() -> None:
    make_parser = functools.partial(argparse.ArgumentParser, allow_abbrev=False)
    if sys.version_info >= (3, 14):
        make_parser = functools.partial(make_parser, color=True, suggest_on_error=True)
    parser = make_parser()
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print the version and exit.",
    )
    parser.add_argument(
        "--includes",
        action="store_true",
        help="Include flags for both pybind11 and Python headers.",
    )
    parser.add_argument(
        "--cmakedir",
        action="store_true",
        help="Print the CMake module directory, ideal for setting -Dpybind11_ROOT in CMake.",
    )
    parser.add_argument(
        "--pkgconfigdir",
        action="store_true",
        help="Print the pkgconfig directory, ideal for setting $PKG_CONFIG_PATH.",
    )
    parser.add_argument(
        "--extension-suffix",
        action="store_true",
        help="Print the extension for a Python module",
    )
    args = parser.parse_args()
    if not sys.argv[1:]:
        parser.print_help()
    if args.includes:
        print_includes()
    if args.cmakedir:
        print(quote(get_cmake_dir()))
    if args.pkgconfigdir:
        print(quote(get_pkgconfig_dir()))
    if args.extension_suffix:
        print(sysconfig.get_config_var("EXT_SUFFIX"))


def main(prog=None, args=None):
    """Entry point for the script "pyflakes"."""
    import argparse

    # Handle "Keyboard Interrupt" and "Broken pipe" gracefully
    _exitOnSignal('SIGINT', '... stopped')
    _exitOnSignal('SIGPIPE', 1)

    parser = argparse.ArgumentParser(prog=prog,
                                     description='Check Python source files for errors')
    parser.add_argument('-V', '--version', action='version', version=_get_version())
    parser.add_argument('path', nargs='*',
                        help='Path(s) of Python file(s) to check. STDIN if not given.')
    args = parser.parse_args(args=args).path
    reporter = modReporter._makeDefaultReporter()
    if args:
        warnings = checkRecursive(args, reporter)
    else:
        warnings = check(sys.stdin.read(), '<stdin>', reporter)
    raise SystemExit(warnings > 0)


def main(args=sys.argv):
    """
    Main command line entry point.
    """
    desc = "Highlight an input file and write the result to an output file."
    parser = argparse.ArgumentParser(description=desc, add_help=False,
                                     formatter_class=HelpFormatter)

    operation = parser.add_argument_group('Main operation')
    lexersel = operation.add_mutually_exclusive_group()
    lexersel.add_argument(
        '-l', metavar='LEXER',
        help='Specify the lexer to use.  (Query names with -L.)  If not '
        'given and -g is not present, the lexer is guessed from the filename.')
    lexersel.add_argument(
        '-g', action='store_true',
        help='Guess the lexer from the file contents, or pass through '
        'as plain text if nothing can be guessed.')
    operation.add_argument(
        '-F', metavar='FILTER[:options]', action='append',
        help='Add a filter to the token stream.  (Query names with -L.) '
        'Filter options are given after a colon if necessary.')
    operation.add_argument(
        '-f', metavar='FORMATTER',
        help='Specify the formatter to use.  (Query names with -L.) '
        'If not given, the formatter is guessed from the output filename, '
        'and defaults to the terminal formatter if the output is to the '
        'terminal or an unknown file extension.')
    operation.add_argument(
        '-O', metavar='OPTION=value[,OPTION=value,...]', action='append',
        help='Give options to the lexer and formatter as a comma-separated '
        'list of key-value pairs. '
        'Example: `-O bg=light,python=cool`.')
    operation.add_argument(
        '-P', metavar='OPTION=value', action='append',
        help='Give a single option to the lexer and formatter - with this '
        'you can pass options whose value contains commas and equal signs. '
        'Example: `-P "heading=Pygments, the Python highlighter"`.')
    operation.add_argument(
        '-o', metavar='OUTPUTFILE',
        help='Where to write the output.  Defaults to standard output.')

    operation.add_argument(
        'INPUTFILE', nargs='?',
        help='Where to read the input.  Defaults to standard input.')

    flags = parser.add_argument_group('Operation flags')
    flags.add_argument(
        '-v', action='store_true',
        help='Print a detailed traceback on unhandled exceptions, which '
        'is useful for debugging and bug reports.')
    flags.add_argument(
        '-s', action='store_true',
        help='Process lines one at a time until EOF, rather than waiting to '
        'process the entire file.  This only works for stdin, only for lexers '
        'with no line-spanning constructs, and is intended for streaming '
        'input such as you get from `tail -f`. '
        'Example usage: `tail -f sql.log | pygmentize -s -l sql`.')
    flags.add_argument(
        '-x', action='store_true',
        help='Allow custom lexers and formatters to be loaded from a .py file '
        'relative to the current working directory. For example, '
        '`-l ./customlexer.py -x`. By default, this option expects a file '
        'with a class named CustomLexer or CustomFormatter; you can also '
        'specify your own class name with a colon (`-l ./lexer.py:MyLexer`). '
        'Users should be very careful not to use this option with untrusted '
        'files, because it will import and run them.')
    flags.add_argument('--json', help='Output as JSON. This can '
        'be only used in conjunction with -L.',
        default=False,
        action='store_true')

    special_modes_group = parser.add_argument_group(
        'Special modes - do not do any highlighting')
    special_modes = special_modes_group.add_mutually_exclusive_group()
    special_modes.add_argument(
        '-S', metavar='STYLE -f formatter',
        help='Print style definitions for STYLE for a formatter '
        'given with -f. The argument given by -a is formatter '
        'dependent.')
    special_modes.add_argument(
        '-L', nargs='*', metavar='WHAT',
        help='List lexers, formatters, styles or filters -- '
        'give additional arguments for the thing(s) you want to list '
        '(e.g. "styles"), or omit them to list everything.')
    special_modes.add_argument(
        '-N', metavar='FILENAME',
        help='Guess and print out a lexer name based solely on the given '
        'filename. Does not take input or highlight anything. If no specific '
        'lexer can be determined, "text" is printed.')
    special_modes.add_argument(
        '-C', action='store_true',
        help='Like -N, but print out a lexer name based solely on '
        'a given content from standard input.')
    special_modes.add_argument(
        '-H', action='store', nargs=2, metavar=('NAME', 'TYPE'),
        help='Print detailed help for the object <name> of type <type>, '
        'where <type> is one of "lexer", "formatter" or "filter".')
    special_modes.add_argument(
        '-V', action='store_true',
        help='Print the package version.')
    special_modes.add_argument(
        '-h', '--help', action='store_true',
        help='Print this help.')
    special_modes_group.add_argument(
        '-a', metavar='ARG',
        help='Formatter-specific additional argument for the -S (print '
        'style sheet) mode.')

    argns = parser.parse_args(args[1:])

    try:
        return main_inner(parser, argns)
    except BrokenPipeError:
        # someone closed our stdout, e.g. by quitting a pager.
        return 0
    except Exception:
        if argns.v:
            print(file=sys.stderr)
            print('*' * 65, file=sys.stderr)
            print('An unhandled exception occurred while highlighting.',
                  file=sys.stderr)
            print('Please report the whole traceback to the issue tracker at',
                  file=sys.stderr)
            print('<https://github.com/pygments/pygments/issues>.',
                  file=sys.stderr)
            print('*' * 65, file=sys.stderr)
            print(file=sys.stderr)
            raise
        import traceback
        info = traceback.format_exception(*sys.exc_info())
        msg = info[-1].strip()
        if len(info) >= 3:
            # extract relevant file and position info
            msg += '\n   (f{})'.format(info[-2].split('\n')[0].strip()[1:])
        print(file=sys.stderr)
        print('*** Error while highlighting:', file=sys.stderr)
        print(msg, file=sys.stderr)
        print('*** If this is a bug you want to report, please rerun with -v.',
              file=sys.stderr)
        return 1


def main():
    '''The entry point for Setuptools.'''
    import sys
    from radon.cli import program, log_error

    if not sys.argv[1:]:
        sys.argv.append('-h')
    try:
        program()
    except Exception as e:
        log_error(e)


def main():
    """Pretty-print the bug information as JSON."""
    print(json.dumps(info(), sort_keys=True, indent=2))


def main():
    if len(sys.argv) == 1:
        infile = sys.stdin
        outfile = sys.stdout
    elif len(sys.argv) == 2:
        infile = open(sys.argv[1], 'r')
        outfile = sys.stdout
    elif len(sys.argv) == 3:
        infile = open(sys.argv[1], 'r')
        outfile = open(sys.argv[2], 'w')
    else:
        raise SystemExit(sys.argv[0] + " [infile [outfile]]")
    with infile:
        try:
            obj = json.load(infile,
                            object_pairs_hook=json.OrderedDict,
                            use_decimal=True)
        except ValueError:
            raise SystemExit(sys.exc_info()[1])
    with outfile:
        json.dump(obj, outfile, sort_keys=True, indent='    ', use_decimal=True)
        outfile.write('\n')


def main(argv: list[str] | None = None):  # pragma: no cover
    """ Run this program """
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    params = slugify_params(args)
    try:
        print(slugify(**params))
    except KeyboardInterrupt:
        sys.exit(-1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ATen source files")
    parser.add_argument(
        "-s",
        "--source-path",
        help="path to source directory for ATen",
        default="aten/src/ATen",
    )
    parser.add_argument(
        "-o",
        "--output-dependencies",
        help="output a list of dependencies into the given file and exit",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="run without writing any files (still updates outputs)",
    )
    parser.add_argument(
        "--per-operator-headers",
        action="store_true",
        help="generate separate headers per operator in ATen/ops",
    )
    parser.add_argument(
        "-d",
        "--install-dir",
        "--install_dir",
        help="output directory",
        default="build/aten/src/ATen",
    )
    parser.add_argument(
        "--aoti-install-dir",
        "--aoti_install_dir",
        help="output directory for AOTInductor shim",
        default="torch/csrc/inductor/aoti_torch/generated",
    )
    parser.add_argument(
        "--headeronly-install-dir",
        "--headeronly_install_dir",
        help="output directory for header-only generated files (e.g. enum_tag.h). "
        "Defaults to `<install-dir>/core` when --install-dir is set, otherwise "
        "`build/torch/headeronly/core`.",
        default=None,
    )
    parser.add_argument(
        "--rocm",
        action="store_true",
        help="reinterpret CUDA as ROCm/HIP and adjust filepaths accordingly",
    )
    parser.add_argument(
        "--mps",
        action="store_true",
        help="Generate MPS registration code when set",
    )
    parser.add_argument(
        "--xpu",
        action="store_true",
        help="Generate XPU registration code when set",
    )
    parser.add_argument(
        "--mtia",
        action="store_true",
        help="Generate MTIA registration code when set",
    )

    # TODO: --op-registration-whitelist will be removed when all call-sites
    # for gen.py are moved over to using the operator YAML file for mobile
    # custom build.
    parser.add_argument(
        "--op-registration-whitelist",
        "--op_registration_whitelist",
        nargs="*",
        help="filter op registrations by the whitelist (if set); "
        "each item is `namespace`::`operator name` without overload name; "
        "e.g.: aten::empty aten::conv2d ...",
    )
    parser.add_argument(
        "--op-selection-yaml-path",
        "--op_selection_yaml_path",
        help="Provide a path to the operator selection (for custom build) YAML "
        "that contains the information about the set of selected operators "
        "and their categories (training, ...). Each operator is either a "
        "full operator name with overload or just a bare operator name. "
        "The operator names also contain the namespace prefix (e.g. aten::)",
    )
    parser.add_argument(
        "--backend-whitelist",
        "--backend_whitelist",
        nargs="*",
        help="filter dispatch backend by the whitelist (if set), "
        "e.g.: CPU CUDA QuantizedCPU ...",
    )
    parser.add_argument(
        "--static-dispatch-backend",
        "--static_dispatch_backend",
        nargs="*",
        help="generate static dispatch code for the specific backend (if set)",
    )
    parser.add_argument(
        "--skip-dispatcher-op-registration",
        "--skip_dispatcher_op_registration",
        action="store_true",
        help="Avoid registering operators into the dispatcher.",
    )
    parser.add_argument(
        "--force-schema-registration",
        "--force_schema_registration",
        action="store_true",
        help="force it to generate schema-only registrations for all ops, including"
        "those that are not listed on --op-registration-whitelist",
    )
    parser.add_argument(
        "--generate",
        type=str,
        nargs="*",
        choices=["headers", "sources", "declarations_yaml"],
        default=["headers", "sources", "declarations_yaml"],
        help="Generate only a subset of files",
    )
    parser.add_argument(
        "--update-aoti-c-shim",
        action="store_true",
        help="Update AOTInductor C shim after adding an entry to inductor_fallback_ops in torchgen/aoti/fallback_ops.py. "
        "WARNING: Do not use this unless you are sure what you are doing!!!",
    )
    parser.add_argument(
        "--extend-aoti-c-shim",
        action="store_true",
        help="This Flag indicates the generation of c shims for out-of-tree ATen ops,"
        "which is an extension to the In-tree ATen op c shims. This flag needs to be combined with"
        "---source-path=<out-of-tree native_functions.yaml>"
        "--aoti-install-dir=<in-tree aoti_install_dir>/extend"
        "   default is torch/csrc/inductor/aoti_torch/generated/extend"
        "WARNING: Do not use this unless you are sure what you are doing!!!",
    )

    options = parser.parse_args()

    selector = get_custom_build_selector(
        options.op_registration_whitelist,
        options.op_selection_yaml_path,
    )

    native_yaml_path = os.path.join(options.source_path, "native/native_functions.yaml")
    tags_yaml_path = os.path.join(options.source_path, "native/tags.yaml")

    from torchgen.model import dispatch_keys

    # Only a limited set of dispatch keys get CPUFunctions.h headers generated
    # for them; this is the set
    functions_keys = {
        DispatchKey.CPU,
        DispatchKey.CUDA,
        DispatchKey.CompositeImplicitAutograd,
        DispatchKey.CompositeImplicitAutogradNestedTensor,
        DispatchKey.CompositeExplicitAutograd,
        DispatchKey.CompositeExplicitAutogradNonFunctional,
        DispatchKey.Meta,
        DispatchKey.MTIA,
    }

    aoti_backends = {
        DispatchKey.CPU,
        DispatchKey.CUDA,
        # None will generate the aten shim based on aten_shimified_ops
        # which does not bypass the dispatcher
        None,
    }

    # TODO: stop generating CUDA kernels for non-CUDA builds
    ignore_keys = set()

    MPS_KEYS = {DispatchKey.MPS, DispatchKey.SparseMPS, DispatchKey.SparseCsrMPS}
    if options.mps or options.update_aoti_c_shim:
        functions_keys.update(MPS_KEYS)
        aoti_backends.add(DispatchKey.MPS)
    else:
        ignore_keys.update(MPS_KEYS)
        dispatch_keys[:] = [k for k in dispatch_keys if k not in MPS_KEYS]

    if options.xpu or options.update_aoti_c_shim:
        functions_keys.add(DispatchKey.XPU)
        aoti_backends.add(DispatchKey.XPU)
    else:
        ignore_keys.add(DispatchKey.XPU)

        if DispatchKey.XPU in dispatch_keys:
            del dispatch_keys[dispatch_keys.index(DispatchKey.XPU)]

    if not options.mtia:
        ignore_keys.add(DispatchKey.MTIA)

        if DispatchKey.MTIA in dispatch_keys:
            del dispatch_keys[dispatch_keys.index(DispatchKey.MTIA)]

    if options.backend_whitelist:
        dispatch_keys = [
            k
            for k in dispatch_keys
            if is_generic_dispatch_key(k) or str(k) in options.backend_whitelist
        ]

    parsed_yaml = parse_native_yaml(native_yaml_path, tags_yaml_path, ignore_keys)
    valid_tags = _GLOBAL_PARSE_TAGS_YAML_CACHE[tags_yaml_path]
    native_functions, backend_indices = (
        parsed_yaml.native_functions,
        parsed_yaml.backend_indices,
    )

    grouped_native_functions = get_grouped_native_functions(native_functions)

    structured_native_functions = [
        g for g in grouped_native_functions if isinstance(g, NativeFunctionsGroup)
    ]
    native_functions_with_view_groups = get_grouped_by_view_native_functions(
        native_functions
    )
    view_groups = [
        g
        for g in native_functions_with_view_groups
        if isinstance(g, NativeFunctionsViewGroup)
    ]

    # NB: It is mandatory to NOT use os.path.join here, as the install directory
    # will eventually be ingested by cmake, which does not respect Windows style
    # path slashes.  If you switch this to use os.path.join, you'll get an error
    # like:
    #
    #   Syntax error in cmake code when parsing string
    #
    #     C:/Jenkins/workspace/pytorch-builds/pytorch-win-ws2016-cuda9-cudnn7-py3-build/build/aten/src/ATen\core/TensorMethods.h
    #
    #   Invalid character escape '\c'.
    core_install_dir = f"{options.install_dir}/core"
    Path(core_install_dir).mkdir(parents=True, exist_ok=True)
    ops_install_dir = f"{options.install_dir}/ops"
    Path(ops_install_dir).mkdir(parents=True, exist_ok=True)

    aoti_install_dir = f"{options.aoti_install_dir}"
    Path(aoti_install_dir).mkdir(parents=True, exist_ok=True)

    if options.headeronly_install_dir is not None:
        headeronly_install_dir = options.headeronly_install_dir
    elif options.install_dir is not None:
        headeronly_install_dir = f"{options.install_dir}/core"
    else:
        headeronly_install_dir = "build/torch/headeronly/core"
    Path(headeronly_install_dir).mkdir(parents=True, exist_ok=True)

    core_fm = make_file_manager(options=options, install_dir=core_install_dir)
    cpu_fm = make_file_manager(options=options)
    cpu_vec_fm = make_file_manager(options=options)
    cuda_fm = make_file_manager(options=options)
    ops_fm = make_file_manager(options=options, install_dir=ops_install_dir)
    aoti_fm = make_file_manager(options=options, install_dir=aoti_install_dir)
    headeronly_fm = make_file_manager(
        options=options, install_dir=headeronly_install_dir
    )
    device_fms = {"cuda": cuda_fm}
    if options.xpu:
        device_fms["xpu"] = make_file_manager(options=options)

    static_dispatch_idx: list[BackendIndex] = []
    if options.static_dispatch_backend:
        static_dispatch_idx = [
            backend_indices[DispatchKey.parse(key)]
            for key in options.static_dispatch_backend
        ]
        for key in options.static_dispatch_backend:
            dp_key = DispatchKey.parse(key)
            if dp_key not in functions_keys:
                functions_keys.add(dp_key)

    if "sources" in options.generate:
        gen_source_files(
            native_functions=native_functions,
            grouped_native_functions=grouped_native_functions,
            structured_native_functions=structured_native_functions,
            view_groups=view_groups,
            selector=selector,
            static_dispatch_idx=static_dispatch_idx,
            backend_indices=backend_indices,
            aoti_fm=aoti_fm,
            core_fm=core_fm,
            cpu_vec_fm=cpu_vec_fm,
            cpu_fm=cpu_fm,
            device_fms=device_fms,
            dispatch_keys=dispatch_keys,
            functions_keys=functions_keys,
            rocm=options.rocm,
            force_schema_registration=options.force_schema_registration,
            per_operator_headers=options.per_operator_headers,
            skip_dispatcher_op_registration=options.skip_dispatcher_op_registration,
            update_aoti_c_shim=options.update_aoti_c_shim,
            aoti_backends=aoti_backends,
            extend_aoti_c_shim=options.extend_aoti_c_shim,
        )

    if "headers" in options.generate:
        gen_headers(
            native_functions=native_functions,
            valid_tags=valid_tags,
            grouped_native_functions=grouped_native_functions,
            structured_native_functions=structured_native_functions,
            static_dispatch_idx=static_dispatch_idx,
            selector=selector,
            backend_indices=backend_indices,
            headeronly_fm=headeronly_fm,
            core_fm=core_fm,
            cpu_fm=cpu_fm,
            device_fms=device_fms,
            ops_fm=ops_fm,
            dispatch_keys=dispatch_keys,
            functions_keys=functions_keys,
            rocm=options.rocm,
            per_operator_headers=options.per_operator_headers,
        )

    if "declarations_yaml" in options.generate:
        gen_declarations_yaml(native_functions=native_functions, cpu_fm=cpu_fm)

    if options.output_dependencies:
        depfile_path = Path(options.output_dependencies).resolve()
        depfile_name = depfile_path.name
        depfile_stem = depfile_path.stem

        for fm, prefix in [
            (cpu_fm, ""),
            (cpu_vec_fm, "cpu_vec_"),
            (core_fm, "core_"),
            (ops_fm, "ops_"),
        ] + [(device_fm, f"{device}_") for device, device_fm in device_fms.items()]:
            varname = prefix + depfile_stem
            path = depfile_path.parent / (prefix + depfile_name)
            fm.write_outputs(varname, str(path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate backend stub files")
    parser.add_argument(
        "-s",
        "--source-yaml",
        "--source_yaml",
        help="path to source yaml file containing operator external definitions",
    )
    parser.add_argument("-o", "--output-dir", "--output_dir", help="output directory")
    parser.add_argument(
        "--dry-run", "--dry_run", type=bool, default=False, help="output directory"
    )
    parser.add_argument(
        "--impl-path",
        "--impl_path",
        type=str,
        default=None,
        help="path to the source C++ file containing kernel definitions",
    )
    options = parser.parse_args()

    run(options.source_yaml, options.output_dir, options.dry_run, options.impl_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Lazy Tensor backend files")
    parser.add_argument(
        "-s",
        "--source-yaml",
        "--source_yaml",
        help="path to source yaml file containing operator external definitions",
    )
    parser.add_argument("-o", "--output-dir", "--output_dir", help="output directory")
    parser.add_argument(
        "--dry-run", "--dry_run", type=bool, default=False, help="output directory"
    )
    parser.add_argument(
        "--impl-path",
        "--impl_path",
        type=str,
        default=None,
        help="path to the source C++ file containing kernel definitions",
    )
    parser.add_argument(
        "--gen-ts-lowerings",
        "--gen_ts_lowerings",
        action="store_true",
        help="Generate TorchScript lowerings in addition to Lazy IR and NativeFunctions",
    )
    parser.add_argument(
        "--node-base",
        "--node_base",
        type=str,
        default=default_args.node_base,
        help="Name of backend specific custom Lazy IR Node base class",
    )
    parser.add_argument(
        "--node-base-hdr",
        "--node_base_hdr",
        type=str,
        default=default_args.node_base_hdr,
        help="Path to header file defining custom Lazy IR Node base class",
    )
    parser.add_argument(
        "--shape-inference-hdr",
        "--shape_inference_hdr",
        type=str,
        default=default_args.shape_inference_hdr,
        help="Path to header file defining custom Lazy shape inference functions",
    )
    parser.add_argument(
        "--tensor-class",
        "--tensor_class",
        type=str,
        default=default_args.tensor_class,
        help="Name of backend specific custom Lazy Tensor class",
    )
    parser.add_argument(
        "--tensor-class-hdr",
        "--tensor_class_hdr",
        type=str,
        default=default_args.tensor_class_hdr,
        help="Path to header file defining custom Lazy Tensor class",
    )
    parser.add_argument(
        "--backend-name",
        "--backend_name",
        type=str,
        default=default_args.backend_name,
        help="Name of the backend to generate",
    )
    options = parser.parse_args()

    # Assumes that this file lives at PYTORCH_ROOT/torchgen/gen_backend_stubs.py
    torch_root = Path(__file__).absolute().parents[2]
    aten_path = str(torch_root / "aten" / "src" / "ATen")
    lazy_ir_generator: type[GenLazyIR] = default_args.lazy_ir_generator
    if options.gen_ts_lowerings:
        lazy_ir_generator = GenTSLazyIR
    native_func_definition_generator: type[GenLazyNativeFuncDefinition] = (
        default_args.native_func_definition_generator
    )

    run_gen_lazy_tensor(
        aten_path,
        options.source_yaml,
        options.output_dir,
        options.dry_run,
        options.impl_path,
        options.node_base,
        options.node_base_hdr,
        options.tensor_class,
        options.tensor_class_hdr,
        options.shape_inference_hdr,
        lazy_ir_generator,
        native_func_definition_generator,
        options.backend_name,
    )


def main(fp=sys.stderr, argv=None):
    """
    Parameters (internal use only)
    ---------
    fp  : file-like object for tqdm
    argv  : list (default: sys.argv[1:])
    """
    if argv is None:
        argv = sys.argv[1:]
    try:
        log_idx = argv.index('--log')
    except ValueError:
        for i in argv:
            if i.startswith('--log='):
                logLevel = i[len('--log='):]
                break
        else:
            logLevel = 'INFO'
    else:
        # argv.pop(log_idx)
        # logLevel = argv.pop(log_idx)
        logLevel = argv[log_idx + 1]
    logging.basicConfig(level=getattr(logging, logLevel),
                        format="%(levelname)s:%(module)s:%(lineno)d:%(message)s")

    # py<3.13 doesn't dedent docstrings
    d = (tqdm.__doc__ if sys.version_info < (3, 13)
         else indent(tqdm.__doc__, "    ")) + CLI_EXTRA_DOC

    opt_types = dict(RE_OPTS.findall(d))
    # opt_types['delim'] = 'chr'

    for o in UNSUPPORTED_OPTS:
        opt_types.pop(o)

    log.debug(sorted(opt_types.items()))

    # d = RE_OPTS.sub(r'  --\1=<\1>  : \2', d)
    split = RE_OPTS.split(d)
    opt_types_desc = zip(split[1::3], split[2::3], split[3::3])
    d = ''.join(('\n  --{0}  : {2}{3}' if otd[1] == 'bool' else
                 '\n  --{0}=<{1}>  : {2}{3}').format(
                     otd[0].replace('_', '-'), otd[0], *otd[1:])
                for otd in opt_types_desc if otd[0] not in UNSUPPORTED_OPTS)

    help_short = "Usage:\n  tqdm [--help | options]\n"
    d = help_short + """
Options:
  -h, --help     Print this help and exit.
  -v, --version  Print version and exit.
""" + d.strip('\n') + '\n'

    # opts = docopt(d, version=__version__)
    if any(v in argv for v in ('-v', '--version')):
        sys.stdout.write(__version__ + '\n')
        sys.exit(0)
    elif any(v in argv for v in ('-h', '--help')):
        sys.stdout.write(d + '\n')
        sys.exit(0)
    elif argv and argv[0][:2] != '--':
        sys.stderr.write(f"Error:Unknown argument:{argv[0]}\n{help_short}")

    argv = RE_SHLEX.split(' '.join(["tqdm"] + argv))
    opts = dict(zip(argv[1::3], argv[3::3]))

    log.debug(opts)
    opts.pop('log', True)

    tqdm_args = {'file': fp}
    try:
        for (o, v) in opts.items():
            o = o.replace('-', '_')
            try:
                tqdm_args[o] = cast(v, opt_types[o])
            except KeyError as e:
                raise TqdmKeyError(str(e))
        log.debug('args:' + str(tqdm_args))

        delim_per_char = tqdm_args.pop('bytes', False)
        update = tqdm_args.pop('update', False)
        update_to = tqdm_args.pop('update_to', False)
        if sum((delim_per_char, update, update_to)) > 1:
            raise TqdmKeyError("Can only have one of --bytes --update --update_to")
    except Exception:
        fp.write("\nError:\n" + help_short)
        stdin, stdout_write = sys.stdin, sys.stdout.write
        for i in stdin:
            stdout_write(i)
        raise
    else:
        buf_size = tqdm_args.pop('buf_size', 256)
        delim = tqdm_args.pop('delim', b'\\n')
        tee = tqdm_args.pop('tee', False)
        manpath = tqdm_args.pop('manpath', None)
        comppath = tqdm_args.pop('comppath', None)
        if tqdm_args.pop('null', False):
            class stdout:
                @staticmethod
                def write(_):
                    pass
        else:
            stdout = sys.stdout
            stdout = getattr(stdout, 'buffer', stdout)
        stdin = getattr(sys.stdin, 'buffer', sys.stdin)
        if manpath or comppath:
            try:  # py<3.9
                import importlib_resources as resources
            except ImportError:
                from importlib import resources
            from pathlib import Path

            def cp(name, dst):
                """copy resource `name` to `dst`"""
                fi = resources.files('tqdm') / name
                dst.write_bytes(fi.read_bytes())
                log.info("written:%s", dst)
            if manpath is not None:
                cp('tqdm.1', Path(manpath) / 'tqdm.1')
            if comppath is not None:
                cp('completion.sh', Path(comppath) / 'tqdm_completion.sh')
            sys.exit(0)
        if tee:
            stdout_write = stdout.write
            fp_write = getattr(fp, 'buffer', fp).write

            class stdout:  # pylint: disable=function-redefined
                @staticmethod
                def write(x):
                    with tqdm.external_write_mode(file=fp):
                        fp_write(x)
                    stdout_write(x)
        if delim_per_char:
            tqdm_args.setdefault('unit', 'B')
            tqdm_args.setdefault('unit_scale', True)
            tqdm_args.setdefault('unit_divisor', 1024)
            log.debug(tqdm_args)
            with tqdm(**tqdm_args) as t:
                posix_pipe(stdin, stdout, '', buf_size, t.update)
        elif delim == b'\\n':
            log.debug(tqdm_args)
            write = stdout.write
            if update or update_to:
                with tqdm(**tqdm_args) as t:
                    if update:
                        def callback(i):
                            t.update(literal_eval(i.decode()))
                    else:  # update_to
                        def callback(i):
                            t.update(literal_eval(i.decode()) - t.n)
                    for i in stdin:
                        write(i)
                        callback(i)
            else:
                for i in tqdm(stdin, **tqdm_args):
                    write(i)
        else:
            log.debug(tqdm_args)
            with tqdm(**tqdm_args) as t:
                callback_len = False
                if update:
                    def callback(i):
                        t.update(literal_eval(i.decode()))
                elif update_to:
                    def callback(i):
                        t.update(literal_eval(i.decode()) - t.n)
                else:
                    callback = t.update
                    callback_len = True
                posix_pipe(stdin, stdout, delim, buf_size, callback, callback_len)


def main() -> Any:
    return app()


def main(
    args: list[str] | os.PathLike[str] | None = None,
    plugins: Sequence[str | _PluggyPlugin] | None = None,
) -> int | ExitCode:
    """Perform an in-process test run.

    :param args:
        List of command line arguments. If `None` or not given, defaults to reading
        arguments directly from the process command line (:data:`sys.argv`).
    :param plugins: List of plugin objects to be auto-registered during initialization.

    :returns: An exit code.
    """
    return _main(args=args, plugins=plugins, prog="pytest.main()")


def main():
    check_cli_update("transformers")
    app()


def main():
    parser = argparse.ArgumentParser(description="Summarize pytest JSON report failures")
    parser.add_argument(
        "--report", default="report.json", help="Path to pytest JSON report file (default: report.json)"
    )
    args = parser.parse_args()

    try:
        summary = summarize(args.report)
    except FileNotFoundError as e:
        print(str(e))
        return

    outcomes = summary["outcomes"]
    print("=== Overall ===")
    total = sum(outcomes.values())
    print(f"Total tests: {total}")
    for k in sorted(outcomes):
        print(f"{k:>10}: {outcomes[k]}")

    def _print_counter(title, counter: Counter, label=""):
        print(f"\n=== {title} ===")
        if not counter:
            print("None")
            return
        for key, cnt in sorted(counter.items(), key=lambda x: (x[1], x[0])):
            if label:
                print(f"{cnt:4d}  {label}{key}")
            else:
                print(f"{cnt:4d}  {key}")

    _print_counter("Failures per test class", summary["failures_per_class"], label="class ")
    _print_counter("Failures per test_modeling_xxx", summary["failures_per_modeling_key"], label="model ")
    _print_counter("Failures per test file", summary["failures_per_file"])
    _print_counter("Failures per test name (base)", summary["failures_per_testname"])


def main():
    parser = argparse.ArgumentParser()
    parser = add_checkpointing_args(parser)
    parser = add_megatron_checkpoint_args(parser)
    parser = add_transformers_checkpoint_args(parser)
    args = parser.parse_args()
    if args.convert_checkpoint_from_megatron_to_transformers:
        convert_checkpoint_from_megatron_to_transformers(args)
    else:
        convert_checkpoint_from_transformers_to_megatron(args)


def main() -> None:
    upgrader_list = generate_upgraders_bytecode()
    sorted_upgrader_list = sort_upgrader(upgrader_list)
    for up in sorted_upgrader_list:
        print("after sort upgrader : ", next(iter(up)))

    pytorch_dir = Path(__file__).resolve().parents[2]
    upgrader_path = pytorch_dir / "torch" / "csrc" / "jit" / "mobile"
    write_cpp(str(upgrader_path), sorted_upgrader_list)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ATen source files")
    parser.add_argument(
        "-s",
        "--source-path",
        help="path to source directory for ATen",
        default="caffe2/aten/src/ATen",
    )
    parser.add_argument(
        "-p",
        "--generated-ops-cpp-path",
        help="path to directory to generate op dispatcher .cpp file",
        default="caffe2/torch/csrc/jit/runtime/static/generated_ops.cpp",
    )
    parser.add_argument(
        "-t",
        "--generated-ops-test-cpp-path",
        help="path to directory to generate op dispatcher .cpp file",
        default="caffe2/benchmarks/static_runtime/test_generated_ops.cc",
    )
    options = parser.parse_args()
    native_yaml_path = os.path.join(options.source_path, "native/native_functions.yaml")
    tags_yaml_path = os.path.join(options.source_path, "native/tags.yaml")
    parsed_yaml = gen.parse_native_yaml(native_yaml_path, tags_yaml_path)
    native_functions, backend_indices = (
        parsed_yaml.native_functions,
        parsed_yaml.backend_indices,
    )

    op_generator = generator.GenOpDispatcher()
    test_case_generator = generator.GenOpTestCase()

    native_functions_groups = [
        g
        for g in gen.get_grouped_native_functions(native_functions)
        if isinstance(g, NativeFunctionsGroup)
    ]

    supported_functions_groups = group_functions_by_op_name(native_functions_groups)

    out_variant_op_result = [
        op_generator.out_variant(groups, backend_indices[DispatchKey.CPU])
        for groups in supported_functions_groups
    ]
    out_variant_test_result = [
        test_case_generator.out_variant(groups) for groups in supported_functions_groups
    ]

    native_functions_view_groups = [
        g
        for g in gen.get_grouped_by_view_native_functions(native_functions)
        if isinstance(g, NativeFunctionsViewGroup)
    ]

    supported_functions_view_groups = group_functions_by_op_name(
        native_functions_view_groups
    )

    view_op_result = [
        op_generator.view(groups, backend_indices[DispatchKey.CPU])
        for groups in supported_functions_view_groups
    ]
    view_test_result = [
        test_case_generator.view(groups) for groups in supported_functions_view_groups
    ]

    op_result = out_variant_op_result + ["\n\n"] + view_op_result
    test_result = out_variant_test_result + ["\n\n"] + view_test_result

    write_cpp(op_result, options.generated_ops_cpp_path)
    write_test_cpp(test_result, options.generated_ops_test_cpp_path)

    print(
        f"\ntotal grouped native ops: {len(gen.get_grouped_native_functions(native_functions)):d}"
    )

    print(f"grouped native ops with out variant: {len(native_functions_groups):d}")
    supported_functions_num = sum(len(groups) for groups in supported_functions_groups)
    print(f"generated functions groups with out variant: {supported_functions_num:d}")

    print(f"\nview grouped native ops: {len(native_functions_view_groups):d}")
    supported_view_functions_num = sum(
        len(groups) for groups in supported_functions_view_groups
    )
    print(f"generated functions view groups: {supported_view_functions_num:d}")

    print(
        f"\noverall generated : {supported_functions_num + supported_view_functions_num:d}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate annotated_fn_args script")
    parser.add_argument(
        "native_functions", metavar="NATIVE", help="path to native_functions.yaml"
    )
    parser.add_argument("tags", metavar="TAGS", help="path to tags.yaml")
    parser.add_argument("out", metavar="OUT", help="path to output directory")
    parser.add_argument(
        "autograd", metavar="AUTOGRAD", help="path to template directory"
    )
    args = parser.parse_args()
    gen_annotated(args.native_functions, args.tags, args.out, args.autograd)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate autograd C++ files script")
    parser.add_argument(
        "native_functions", metavar="NATIVE", help="path to native_functions.yaml"
    )
    parser.add_argument("tags", metavar="NATIVE", help="path to tags.yaml")
    parser.add_argument("out", metavar="OUT", help="path to output directory")
    parser.add_argument(
        "autograd", metavar="AUTOGRAD", help="path to autograd directory"
    )
    args = parser.parse_args()
    gen_autograd(
        args.native_functions,
        args.tags,
        args.out,
        args.autograd,
        SelectiveBuilder.get_nop_selector(),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Annotate a profiler trace with CUDA graph kernel annotations."
    )
    parser.add_argument(
        "trace_file", type=Path, help="Input trace file (.json or .json.gz)"
    )
    parser.add_argument(
        "-a",
        "--annotations",
        type=Path,
        default=None,
        help="Kernel annotations pickle file. Auto-discovered if omitted.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file path. Defaults to <trace_file>.annotated.<ext>",
    )
    parser.add_argument(
        "--default-stream",
        type=int,
        default=7,
        help="Stream ID to assign to unannotated graphed events (default: 7).",
    )
    args = parser.parse_args()

    annotations_pkl = args.annotations
    if annotations_pkl is None:
        annotations_pkl = _find_annotations_pkl(args.trace_file)
        if annotations_pkl is None:
            print(
                f"Could not auto-discover annotations pickle for {args.trace_file}. "
                f"Use -a to specify it explicitly.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"Auto-discovered annotations: {annotations_pkl}")

    with open(annotations_pkl, "rb") as f:
        annotations = pickle.load(f)
    print(f"Loaded {len(annotations)} kernel annotations")

    trace = load_trace(args.trace_file)
    total_events = len(trace.get("traceEvents", []))
    print(f"Loaded trace with {total_events} events")

    count = annotate_trace(trace, annotations, default_stream=args.default_stream)
    print(f"Annotated {count} kernel events")

    overlap_moved = _move_overlapping_to_stream(
        trace, default_stream=args.default_stream
    )
    if overlap_moved:
        print(f"Moved {overlap_moved} overlapping events to stream 8")

    ts_fixed = _fix_overlapping_timestamps(trace)
    if ts_fixed:
        print(f"Fixed {ts_fixed} overlapping graphed event timestamps")

    output = args.output
    if output is None:
        name = args.trace_file.name
        if name.endswith(".json.gz"):
            output = args.trace_file.with_name(
                name.replace(".json.gz", ".annotated.json.gz")
            )
        elif name.endswith(".json"):
            output = args.trace_file.with_suffix(".annotated.json")
        else:
            output = args.trace_file.with_suffix(args.trace_file.suffix + ".annotated")

    save_trace(trace, output)
    print(f"Saved annotated trace to {output}")


def main(args=None):
    args = parse_args(args)
    launch(args)


def main(args=None):
    args = parse_args(args)
    run(args)


def main(op="scatter_mm", force=False, dtype=torch.float16, verbose=True):
    import itertools

    sizes_lst = [
        256,
        512,
        1024,
        2048,
        4096,
        8192,
        16384,
        32768,
        65536,
        131072,
        50432,
        65792,
    ]
    sizes3_lst = [3 * sz for sz in [64, 128] + sizes_lst if sz <= 2048]
    shapes_lst = [(sz, sz) for sz in sizes_lst[:-4] + sizes3_lst]
    shapes_lst.extend([(3072, 768), (768, 3072)])
    shapes_lst.extend([(5120, 1280), (1280, 5120)])
    if dtype is torch.int8:
        # triton does not support smaller blocks than 32
        blocksize_lst = [(32, 32), (64, 64), (128, 128), (256, 256)]
    else:
        blocksize_lst = [(16, 16), (32, 32), (64, 64), (128, 128)]
    sparsity_lst = [0.5, 0.7, 0.3][:1]
    for sparsity in sparsity_lst:
        print(f"{op, dtype, sparsity=}")
        try:
            for (M, K), N, (BM, BK) in itertools.product(
                shapes_lst, sizes_lst, blocksize_lst
            ):
                if not (BM <= M and BK <= K and M % BM == 0 and K % BK == 0):
                    continue
                if op == "scatter_mm":
                    optimize_scatter_mm(
                        M, K, N, BM, BK, force=force, sparsity=sparsity, dtype=dtype
                    )
                elif op in {"bsr_dense_addmm", "_int_bsr_dense_addmm"}:
                    if M == K and N == 50432:
                        continue
                    print(f"{M, K, N, (BM, BK)=}")
                    for alpha, beta in [(1, 1), (1, 0)]:
                        optimize_bsr_dense_addmm(
                            M,
                            K,
                            N,
                            BM,
                            BK,
                            beta=beta,
                            alpha=alpha,
                            force=force,
                            sparsity=sparsity,
                            dtype=dtype,
                            verbose=verbose,
                            opname=op,
                        )
                else:
                    raise NotImplementedError(op)
        except KeyboardInterrupt:
            break
        except Exception:
            dump()
            raise
    dump()

    if 0:
        # Check performance dependence on sparsity and apply
        # adjustments when differences are noticeable (more than 10%).
        #
        # When using NVIDIA A100 GPU, the performance dependence on
        # sparsity is insignificant (0 % ... 10 %) for majority of
        # shapes/blocksizes combinations. However, for a very few
        # specific size combinations, the effect of sparsity on
        # performance can be up to 20 %.
        for (M, K), N, (BM, BK) in itertools.product(
            shapes_lst, sizes_lst, blocksize_lst
        ):
            meta_lst: list = []
            key = (M, K, N, BM, BK)
            for sparsity1 in sparsity_lst:
                torch.manual_seed(0)
                bsr = create_blocked_tensor(
                    0, M, K, (BM, BK), sparsity1, dtype, device="cuda"
                ).to_sparse_bsr((BM, BK))
                dense = make_tensor(K, N, dtype=dtype, device="cuda")
                meta_lst = []
                for sparsity in sparsity_lst:
                    meta = get_meta(op, key, version=(0, dtype, sparsity), exact=True)
                    if meta is None:
                        continue

                    def bench(meta, bsr=bsr, dense=dense):
                        import triton

                        if op == "scatter_mm":
                            from torch.sparse._triton_ops import (
                                bsr_scatter_mm,
                                bsr_scatter_mm_indices_data,
                            )

                            indices_data = bsr_scatter_mm_indices_data(
                                bsr,
                                dense,
                                indices_format="bsr_strided_mm_compressed",
                                **meta,
                            )

                            def test_func():
                                return bsr_scatter_mm(
                                    bsr, dense, indices_data=indices_data
                                )

                        else:
                            raise NotImplementedError(op)

                        ms_min = triton.testing.do_bench(test_func, warmup=500, rep=100)

                        return ms_min

                    meta_lst.append(
                        (bench(meta), sparsity, tuple(meta[k] for k in sorted(meta)))
                    )
                if not meta_lst:
                    continue
                meta_lst = sorted(meta_lst)
                index = next(
                    i for i, item in enumerate(meta_lst) if item[1] == sparsity1
                )
                if meta_lst[0][2] == meta_lst[index][2]:
                    continue
                speeddiff = (1 - meta_lst[index][0] / meta_lst[0][0]) * 100
                if abs(speeddiff) < 10:
                    continue

                print(sparsity1, index, key, meta_lst, speeddiff)

                if index > 0:
                    device_name = torch.cuda.get_device_name()
                    meta = get_meta(
                        op, key, version=(0, dtype, meta_lst[0][1]), exact=True
                    )
                    update(
                        op,
                        device_name,
                        (0, dtype, sparsity1),
                        key,
                        tuple(meta[k] for k in sorted(meta)),
                    )
                    print("update")
                    dump()


def main() -> None:
    print("Collecting environment information...")
    output = get_pretty_env_info()
    print(output)

    if (
        TORCH_AVAILABLE
        and hasattr(torch, "utils")
        and hasattr(torch.utils, "_crash_handler")
    ):
        minidump_dir = torch.utils._crash_handler.DEFAULT_MINIDUMP_DIR
        if sys.platform == "linux" and os.path.exists(minidump_dir):
            dumps = [
                os.path.join(minidump_dir, dump) for dump in os.listdir(minidump_dir)
            ]
            latest = max(dumps, key=os.path.getctime)
            ctime = os.path.getctime(latest)
            creation_time = datetime.datetime.fromtimestamp(ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            msg = (
                "\n*** Detected a minidump at {} created on {}, ".format(
                    latest, creation_time
                )
                + "if this is related to your bug please include it when you file a report ***"
            )
            print(msg, file=sys.stderr)


def main(argv, output_stream=None) -> int | None:
    if len(argv) != 2:
        # Don't spam stderr if not using stdout.
        if output_stream is not None:
            raise Exception("Pass argv of length 2.")  # noqa: TRY002
        sys.stderr.write("usage: show_pickle PICKLE_FILE\n")
        sys.stderr.write("  PICKLE_FILE can be any of:\n")
        sys.stderr.write("    path to a pickle file\n")
        sys.stderr.write("    file.zip@member.pkl\n")
        sys.stderr.write("    file.zip@*/pattern.*\n")
        sys.stderr.write("      (shell glob pattern for members)\n")
        sys.stderr.write("      (only first match will be shown)\n")
        return 2

    fname = argv[1]
    handle: IO[bytes]
    if "@" not in fname:
        with open(fname, "rb") as handle:
            DumpUnpickler.dump(handle, output_stream)
    else:
        zfname, mname = fname.split("@", 1)
        with zipfile.ZipFile(zfname) as zf:
            if "*" not in mname:
                with zf.open(mname) as handle:
                    DumpUnpickler.dump(handle, output_stream)
            else:
                found = False
                for info in zf.infolist():
                    if fnmatch.fnmatch(info.filename, mname):
                        with zf.open(info) as handle:
                            DumpUnpickler.dump(handle, output_stream)
                        found = True
                        break
                if not found:
                    raise Exception(f"Could not find member matching {mname} in {zfname}")  # noqa: TRY002


def main() -> None:
    global strip_file_dir
    parser = argparse.ArgumentParser(description="Zip py source")
    parser.add_argument("paths", nargs="*", help="Paths to zip.")
    parser.add_argument(
        "--install-dir", "--install_dir", help="Root directory for all output files"
    )
    parser.add_argument(
        "--strip-dir",
        "--strip_dir",
        help="The absolute directory we want to remove from zip",
    )
    parser.add_argument(
        "--prepend-str",
        "--prepend_str",
        help="A string to prepend onto all paths of a file in the zip",
        default="",
    )
    parser.add_argument("--zip-name", "--zip_name", help="Output zip name")

    args = parser.parse_args()

    zip_file_name = args.install_dir + "/" + args.zip_name
    strip_file_dir = args.strip_dir
    prepend_str = args.prepend_str
    with ZipFile(zip_file_name, mode="w") as zf:
        for p in sorted(args.paths):
            if os.path.isdir(p):
                files = glob.glob(p + "/**/*.py", recursive=True)
                for file_path in sorted(files):
                    # strip the absolute path
                    write_to_zip(
                        file_path, strip_file_dir + "/", zf, prepend_str=prepend_str
                    )
            else:
                write_to_zip(p, strip_file_dir + "/", zf, prepend_str=prepend_str)


def main() -> None:
    """
    Main function for the profile analysis script.
    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--diff",
        nargs=5,
        metavar=(
            "input_file1",
            "name1",
            "input_file2",
            "name2",
            "dtype",
        ),
        help="Two json traces to compare with, specified as <file1> <name1> <file2> <name2> <dtype>",
    )
    parser.add_argument(
        "--name_limit",
        type=int,
        help="the maximum name size in the final report",
    )
    parser.add_argument(
        "--augment_trace",
        "-a",
        nargs=3,
        metavar=("input_file", "output_file", "dtype"),
        help="Augment a trace with inductor meta information. Provide input and output file paths.",
    )
    parser.add_argument(
        "--analysis",
        nargs=2,
        metavar=("input_file", "dtype"),
        help="Run analysis on a single trace, specified as <file> <dtype>",
    )
    parser.add_argument(
        "--combine",
        nargs="+",
        metavar=("input_files", "output_file"),
        help="Combine multiple profiles into a single profile by merging trace events. Specify as <input_file1> \
<input_file2> [input_file3 ...] <output_file>. The last argument is the output file, all preceding arguments are \
input files to combine.",
    )
    args = parser.parse_args()

    if args.diff:
        p1 = JsonProfile(args.diff[0], args.diff[1], dtype=args.diff[4])
        p1.augment_trace()
        p2 = JsonProfile(args.diff[2], args.diff[3], dtype=args.diff[4])
        p2.augment_trace()
        if args.name_limit:
            print(p1.report(p2, name_limit=args.name_limit))
        else:
            print(p1.report(p2))
    if args.analysis:
        p1 = JsonProfile(
            args.analysis[0],
            dtype=args.analysis[1],
        )
        p1.augment_trace()
        if args.name_limit:
            print(p1.report(name_limit=args.name_limit))
        else:
            print(p1.report())
    if args.augment_trace:
        p = JsonProfile(args.augment_trace[0], dtype=args.augment_trace[2])
        p.augment_trace()
        p.dump(args.augment_trace[1])
    if args.combine:
        input_files = args.combine[:-1]  # All arguments except the last one
        output_file = args.combine[-1]  # Last argument is the output file

        if len(input_files) < 2:
            print("Error: At least 2 input files are required for combining")
            return

        # Load the first profile
        combined = JsonProfile(input_files[0], dtype=None)

        # Iteratively combine with all other profiles
        for input_file in input_files[1:]:
            profile = JsonProfile(input_file, dtype=None)
            combined = combined.combine_with(profile)

        combined.dump(output_file)
        print(f"Successfully combined {', '.join(input_files)} into {output_file}")


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--pickler", type=functools.partial(_lookup_and_create_type, SubprocPickler)
        )
        parser.add_argument("--kind", type=SubprocKind)
        parser.add_argument("--workers", type=int)
        parser.add_argument("--parent", type=int)
        parser.add_argument("--read-fd", type=int)
        parser.add_argument("--write-fd", type=int)
        parser.add_argument("--torch-key", type=str)
        args = parser.parse_args()
        if os.getppid() != args.parent:
            sys.exit(0)
        read_fd = os.fdopen(args.read_fd, "rb")
        write_fd = os.fdopen(args.write_fd, "wb")

        pre_fork_setup()

        torch_key.set(base64.b64decode(args.torch_key.encode("utf-8")))  # type: ignore[attr-defined]

        _async_compile_initializer(args.parent)

        SubprocMain(args.pickler, args.kind, args.workers, read_fd, write_fd).main()
    except Exception:
        log.exception("Uncaught exception in compile_worker subprocess")


def main(argv, *, stdout=None) -> None:
    warnings.warn("torch.utils.model_dump is deprecated and will be removed in a future PyTorch release.", stacklevel=2)
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", choices=["json", "html"])
    parser.add_argument("--title")
    parser.add_argument("model")
    args = parser.parse_args(argv[1:])

    info = get_model_info(args.model, title=args.title)

    output = stdout or sys.stdout

    if args.style == "json":
        output.write(json.dumps(info, sort_keys=True) + "\n")
    elif args.style == "html":
        skeleton = get_inline_skeleton()
        page = burn_in_info(skeleton, info)
        output.write(page)
    else:
        raise Exception("Invalid style")  # noqa: TRY002


def main() -> None:
    """
    # Inject file into template datapipe.pyi.in.

    TODO: The current implementation of this script only generates interfaces for built-in methods. To generate
          interface for user-defined DataPipes, consider changing `IterDataPipe.register_datapipe_as_function`.
    """
    iter_method_definitions = get_method_definitions(
        iterDP_file_path,
        iterDP_files_to_exclude,
        iterDP_deprecated_files,
        "IterDataPipe",
        iterDP_method_to_special_output_type,
    )

    map_method_definitions = get_method_definitions(
        mapDP_file_path,
        mapDP_files_to_exclude,
        mapDP_deprecated_files,
        "MapDataPipe",
        mapDP_method_to_special_output_type,
    )

    path = Path(__file__).absolute().parent
    fm = FileManager(install_dir=path, template_dir=path, dry_run=False)
    fm.write_with_template(
        "datapipe.pyi",
        "datapipe.pyi.in",
        lambda: {
            "IterDataPipeMethods": iter_method_definitions,
            "MapDataPipeMethods": map_method_definitions,
        },
    )


def main() -> None:
    tasks = [
        ("add", "add", "torch.add(x, y)"),
        ("add", "add (extra +0)", "torch.add(x, y + zero)"),
    ]

    serialized_results = []
    repeats = 2
    timers = [
        benchmark_utils.Timer(
            stmt=stmt,
            globals={
                "torch": torch if branch == "master" else FauxTorch(torch, overhead_ns),
                "x": torch.ones((size, 4)),
                "y": torch.ones((1, 4)),
                "zero": torch.zeros(()),
            },
            label=label,
            sub_label=sub_label,
            description=f"size: {size}",
            env=branch,
            num_threads=num_threads,
        )
        for branch, overhead_ns in [("master", None), ("my_branch", 1), ("severe_regression", 5)]
        for label, sub_label, stmt in tasks
        for size in [1, 10, 100, 1000, 10000, 50000]
        for num_threads in [1, 4]
    ]

    for i, timer in enumerate(timers * repeats):
        serialized_results.append(pickle.dumps(
            timer.blocked_autorange(min_run_time=0.05)
        ))
        print(f"\r{i + 1} / {len(timers) * repeats}", end="")
        sys.stdout.flush()
    print()

    comparison = benchmark_utils.Compare([
        pickle.loads(i) for i in serialized_results
    ])

    print("== Unformatted " + "=" * 80 + "\n" + "/" * 95 + "\n")
    comparison.print()

    print("== Formatted " + "=" * 80 + "\n" + "/" * 93 + "\n")
    comparison.trim_significant_figures()
    comparison.colorize()
    comparison.print()


def main() -> None:
    add_fuzzer = benchmark_utils.Fuzzer(
        parameters=[
            [
                benchmark_utils.FuzzedParameter(
                    name=f"k{i}",
                    minval=16,
                    maxval=16 * 1024,
                    distribution="loguniform",
                ) for i in range(3)
            ],
            benchmark_utils.FuzzedParameter(
                name="d",
                distribution={2: 0.6, 3: 0.4},
            ),
        ],
        tensors=[
            [
                benchmark_utils.FuzzedTensor(
                    name=name,
                    size=("k0", "k1", "k2"),
                    dim_parameter="d",
                    probability_contiguous=0.75,
                    min_elements=64 * 1024,
                    max_elements=128 * 1024,
                ) for name in ("x", "y")
            ],
        ],
        seed=0,
    )

    n = 250
    measurements = []
    for i, (tensors, tensor_properties, _) in enumerate(add_fuzzer.take(n=n)):
        x, x_order = tensors["x"], str(tensor_properties["x"]["order"])
        y, y_order = tensors["y"], str(tensor_properties["y"]["order"])
        shape = ", ".join(tuple(f'{i:>4}' for i in x.shape))

        description = "".join([
            f"{x.numel():>7} | {shape:<16} | ",
            f"{'contiguous' if x.is_contiguous() else x_order:<12} | ",
            f"{'contiguous' if y.is_contiguous() else y_order:<12} | ",
        ])

        timer = benchmark_utils.Timer(
            stmt="x + y",
            globals=tensors,
            description=description,
        )

        measurements.append(timer.blocked_autorange(min_run_time=0.1))
        measurements[-1].metadata = {"numel": x.numel()}
        print(f"\r{i + 1} / {n}", end="")
        sys.stdout.flush()
    print()

    # More string munging to make pretty output.
    print(f"Average attempts per valid config: {1. / (1. - add_fuzzer.rejection_rate):.1f}")

    def time_fn(m):
        return m.median / m.metadata["numel"]
    measurements.sort(key=time_fn)

    template = f"{{:>6}}{' ' * 19}Size    Shape{' ' * 13}X order        Y order\n{'-' * 80}"
    print(template.format("Best:"))
    for m in measurements[:15]:
        print(f"{time_fn(m) * 1e9:>4.1f} ns / element     {m.description}")

    print("\n" + template.format("Worst:"))
    for m in measurements[-15:]:
        print(f"{time_fn(m) * 1e9:>4.1f} ns / element     {m.description}")


def main() -> None:
    run(n=100, stmt="torch.median(x, dim=0)", fuzzer_cls=UnaryOpFuzzer)
    run(n=100, stmt="torch.square(x)", fuzzer_cls=UnaryOpFuzzer)
    run(n=100, stmt="x + y", fuzzer_cls=BinaryOpFuzzer)


def main() -> None:
    timer = benchmark_utils.Timer(
        stmt="x + y",
        globals={"x": torch.ones((4, 8)), "y": torch.ones((1, 8))},
        label="Broadcasting add (4x8)",
    )

    for i in range(3):
        print(f"Run: {i}\n{'-' * 40}")
        print(f"timeit:\n{timer.timeit(10000)}\n")
        print(f"autorange:\n{timer.blocked_autorange()}\n\n")


def main(
    port: int,
    dump_dir: str | None,
    dump_interval: float,
    handlers: list[DebugHandler],
    enabled_dumps: set[str],
    fetch_timeout: float = 60.0,
) -> None:
    for handler in handlers:
        handler.fetch_timeout = fetch_timeout

    logger.setLevel(logging.INFO)

    server = FrontendServer(port=port, handlers=handlers)
    logger.info("Frontend server started on port %d", server._server.server_port)

    dumper: PeriodicDumper | None = None
    if dump_dir is not None:
        dumper = PeriodicDumper(
            [
                handler
                for handler in handlers
                if handler.dump_filename() in enabled_dumps
            ],
            dump_dir,
            dump_interval,
        )
        dumper.start()
        logger.info(
            "Periodic dumper started, writing to %s every %.0fs",
            dump_dir,
            dump_interval,
        )

    try:
        server.join()
    finally:
        if dumper is not None:
            dumper.stop()


def main(args: Sequence[str] | None = None) -> None:
    config = JobConfig()
    # pyrefly: ignore [bad-assignment]
    args = config.parse_args(args)
    # pyrefly: ignore [missing-attribute]
    if not args.trace_dir:
        raise AssertionError("Trace directory trace_dir is required")
    # pyrefly: ignore [bad-argument-type]
    details, version = read_dir(args)
    # pyrefly: ignore [missing-attribute]
    if args.transform_ft:
        # pyrefly: ignore [missing-attribute]
        if not args.group_world_size:
            raise AssertionError("World size is required for transform_ft")
        # pyrefly: ignore [bad-argument-type]
        details = transform_ft(details, args.group_world_size)
    # pyrefly: ignore [bad-argument-type]
    db = build_db(details, args, version)
    # pyrefly: ignore [missing-attribute]
    if args.output:
        # pyrefly: ignore [no-matching-overload]
        with open(args.output, "wb") as f:
            pickle.dump((types, db), f)


def main(args):
    env_before = set(os.environ.keys())
    if platform.system() in ["Windows", "Darwin"]:
        raise RuntimeError(f"{platform.system()} is not supported!!!")

    if args.log_path:
        os.makedirs(args.log_path, exist_ok=True)
    else:
        args.log_path = os.devnull

    if args.latency_mode and args.throughput_mode:
        raise RuntimeError(
            "Either args.latency_mode or args.throughput_mode should be set"
        )

    if not args.no_python and not args.program.endswith(".py"):
        raise RuntimeError(
            'For non Python script, you should use "--no-python" parameter.'
        )

    # Verify LD_PRELOAD
    if "LD_PRELOAD" in os.environ:
        lst_valid = []
        tmp_ldpreload = os.environ["LD_PRELOAD"]
        for item in tmp_ldpreload.split(":"):
            matches = glob.glob(item)
            if len(matches) > 0:
                lst_valid.append(item)
            else:
                logger.warning("%s doesn't exist. Removing it from LD_PRELOAD.", item)
        if len(lst_valid) > 0:
            os.environ["LD_PRELOAD"] = ":".join(lst_valid)
        else:
            os.environ["LD_PRELOAD"] = ""

    launcher = _Launcher()
    launcher.launch(args)
    for x in sorted(set(os.environ.keys()) - env_before):
        logger.debug("%s=%s", x, os.environ[x])


def main(project_dir=None):
    runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count("-v"))
    suite = all_tests_suite(project_dir=project_dir)
    raise SystemExit(not runner.run(suite).wasSuccessful())


def main() -> None:
    """Run the main entry point."""
    app_name = "MyApp"
    app_author = "MyCompany"

    print(f"-- platformdirs {__version__} --")  # noqa: T201

    print("-- app dirs (with optional 'version')")  # noqa: T201
    dirs = PlatformDirs(app_name, app_author, version="1.0")
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (without optional 'version')")  # noqa: T201
    dirs = PlatformDirs(app_name, app_author)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (without optional 'appauthor')")  # noqa: T201
    dirs = PlatformDirs(app_name)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (with disabled 'appauthor')")  # noqa: T201
    dirs = PlatformDirs(app_name, appauthor=False)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201


def main() -> NoReturn:  # needed for console script
    if __package__ == "":
        # To be able to run 'python wheel-0.9.whl/wheel':
        import os.path

        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]

    from ._commands import main as cli_main

    sys.exit(cli_main())


def main() -> int:
    p = parser()
    args = p.parse_args()
    if not hasattr(args, "func"):
        p.print_help()
    else:
        try:
            args.func(args)
            return 0
        except WheelError as e:
            print(e, file=sys.stderr)

    return 1


def main():
    import argparse

    description = 'A simple command-line interface for tarfile module.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Verbose output')
    parser.add_argument('--filter', metavar='<filtername>',
                        choices=_NAMED_FILTERS,
                        help='Filter for extraction')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--list', metavar='<tarfile>',
                       help='Show listing of a tarfile')
    group.add_argument('-e', '--extract', nargs='+',
                       metavar=('<tarfile>', '<output_dir>'),
                       help='Extract tarfile into target dir')
    group.add_argument('-c', '--create', nargs='+',
                       metavar=('<name>', '<file>'),
                       help='Create tarfile from sources')
    group.add_argument('-t', '--test', metavar='<tarfile>',
                       help='Test if a tarfile is valid')

    args = parser.parse_args()

    if args.filter and args.extract is None:
        parser.exit(1, '--filter is only valid for extraction\n')

    if args.test is not None:
        src = args.test
        if is_tarfile(src):
            with open(src, 'r') as tar:
                tar.getmembers()
                print(tar.getmembers(), file=sys.stderr)
            if args.verbose:
                print('{!r} is a tar archive.'.format(src))
        else:
            parser.exit(1, '{!r} is not a tar archive.\n'.format(src))

    elif args.list is not None:
        src = args.list
        if is_tarfile(src):
            with TarFile.open(src, 'r:*') as tf:
                tf.list(verbose=args.verbose)
        else:
            parser.exit(1, '{!r} is not a tar archive.\n'.format(src))

    elif args.extract is not None:
        if len(args.extract) == 1:
            src = args.extract[0]
            curdir = os.curdir
        elif len(args.extract) == 2:
            src, curdir = args.extract
        else:
            parser.exit(1, parser.format_help())

        if is_tarfile(src):
            with TarFile.open(src, 'r:*') as tf:
                tf.extractall(path=curdir, filter=args.filter)
            if args.verbose:
                if curdir == '.':
                    msg = '{!r} file is extracted.'.format(src)
                else:
                    msg = ('{!r} file is extracted '
                           'into {!r} directory.').format(src, curdir)
                print(msg)
        else:
            parser.exit(1, '{!r} is not a tar archive.\n'.format(src))

    elif args.create is not None:
        tar_name = args.create.pop(0)
        _, ext = os.path.splitext(tar_name)
        compressions = {
            # gz
            '.gz': 'gz',
            '.tgz': 'gz',
            # xz
            '.xz': 'xz',
            '.txz': 'xz',
            # bz2
            '.bz2': 'bz2',
            '.tbz': 'bz2',
            '.tbz2': 'bz2',
            '.tb2': 'bz2',
        }
        tar_mode = 'w:' + compressions[ext] if ext in compressions else 'w'
        tar_files = args.create

        with TarFile.open(tar_name, tar_mode) as tf:
            for file_name in tar_files:
                tf.add(file_name)

        if args.verbose:
            print('{!r} file created.'.format(tar_name))


def main():
    parser = argparse.ArgumentParser(description='Download SciPy data files.')
    parser.add_argument("path", nargs='?', type=str,
                        default=pooch.os_cache('scipy-data'),
                        help="Directory path to download all the data files.")
    args = parser.parse_args()
    download_all(args.path)


def main():
    t_start = time.perf_counter()

    total_cases = 2 * len(cdf_pdf_cases) + len(moment_cases)
    print(f"Processing {total_cases} test cases")

    print(f"Running 1st batch ({len(cdf_pdf_cases)} PDF cases). "
          f"These take about 30s each.")
    run_cases(cdf_pdf_cases, run_pdf, "pdf_data")

    print(f"Running 2nd batch ({len(cdf_pdf_cases)} CDF cases). "
          f"These take about 30s each.")
    run_cases(cdf_pdf_cases, run_cdf, "cdf_data")

    print(f"Running 3rd batch ({len(moment_cases)} moment cases). "
          f"These take about anywhere from a few hours to days each.")
    run_cases(moment_cases, run_moment, "moment_data")

    print(f"Test data generated in {time.perf_counter() - t_start}s")


def main():
    print(__doc__)
    fn = os.path.join('..', 'cephes', 'expn.h')

    K = 12
    A = generate_A(K)
    with open(fn + '.new', 'w') as f:
        f.write(WARNING)
        f.write(f"#define nA {len(A)}\n")
        for k, Ak in enumerate(A):
            ', '.join([str(x.evalf(18)) for x in Ak.coeffs()])
            f.write(f"static const double A{k}[] = {{tmp}};\n")
        ", ".join([f"A{k}" for k in range(K + 1)])
        f.write("static const double *A[] = {{tmp}};\n")
        ", ".join([str(Ak.degree()) for Ak in A])
        f.write("static const int Adegs[] = {{tmp}};\n")
    os.rename(fn + '.new', fn)


def main():
    print(__doc__)
    K = 25
    N = 25
    with mp.workdps(50):
        d = compute_d(K, N)
    fn = os.path.join(os.path.dirname(__file__), '..', 'cephes', 'igam.h')
    with open(fn + '.new', 'w') as f:
        f.write(header.format(K, N))
        for k, row in enumerate(d):
            row = [mp.nstr(x, 17, min_fixed=0, max_fixed=0) for x in row]
            f.write('{')
            f.write(", ".join(row))
            if k < K - 1:
                f.write('},\n')
            else:
                f.write('}};\n')
        f.write(footer)
    os.rename(fn + '.new', fn)


def main():
    t0 = time()
    # It would be nice to have data for larger values, but either this
    # requires prohibitively large precision (dps > 800) or mpmath has
    # a bug. For example, gammainc(1e20, 1e20, dps=800) returns a
    # value around 0.03, while the true value should be close to 0.5
    # (DLMF 8.12.15).
    print(__doc__)
    pwd = os.path.dirname(__file__)
    r = np.logspace(4, 14, 30)
    ltheta = np.logspace(np.log10(pi/4), np.log10(np.arctan(0.6)), 30)
    utheta = np.logspace(np.log10(pi/4), np.log10(np.arctan(1.4)), 30)

    regimes = [(gammainc, ltheta), (gammaincc, utheta)]
    for func, theta in regimes:
        rg, thetag = np.meshgrid(r, theta)
        a, x = rg*np.cos(thetag), rg*np.sin(thetag)
        a, x = a.flatten(), x.flatten()
        dataset = []
        for i, (a0, x0) in enumerate(zip(a, x)):
            if func == gammaincc:
                # Exploit the fast integer path in gammaincc whenever
                # possible so that the computation doesn't take too
                # long
                a0, x0 = np.floor(a0), np.floor(x0)
            dataset.append((a0, x0, func(a0, x0)))
        dataset = np.array(dataset)
        filename = os.path.join(pwd, '..', 'tests', 'data', 'local',
                                f'{func.__name__}.txt')
        np.savetxt(filename, dataset)

    print(f"{(time() - t0)/60} minutes elapsed")


def main(
        outpath,
        n_jobs=1,
        box_size=2.0,
        grid_size=20,
        regions=None,
        parameter_groups=None,
        compute_mp=True,
):
    outpath = os.path.realpath(os.path.expanduser(outpath))

    random_state = np.random.RandomState(1234)
    # Parameters a, b, c selected near these values.
    root_params = np.array(
        [-16, -8, -4, -2, -1, 1, 2, 4, 8, 16]
    )
    # Perturbations to apply to root values.
    perturbations = 0.1 * random_state.random_sample(
        size=(3, len(root_params))
    )

    params = []
    # Parameter group 1
    # -----------------
    # No integer differences. This has been confirmed for the above seed.
    A = root_params + perturbations[0, :]
    B = root_params + perturbations[1, :]
    C = root_params + perturbations[2, :]
    params.extend(
        sorted(
            ((a, b, c, 1) for a, b, c in product(A, B, C)),
            key=lambda x: max(abs(x[0]), abs(x[1])),
        )
    )

    # Parameter group 2
    # -----------------
    # B - A an integer
    A = root_params + 0.5
    B = root_params + 0.5
    C = root_params + perturbations[1, :]
    params.extend(
        sorted(
            ((a, b, c, 2) for a, b, c in product(A, B, C)),
            key=lambda x: max(abs(x[0]), abs(x[1])),
        )
    )

    # Parameter group 3
    # -----------------
    # C - A an integer
    A = root_params + 0.5
    B = root_params + perturbations[1, :]
    C = root_params + 0.5
    params.extend(
        sorted(
            ((a, b, c, 3) for a, b, c in product(A, B, C)),
            key=lambda x: max(abs(x[0]), abs(x[1])),
        )
    )

    # Parameter group 4
    # -----------------
    # C - B an integer
    A = root_params + perturbations[0, :]
    B = root_params + 0.5
    C = root_params + 0.5
    params.extend(
        sorted(
            ((a, b, c, 4) for a, b, c in product(A, B, C)),
            key=lambda x: max(abs(x[0]), abs(x[1])),
        )
    )

    # Parameter group 5
    # -----------------
    # C - A - B an integer
    A = root_params + 0.25
    B = root_params + 0.25
    C = root_params + 0.5
    params.extend(
        sorted(
            ((a, b, c, 5) for a, b, c in product(A, B, C)),
            key=lambda x: max(abs(x[0]), abs(x[1])),
        )
    )

    # Parameter group 6
    # -----------------
    # A an integer
    A = root_params
    B = root_params + perturbations[0, :]
    C = root_params + perturbations[1, :]
    params.extend(
        sorted(
            ((a, b, c, 6) for a, b, c in product(A, B, C)),
            key=lambda x: max(abs(x[0]), abs(x[1])),
        )
    )

    # Parameter group 7
    # -----------------
    # B an integer
    A = root_params + perturbations[0, :]
    B = root_params
    C = root_params + perturbations[1, :]
    params.extend(
        sorted(
            ((a, b, c, 7) for a, b, c in product(A, B, C)),
            key=lambda x: max(abs(x[0]), abs(x[1])),
        )
    )

    # Parameter group 8
    # -----------------
    # C an integer
    A = root_params + perturbations[0, :]
    B = root_params + perturbations[1, :]
    C = root_params
    params.extend(
        sorted(
            ((a, b, c, 8) for a, b, c in product(A, B, C)),
            key=lambda x: max(abs(x[0]), abs(x[1])),
        )
    )

    # Parameter group 9
    # -----------------
    # Wide range of magnitudes, c - a - b > 0.
    phi = (1 + np.sqrt(5))/2
    P = phi**np.arange(16)
    P = np.hstack([-P, P])
    group_9_params = sorted(
        (
            (a, b, c, 9) for a, b, c in product(P, P, P) if c - a - b > 0
        ),
        key=lambda x: max(abs(x[0]), abs(x[1])),
    )

    if parameter_groups is not None:
        # Group 9 params only used if specified in arguments.
        params.extend(group_9_params)
        params = [
            (a, b, c, group) for a, b, c, group in params
            if group in parameter_groups
        ]

    # grid_size * grid_size grid in box with corners
    # -2 - 2j, -2 + 2j, 2 - 2j, 2 + 2j
    X, Y = np.meshgrid(
        np.linspace(-box_size, box_size, grid_size),
        np.linspace(-box_size, box_size, grid_size)
    )
    Z = X + Y * 1j
    Z = Z.flatten().tolist()
    # Add z = 1 + 0j (region 0).
    Z.append(1 + 0j)
    if regions is not None:
        Z = [z for z in Z if get_region(z) in regions]

    # Evaluate scipy and mpmath's hyp2f1 for all parameter combinations
    # above against all arguments in the grid Z
    rows = get_results(params, Z, n_jobs=n_jobs, compute_mp=compute_mp)

    with open(outpath, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(
            [
                "a",
                "b",
                "c",
                "z",
                "|z|",
                "region",
                "parameter_group",
                "expected",  # mpmath's hyp2f1
                "observed",  # scipy's hyp2f1
                "relative_error",
                "absolute_error",
            ]
        )
        for row in rows:
            writer.writerow(row)


def main():
    print(__doc__)
    with mpmath.workdps(50):
        p, q = lambertw_pade()
        p, q = p[::-1], q[::-1]
        print(f"p = {p}")
        print(f"q = {q}")

    x, y = np.linspace(-1.5, 1.5, 75), np.linspace(-1.5, 1.5, 75)
    x, y = np.meshgrid(x, y)
    z = x + 1j*y
    lambertw_std = []
    for z0 in z.flatten():
        lambertw_std.append(complex(mpmath.lambertw(z0)))
    lambertw_std = np.array(lambertw_std).reshape(x.shape)

    fig, axes = plt.subplots(nrows=3, ncols=1)
    # Compare Pade approximation to true result
    p = np.array([float(p0) for p0 in p])
    q = np.array([float(q0) for q0 in q])
    pade_approx = np.polyval(p, z)/np.polyval(q, z)
    pade_err = abs(pade_approx - lambertw_std)
    axes[0].pcolormesh(x, y, pade_err)
    # Compare two terms of asymptotic series to true result
    asy_approx = np.log(z) - np.log(np.log(z))
    asy_err = abs(asy_approx - lambertw_std)
    axes[1].pcolormesh(x, y, asy_err)
    # Compare two terms of the series around the branch point to the
    # true result
    p = np.sqrt(2*(np.exp(1)*z + 1))
    series_approx = -1 + p - p**2/3
    series_err = abs(series_approx - lambertw_std)
    im = axes[2].pcolormesh(x, y, series_err)

    fig.colorbar(im, ax=axes.ravel().tolist())
    plt.show()

    fig, ax = plt.subplots(nrows=1, ncols=1)
    pade_better = pade_err < asy_err
    im = ax.pcolormesh(x, y, pade_better)
    t = np.linspace(-0.3, 0.3)
    ax.plot(-2.5*abs(t) - 0.2, t, 'r')
    fig.colorbar(im, ax=ax)
    plt.show()


def main():
    print(__doc__)
    print()
    stirling_coeffs = [mpmath.nstr(x, 20, min_fixed=0, max_fixed=0)
                       for x in stirling_series(8)[::-1]]
    taylor_coeffs = [mpmath.nstr(x, 20, min_fixed=0, max_fixed=0)
                     for x in taylor_series_at_1(23)[::-1]]
    print("Stirling series coefficients")
    print("----------------------------")
    print("\n".join(stirling_coeffs))
    print()
    print("Taylor series coefficients")
    print("--------------------------")
    print("\n".join(taylor_coeffs))
    print()


def main():
    plt.clf()
    plt.subplot(121)
    do_plot(True)
    plt.title('Struve H')

    plt.subplot(122)
    do_plot(False)
    plt.title('Struve L')

    plt.savefig('struve_convergence.png')
    plt.show()


def main():
    desired_error = 2 * np.finfo(float).eps
    print('Series Error')
    for x in [1e5, 1e10, 1e15, 1e20]:
        with mpmath.workdps(100):
            error = wrightomega_series_error(x)
        print(x, error, error < desired_error)

    print('Exp error')
    for x in [-10, -25, -50, -100, -200, -400, -700, -740]:
        with mpmath.workdps(100):
            error = wrightomega_exp_error(x)
        print(x, error, error < desired_error)


def main():
    t0 = time()
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('action', type=int, choices=[1, 2, 3, 4],
                        help='chose what expansion to precompute\n'
                             '1 : Series for small a\n'
                             '2 : Series for small a and small b\n'
                             '3 : Asymptotic series for large x\n'
                             '    This may take some time (>4h).\n'
                             '4 : Fit optimal eps for integral representation.'
                        )
    args = parser.parse_args()

    switch = {1: lambda: print(series_small_a()),
              2: lambda: print(series_small_a_small_b()),
              3: lambda: print(asymptotic_series()),
              4: lambda: print(optimal_epsilon_integral())
              }
    switch.get(args.action, lambda: print("Invalid input."))()
    print(f"\n{(time() - t0)/60:.1f} minutes elapsed.\n")


def main():
    t0 = time()
    print(__doc__)
    pwd = os.path.dirname(__file__)
    eps = np.finfo(float).eps * 100

    a_range = np.array([eps,
                        1e-4 * (1 - eps), 1e-4, 1e-4 * (1 + eps),
                        1e-3 * (1 - eps), 1e-3, 1e-3 * (1 + eps),
                        0.1, 0.5,
                        1 * (1 - eps), 1, 1 * (1 + eps),
                        1.5, 2, 4.999, 5, 10])
    b_range = np.array([0, eps, 1e-10, 1e-5, 0.1, 1, 2, 10, 20, 100])
    x_range = np.array([0, eps, 1 - eps, 1, 1 + eps,
                        1.5,
                        2 - eps, 2, 2 + eps,
                        9 - eps, 9, 9 + eps,
                        10 * (1 - eps), 10, 10 * (1 + eps),
                        100 * (1 - eps), 100, 100 * (1 + eps),
                        500, exp_inf, 1e3, 1e5, 1e10, 1e20])

    a_range, b_range, x_range = np.meshgrid(a_range, b_range, x_range,
                                            indexing='ij')
    a_range = a_range.flatten()
    b_range = b_range.flatten()
    x_range = x_range.flatten()

    # filter out some values, especially too large x
    bool_filter = ~((a_range < 5e-3) & (x_range >= exp_inf))
    bool_filter = bool_filter & ~((a_range < 0.2) & (x_range > exp_inf))
    bool_filter = bool_filter & ~((a_range < 0.5) & (x_range > 1e3))
    bool_filter = bool_filter & ~((a_range < 0.56) & (x_range > 5e3))
    bool_filter = bool_filter & ~((a_range < 1) & (x_range > 1e4))
    bool_filter = bool_filter & ~((a_range < 1.4) & (x_range > 1e5))
    bool_filter = bool_filter & ~((a_range < 1.8) & (x_range > 1e6))
    bool_filter = bool_filter & ~((a_range < 2.2) & (x_range > 1e7))
    bool_filter = bool_filter & ~((a_range < 2.5) & (x_range > 1e8))
    bool_filter = bool_filter & ~((a_range < 2.9) & (x_range > 1e9))
    bool_filter = bool_filter & ~((a_range < 3.3) & (x_range > 1e10))
    bool_filter = bool_filter & ~((a_range < 3.7) & (x_range > 1e11))
    bool_filter = bool_filter & ~((a_range < 4) & (x_range > 1e12))
    bool_filter = bool_filter & ~((a_range < 4.4) & (x_range > 1e13))
    bool_filter = bool_filter & ~((a_range < 4.7) & (x_range > 1e14))
    bool_filter = bool_filter & ~((a_range < 5.1) & (x_range > 1e15))
    bool_filter = bool_filter & ~((a_range < 5.4) & (x_range > 1e16))
    bool_filter = bool_filter & ~((a_range < 5.8) & (x_range > 1e17))
    bool_filter = bool_filter & ~((a_range < 6.2) & (x_range > 1e18))
    bool_filter = bool_filter & ~((a_range < 6.2) & (x_range > 1e18))
    bool_filter = bool_filter & ~((a_range < 6.5) & (x_range > 1e19))
    bool_filter = bool_filter & ~((a_range < 6.9) & (x_range > 1e20))

    # filter out known values that do not meet the required numerical accuracy
    # see test test_wright_data_grid_failures
    failing = np.array([
        [0.1, 100, 709.7827128933841],
        [0.5, 10, 709.7827128933841],
        [0.5, 10, 1000],
        [0.5, 100, 1000],
        [1, 20, 100000],
        [1, 100, 100000],
        [1.0000000000000222, 20, 100000],
        [1.0000000000000222, 100, 100000],
        [1.5, 0, 500],
        [1.5, 2.220446049250313e-14, 500],
        [1.5, 1.e-10, 500],
        [1.5, 1.e-05, 500],
        [1.5, 0.1, 500],
        [1.5, 20, 100000],
        [1.5, 100, 100000],
        ]).tolist()

    does_fail = np.full_like(a_range, False, dtype=bool)
    for i in range(x_range.size):
        if [a_range[i], b_range[i], x_range[i]] in failing:
            does_fail[i] = True

    # filter and flatten
    a_range = a_range[bool_filter]
    b_range = b_range[bool_filter]
    x_range = x_range[bool_filter]
    does_fail = does_fail[bool_filter]

    dataset = []
    print(f"Computing {x_range.size} single points.")
    print("Tests will fail for the following data points:")
    for i in range(x_range.size):
        a = a_range[i]
        b = b_range[i]
        x = x_range[i]
        # take care of difficult corner cases
        maxterms = 1000
        if a < 1e-6 and x >= exp_inf/10:
            maxterms = 2000
        f = mp_wright_bessel(a, b, x, maxterms=maxterms)
        if does_fail[i]:
            print("failing data point a, b, x, value = "
                  f"[{a}, {b}, {x}, {f}]")
        else:
            dataset.append((a, b, x, f))
    dataset = np.array(dataset)

    filename = os.path.join(pwd, '..', 'tests', 'data', 'local',
                            'wright_bessel.txt')
    np.savetxt(filename, dataset)

    print(f"{(time() - t0)/60:.1f} minutes elapsed")


def main():
    print(__doc__)
    coeffs = zetac_series(10)
    coeffs = [mpmath.nstr(x, 20, min_fixed=0, max_fixed=0)
              for x in coeffs]
    print("\n".join(coeffs[::-1]))


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    screen.fill((255, 0, 0))
    s = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    pygame.draw.line(s, (0, 0, 0), (250, 250), (250 + 200, 250))

    width = 1
    for a_radius in range(width):
        radius = 200
        pygame.gfxdraw.aacircle(s, 250, 250, radius - a_radius, (0, 0, 0))

    screen.blit(s, (0, 0))

    pygame.draw.circle(screen, "green", (50, 100), 10)
    pygame.draw.circle(screen, "black", (50, 100), 10, 1)

    pygame.display.flip()
    try:
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == "q":
                    break
            pygame.display.flip()
    finally:
        pygame.quit()


def main(winstyle=0):
    # Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    img = load_image("player1.gif")
    Player.images = [img, pg.transform.flip(img, 1, 0)]
    img = load_image("explosion1.gif")
    Explosion.images = [img, pg.transform.flip(img, 1, 1)]
    Alien.images = [load_image(im) for im in ("alien1.gif", "alien2.gif", "alien3.gif")]
    Bomb.images = [load_image("bomb.gif")]
    Shot.images = [load_image("shot.gif")]

    # decorate the game window
    icon = pg.transform.scale(Alien.images[0], (32, 32))
    pg.display.set_icon(icon)
    pg.display.set_caption("Pygame Aliens")
    pg.mouse.set_visible(0)

    # create the background, tile the bgd image
    bgdtile = load_image("background.gif")
    background = pg.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    # load the sound effects
    boom_sound = load_sound("boom.wav")
    shoot_sound = load_sound("car_door.wav")
    if pg.mixer:
        music = os.path.join(main_dir, "data", "house_lo.wav")
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1)

    # Initialize Game Groups
    aliens = pg.sprite.Group()
    shots = pg.sprite.Group()
    bombs = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()
    lastalien = pg.sprite.GroupSingle()

    # Create Some Starting Values
    alienreload = ALIEN_RELOAD
    clock = pg.time.Clock()

    # initialize our starting sprites
    global SCORE
    player = Player(all)
    Alien(
        aliens, all, lastalien
    )  # note, this 'lives' because it goes into a sprite group
    if pg.font:
        all.add(Score(all))

    # Run our main loop whilst the player is alive.
    while player.alive():
        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle | pg.FULLSCREEN, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    fullscreen = not fullscreen

        keystate = pg.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        # update all the sprites
        all.update()

        # handle player input
        direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        player.move(direction)
        firing = keystate[pg.K_SPACE]
        if not player.reloading and firing and len(shots) < MAX_SHOTS:
            Shot(player.gunpos(), shots, all)
            if pg.mixer and shoot_sound is not None:
                shoot_sound.play()
        player.reloading = firing

        # Create new alien
        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * ALIEN_ODDS):
            Alien(aliens, all, lastalien)
            alienreload = ALIEN_RELOAD

        # Drop bombs
        if lastalien and not int(random.random() * BOMB_ODDS):
            Bomb(lastalien.sprite, all, bombs, all)

        # Detect collisions between aliens and players.
        for alien in pg.sprite.spritecollide(player, aliens, 1):
            if pg.mixer and boom_sound is not None:
                boom_sound.play()
            Explosion(alien, all)
            Explosion(player, all)
            SCORE = SCORE + 1
            player.kill()

        # See if shots hit the aliens.
        for alien in pg.sprite.groupcollide(aliens, shots, 1, 1).keys():
            if pg.mixer and boom_sound is not None:
                boom_sound.play()
            Explosion(alien, all)
            SCORE = SCORE + 1

        # See if alien bombs hit the player.
        for bomb in pg.sprite.spritecollide(player, bombs, 1):
            if pg.mixer and boom_sound is not None:
                boom_sound.play()
            Explosion(player, all)
            Explosion(bomb, all)
            player.kill()

        # draw the scene
        dirty = all.draw(screen)
        pg.display.update(dirty)

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(40)

    if pg.mixer:
        pg.mixer.music.fadeout(1000)
    pg.time.wait(1000)


def main():
    """show various surfarray effects"""
    import numpy as np
    from numpy import int32, uint

    pg.init()

    print("Using Numpy")
    print("Press the left mouse button to advance image.")
    print('Press the "s" key to save the current image.')

    # allblack
    allblack = np.zeros((128, 128), int32)
    surfdemo_show(allblack, "allblack")

    # striped
    # the element type is required for np.zeros in numpy else
    # an array of float is returned.
    striped = np.zeros((128, 128, 3), int32)
    striped[:] = (255, 0, 0)
    striped[:, ::3] = (0, 255, 255)
    surfdemo_show(striped, "striped")

    # rgbarray
    imagename = os.path.join(main_dir, "data", "arraydemo.bmp")
    imgsurface = pg.image.load(imagename)
    rgbarray = surfarray.array3d(imgsurface)
    surfdemo_show(rgbarray, "rgbarray")

    # flipped
    flipped = rgbarray[:, ::-1]
    surfdemo_show(flipped, "flipped")

    # scaledown
    scaledown = rgbarray[::2, ::2]
    surfdemo_show(scaledown, "scaledown")

    # scaleup
    # the element type is required for np.zeros in numpy else
    # an #array of floats is returned.
    shape = rgbarray.shape
    scaleup = np.zeros((shape[0] * 2, shape[1] * 2, shape[2]), int32)
    scaleup[::2, ::2, :] = rgbarray
    scaleup[1::2, ::2, :] = rgbarray
    scaleup[:, 1::2] = scaleup[:, ::2]
    surfdemo_show(scaleup, "scaleup")

    # redimg
    redimg = np.array(rgbarray)
    redimg[:, :, 1:] = 0
    surfdemo_show(redimg, "redimg")

    # soften
    # having factor as an array forces integer upgrade during multiplication
    # of rgbarray, even for numpy.
    factor = np.array((8,), int32)
    soften = np.array(rgbarray, int32)
    soften[1:, :] += rgbarray[:-1, :] * factor
    soften[:-1, :] += rgbarray[1:, :] * factor
    soften[:, 1:] += rgbarray[:, :-1] * factor
    soften[:, :-1] += rgbarray[:, 1:] * factor
    soften //= 33
    surfdemo_show(soften, "soften")

    # crossfade (50%)
    src = np.array(rgbarray)
    dest = np.zeros(rgbarray.shape)  # dest is float64 by default.
    dest[:] = 20, 50, 100
    diff = (dest - src) * 0.50
    xfade = src + diff.astype(uint)
    surfdemo_show(xfade, "xfade")

    # all done
    pg.quit()


def main():
    color = [0, 0, 0]
    changed = False
    blendtype = 0
    step = 5

    pg.init()
    screen = pg.display.set_mode((640, 480), 0, 32)
    screen.fill((100, 100, 100))

    image = pg.image.load(os.path.join(data_dir, "liquid.bmp")).convert()
    blendimage = pg.image.load(os.path.join(data_dir, "liquid.bmp")).convert()
    screen.blit(image, (10, 10))
    screen.blit(blendimage, (200, 10))

    pg.display.flip()
    pg.key.set_repeat(500, 30)
    usage()

    going = True
    while going:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

            if event.type == pg.KEYDOWN:
                usage()

                if event.key == pg.K_ESCAPE:
                    going = False

                if event.key == pg.K_r:
                    color[0] += step
                    if color[0] > 255:
                        color[0] = 0
                    changed = True

                elif event.key == pg.K_g:
                    color[1] += step
                    if color[1] > 255:
                        color[1] = 0
                    changed = True

                elif event.key == pg.K_b:
                    color[2] += step
                    if color[2] > 255:
                        color[2] = 0
                    changed = True

                elif event.key == pg.K_a:
                    blendtype = pg.BLEND_ADD
                    changed = True
                elif event.key == pg.K_s:
                    blendtype = pg.BLEND_SUB
                    changed = True
                elif event.key == pg.K_m:
                    blendtype = pg.BLEND_MULT
                    changed = True
                elif event.key == pg.K_PLUS:
                    blendtype = pg.BLEND_MAX
                    changed = True
                elif event.key == pg.K_MINUS:
                    blendtype = pg.BLEND_MIN
                    changed = True

                elif event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9):
                    step = int(event.unicode)

            if changed:
                screen.fill((100, 100, 100))
                screen.blit(image, (10, 10))
                blendimage.blit(image, (0, 0))
                # blendimage.fill (color, (0, 0, 20, 20), blendtype)
                blendimage.fill(color, None, blendtype)
                screen.blit(blendimage, (200, 10))
                print(
                    f"Color: {tuple(color)}, Pixel (0,0): {[blendimage.get_at((0, 0))]}"
                )
                changed = False
                pg.display.flip()

    pg.quit()


def main():
    pg.init()
    pg.mixer.quit()  # remove ALSA underflow messages for Debian squeeze
    screen = pg.display.set_mode((640, 480))

    im1 = pg.Surface(screen.get_size())
    # im1= im1.convert()
    im1.fill((100, 0, 0))

    im2 = pg.Surface(screen.get_size())
    im2.fill((0, 50, 0))
    # we make a srcalpha copy of it.
    # im3= im2.convert(SRCALPHA)
    im3 = im2
    im3.set_alpha(127)

    images = {}
    images[pg.K_1] = im2
    images[pg.K_2] = pg.image.load(os.path.join(data_dir, "chimp.png"))
    images[pg.K_3] = pg.image.load(os.path.join(data_dir, "alien3.gif"))
    images[pg.K_4] = pg.image.load(os.path.join(data_dir, "liquid.bmp"))
    img_to_blit = im2.convert()
    iaa = img_to_blit.convert_alpha()

    blits = {}
    blits[pg.K_a] = pg.BLEND_ADD
    blits[pg.K_s] = pg.BLEND_SUB
    blits[pg.K_m] = pg.BLEND_MULT
    blits[pg.K_EQUALS] = pg.BLEND_MAX
    blits[pg.K_MINUS] = pg.BLEND_MIN

    blitsn = {}
    blitsn[pg.K_a] = "BLEND_ADD"
    blitsn[pg.K_s] = "BLEND_SUB"
    blitsn[pg.K_m] = "BLEND_MULT"
    blitsn[pg.K_EQUALS] = "BLEND_MAX"
    blitsn[pg.K_MINUS] = "BLEND_MIN"

    screen.blit(im1, (0, 0))
    pg.display.flip()
    clock = pg.time.Clock()
    print("one pixel is:%s:" % [im1.get_at((0, 0))])

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            if event.type == pg.KEYDOWN:
                usage()

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False

            elif event.type == pg.KEYDOWN and event.key in images.keys():
                img_to_blit = images[event.key]
                iaa = img_to_blit.convert_alpha()

            elif event.type == pg.KEYDOWN and event.key in blits.keys():
                t1 = time.time()
                # blits is a dict keyed with key -> blit flag.  eg BLEND_ADD.
                im1.blit(img_to_blit, (0, 0), None, blits[event.key])
                t2 = time.time()
                print("one pixel is:%s:" % [im1.get_at((0, 0))])
                print(f"time to do:{t2 - t1}:")

            elif event.type == pg.KEYDOWN and event.key in [pg.K_t]:
                for bkey in blits.keys():
                    t1 = time.time()

                    for x in range(300):
                        im1.blit(img_to_blit, (0, 0), None, blits[bkey])

                    t2 = time.time()

                    # show which key we're doing...
                    onedoing = blitsn[bkey]
                    print(f"time to do :{onedoing}: is :{t2 - t1}:")

            elif event.type == pg.KEYDOWN and event.key in [pg.K_o]:
                t1 = time.time()
                # blits is a dict keyed with key -> blit flag.  eg BLEND_ADD.
                im1.blit(iaa, (0, 0))
                t2 = time.time()
                print("one pixel is:%s:" % [im1.get_at((0, 0))])
                print(f"time to do:{t2 - t1}:")

            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # this additive blend without clamp two surfaces.
                # im1.set_alpha(127)
                # im1.blit(im1, (0,0))
                # im1.set_alpha(255)
                t1 = time.time()

                im1p = pygame.surfarray.pixels2d(im1)
                im2p = pygame.surfarray.pixels2d(im2)
                im1p += im2p
                del im1p
                del im2p
                t2 = time.time()
                print("one pixel is:%s:" % [im1.get_at((0, 0))])
                print(f"time to do:{t2 - t1}:")

            elif event.type == pg.KEYDOWN and event.key in [pg.K_z]:
                t1 = time.time()
                im1p = pygame.surfarray.pixels3d(im1)
                im2p = pygame.surfarray.pixels3d(im2)
                im1p16 = im1p.astype(numpy.uint16)
                im2p16 = im1p.astype(numpy.uint16)
                im1p16 += im2p16
                im1p16 = numpy.minimum(im1p16, 255)
                pygame.surfarray.blit_array(im1, im1p16)

                del im1p
                del im2p
                t2 = time.time()
                print("one pixel is:%s:" % [im1.get_at((0, 0))])
                print(f"time to do:{t2 - t1}:")

            elif event.type == pg.KEYDOWN and event.key in [pg.K_r, pg.K_g, pg.K_b]:
                # this adds one to each pixel.
                colmap = {}
                colmap[pg.K_r] = 0x10000
                colmap[pg.K_g] = 0x00100
                colmap[pg.K_b] = 0x00001
                im1p = pygame.surfarray.pixels2d(im1)
                im1p += colmap[event.key]
                del im1p
                print("one pixel is:%s:" % [im1.get_at((0, 0))])

            elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                print("one pixel is:%s:" % [im1.get_at((0, 0))])

            elif event.type == pg.KEYDOWN and event.key == pg.K_f:
                # this additive blend without clamp two surfaces.

                t1 = time.time()
                im1.set_alpha(127)
                im1.blit(im2, (0, 0))
                im1.set_alpha(255)

                t2 = time.time()
                print("one pixel is:%s:" % [im1.get_at((0, 0))])
                print(f"time to do:{t2 - t1}:")

        screen.blit(im1, (0, 0))
        pg.display.flip()

    pg.quit()


def main():
    pg.init()
    pygame.camera.init()
    VideoCapturePlayer().main()
    pg.quit()


def main():
    """this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((1280, 480), pg.SCALED)
    pg.display.set_caption("Monkey Fever")
    pg.mouse.set_visible(False)

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    # Put Text On The Background, Centered
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Pummel The Chimp, And Win $$$", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Prepare Game Objects
    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    chimp = Chimp()
    fist = Fist()
    allsprites = pg.sprite.RenderPlain((chimp, fist))
    clock = pg.time.Clock()

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == pg.MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    pg.quit()


def main():
    pg.init()
    pg.display.set_caption("Cursors Example")

    pg.font.init()
    font = pg.font.Font(None, 30)
    font1 = pg.font.Font(None, 24)

    bg = pg.display.set_mode((500, 400))
    bg.fill((183, 201, 226))

    # Initialize circles
    radius1 = 40
    radius2 = 40
    radius3 = 40
    radius4 = 40
    radius5 = 40
    radius6 = 40
    radius7 = 40

    pos_x1 = 82
    pos_x2 = 138
    pos_x3 = 194
    pos_x4 = 250
    pos_x5 = 306
    pos_x6 = 362
    pos_x7 = 418

    pos_y1 = 140
    pos_y2 = 220
    pos_y3 = 140
    pos_y4 = 220
    pos_y5 = 140
    pos_y6 = 220
    pos_y7 = 140

    circle1 = pg.draw.circle(bg, (255, 255, 255), (pos_x1, pos_y1), radius1)
    circle2 = pg.draw.circle(bg, (255, 255, 255), (pos_x2, pos_y2), radius2)
    circle3 = pg.draw.circle(bg, (255, 255, 255), (pos_x3, pos_y3), radius3)
    circle4 = pg.draw.circle(bg, (255, 255, 255), (pos_x4, pos_y4), radius4)
    circle5 = pg.draw.circle(bg, (255, 255, 255), (pos_x5, pos_y5), radius5)
    circle6 = pg.draw.circle(bg, (255, 255, 255), (pos_x6, pos_y6), radius6)
    circle7 = pg.draw.circle(bg, (255, 255, 255), (pos_x7, pos_y7), radius7)

    # Initialize button
    button_text = font1.render("Click here to change cursor", True, (0, 0, 0))
    button = pg.draw.rect(
        bg,
        (180, 180, 180),
        (139, 300, button_text.get_width() + 5, button_text.get_height() + 50),
    )
    button_text_rect = button_text.get_rect(center=button.center)
    bg.blit(button_text, button_text_rect)

    pg.display.update()

    cursors = [
        system_cursor1,
        color_cursor,
        system_cursor2,
        image_cursor,
        system_cursor3,
        bitmap_cursor1,
        bitmap_cursor2,
    ]

    index = 0
    pg.mouse.set_cursor(cursors[index])

    pressed = False
    clock = pg.time.Clock()

    while True:
        clock.tick(50)

        mouse_x, mouse_y = pg.mouse.get_pos()

        # Check if mouse is inside a circle to change its color
        if check_circle(mouse_x, mouse_y, circle1.centerx, circle1.centery, radius1):
            circle1 = pg.draw.circle(bg, (255, 0, 0), (pos_x1, pos_y1), radius1)
        else:
            circle1 = pg.draw.circle(bg, (255, 255, 255), (pos_x1, pos_y1), radius1)

        if check_circle(mouse_x, mouse_y, circle2.centerx, circle2.centery, radius2):
            circle2 = pg.draw.circle(bg, (255, 127, 0), (pos_x2, pos_y2), radius2)
        else:
            circle2 = pg.draw.circle(bg, (255, 255, 255), (pos_x2, pos_y2), radius2)

        if check_circle(mouse_x, mouse_y, circle3.centerx, circle3.centery, radius3):
            circle3 = pg.draw.circle(bg, (255, 255, 0), (pos_x3, pos_y3), radius3)
        else:
            circle3 = pg.draw.circle(bg, (255, 255, 255), (pos_x3, pos_y3), radius3)

        if check_circle(mouse_x, mouse_y, circle4.centerx, circle4.centery, radius3):
            circle4 = pg.draw.circle(bg, (0, 255, 0), (pos_x4, pos_y4), radius4)
        else:
            circle4 = pg.draw.circle(bg, (255, 255, 255), (pos_x4, pos_y4), radius4)

        if check_circle(mouse_x, mouse_y, circle5.centerx, circle5.centery, radius4):
            circle5 = pg.draw.circle(bg, (0, 0, 255), (pos_x5, pos_y5), radius5)
        else:
            circle5 = pg.draw.circle(bg, (255, 255, 255), (pos_x5, pos_y5), radius5)

        if check_circle(mouse_x, mouse_y, circle6.centerx, circle6.centery, radius6):
            circle6 = pg.draw.circle(bg, (75, 0, 130), (pos_x6, pos_y6), radius6)
        else:
            circle6 = pg.draw.circle(bg, (255, 255, 255), (pos_x6, pos_y6), radius6)

        if check_circle(mouse_x, mouse_y, circle7.centerx, circle7.centery, radius7):
            circle7 = pg.draw.circle(bg, (148, 0, 211), (pos_x7, pos_y7), radius7)
        else:
            circle7 = pg.draw.circle(bg, (255, 255, 255), (pos_x7, pos_y7), radius7)

        bg.fill((183, 201, 226), (0, 15, bg.get_width(), 50))
        text1 = font.render(
            (f"This is a {pg.mouse.get_cursor().type} cursor"), True, (0, 0, 0)
        )
        text_rect1 = text1.get_rect(center=(bg.get_width() / 2, 40))
        bg.blit(text1, text_rect1)

        button = pg.draw.rect(
            bg,
            (100, 149, 240),
            (139, 300, button_text.get_width() + 5, button_text.get_height() + 50),
        )
        bg.blit(button_text, button_text_rect)

        # Check if button was clicked and change cursor
        if button.collidepoint(mouse_x, mouse_y):
            button = pg.draw.rect(
                bg,
                (60, 100, 255),
                (
                    139,
                    300,
                    button_text.get_width() + 5,
                    button_text.get_height() + 50,
                ),
            )
            bg.blit(button_text, button_text_rect)

            if pg.mouse.get_pressed()[0] == 1 and pressed is False:
                button = pg.draw.rect(
                    bg,
                    (0, 0, 139),
                    (
                        139,
                        300,
                        button_text.get_width() + 5,
                        button_text.get_height() + 50,
                    ),
                )
                bg.blit(button_text, button_text_rect)
                index += 1
                index %= len(cursors)
                pg.mouse.set_cursor(cursors[index])
                pg.display.update()
                pg.time.delay(40)

        if pg.mouse.get_pressed()[0] == 1:
            pressed = True
        elif pg.mouse.get_pressed()[0] == 0:
            pressed = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        pg.display.update()


def main():
    pg.init()

    going = True
    surf = pg.display.set_mode((640, 480))
    font = pg.font.SysFont("Arial", 24)
    clock = pg.time.Clock()

    spr_file_text = font.render("Drag and drop a file or image!", 1, (255, 255, 255))
    spr_file_text_rect = spr_file_text.get_rect()
    spr_file_text_rect.center = surf.get_rect().center

    spr_file_image = None
    spr_file_image_rect = None

    while going:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                going = False
            elif ev.type == pg.DROPBEGIN:
                print(ev)
                print("File drop begin!")
            elif ev.type == pg.DROPCOMPLETE:
                print(ev)
                print("File drop complete!")
            elif ev.type == pg.DROPTEXT:
                print(ev)
                spr_file_text = font.render(ev.text, 1, (255, 255, 255))
                spr_file_text_rect = spr_file_text.get_rect()
                spr_file_text_rect.center = surf.get_rect().center
            elif ev.type == pg.DROPFILE:
                print(ev)
                spr_file_text = font.render(ev.file, 1, (255, 255, 255))
                spr_file_text_rect = spr_file_text.get_rect()
                spr_file_text_rect.center = surf.get_rect().center

                # Try to open the file if it's an image
                filetype = ev.file[-3:]
                if filetype in ["png", "bmp", "jpg"]:
                    spr_file_image = pg.image.load(ev.file).convert()
                    spr_file_image.set_alpha(127)
                    spr_file_image_rect = spr_file_image.get_rect()
                    spr_file_image_rect.center = surf.get_rect().center

        surf.fill((0, 0, 0))
        surf.blit(spr_file_text, spr_file_text_rect)
        if spr_file_image and spr_file_image_rect is not None:
            surf.blit(spr_file_image, spr_file_image_rect)

        pg.display.flip()
        clock.tick(30)

    pg.quit()


def main():
    pg.init()
    pygame._sdl2.controller.init()

    print(usage)

    win = pg.display.set_mode((640, 480), pg.RESIZABLE)
    pg.display.set_caption("Mouse Focus Workout. h key for help")

    global font
    font = pg.font.Font(None, 26)

    global img_on_off
    img_on_off.append(font.render("Off", 1, (0, 0, 0), (255, 50, 50)))
    img_on_off.append(font.render("On", 1, (0, 0, 0), (50, 255, 50)))

    # stores surfaces of text representing what has gone through the event queue
    history = []

    # let's turn on the joysticks just so we can play with em
    for x in range(pg.joystick.get_count()):
        if pygame._sdl2.controller.is_controller(x):
            c = pygame._sdl2.controller.Controller(x)
            txt = "Enabled controller: " + c.name
        else:
            j = pg.joystick.Joystick(x)
            txt = "Enabled joystick: " + j.get_name()

        img = font.render(txt, 1, (50, 200, 50), (0, 0, 0))
        history.append(img)
    if not pg.joystick.get_count():
        img = font.render("No Joysticks to Initialize", 1, (50, 200, 50), (0, 0, 0))
        history.append(img)

    going = True
    while going:
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    going = False
                else:
                    global last_key
                    last_key = e.key
                if e.key == pg.K_h:
                    draw_usage_in_history(history, usage)
                if e.key == pg.K_c:
                    current_state = pygame._sdl2.controller.get_eventstate()
                    pygame._sdl2.controller.set_eventstate(not current_state)

            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                pg.event.set_grab(not pg.event.get_grab())

            if e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
                pg.mouse.set_visible(not pg.mouse.get_visible())

            if e.type != pg.MOUSEMOTION:
                txt = f"{pg.event.event_name(e.type)}: {e.dict}"
                img = font.render(txt, 1, (50, 200, 50), (0, 0, 0))
                history.append(img)
                history = history[-13:]

            if e.type == pg.VIDEORESIZE:
                win = pg.display.set_mode(e.size, pg.RESIZABLE)

            if e.type == pg.QUIT:
                going = False

        drawstatus(win)
        drawhistory(win, history)

        pg.display.flip()
        pg.time.wait(10)

    pg.quit()
    raise SystemExit


def main():
    # initialize
    pg.init()
    resolution = 400, 200
    screen = pg.display.set_mode(resolution)

    ##    pg.mouse.set_cursor(*pg.cursors.diamond)

    fg = 250, 240, 230
    bg = 5, 5, 5
    wincolor = 40, 40, 90

    # fill background
    screen.fill(wincolor)

    # load font, prepare values
    font = pg.font.Font(None, 80)
    text = "Fonty"
    size = font.size(text)

    # no AA, no transparency, normal
    ren = font.render(text, 0, fg, bg)
    screen.blit(ren, (10, 10))

    # no AA, transparency, underline
    font.set_underline(1)
    ren = font.render(text, 0, fg)
    screen.blit(ren, (10, 40 + size[1]))
    font.set_underline(0)

    a_sys_font = pg.font.SysFont("Arial", 60)

    # AA, no transparency, bold
    a_sys_font.set_bold(1)
    ren = a_sys_font.render(text, 1, fg, bg)
    screen.blit(ren, (30 + size[0], 10))
    a_sys_font.set_bold(0)

    # AA, transparency, italic
    a_sys_font.set_italic(1)
    ren = a_sys_font.render(text, 1, fg)
    screen.blit(ren, (30 + size[0], 40 + size[1]))
    a_sys_font.set_italic(0)

    # Get some metrics.
    print(f"Font metrics for 'Fonty':  {a_sys_font.metrics(text)}")
    ch = "\u3060"
    msg = f"Font metrics for '{ch}':  {a_sys_font.metrics(ch)}"
    print(msg)

    ## #some_japanese_unicode = u"\u304b\u3070\u306b"
    ##some_japanese_unicode = unicode_('%c%c%c') % (0x304b, 0x3070, 0x306b)

    # AA, transparency, italic
    ##ren = a_sys_font.render(some_japanese_unicode, 1, fg)
    ##screen.blit(ren, (30 + size[0], 40 + size[1]))

    # show the surface and await user quit
    pg.display.flip()
    while True:
        # use event.wait to keep from polling 100% cpu
        if pg.event.wait().type in (pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
            break
    pg.quit()


def main():
    """run the demo"""

    # initialize pygame and setup an opengl display
    pg.init()

    gl_version = (3, 0)  # GL Version number (Major, Minor)
    if USE_MODERN_GL:
        gl_version = (3, 2)  # GL Version number (Major, Minor)

        # By setting these attributes we can choose which Open GL Profile
        # to use, profiles greater than 3.2 use a different rendering path
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, gl_version[0])
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, gl_version[1])
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )

    fullscreen = False  # start in windowed mode

    display_size = (640, 480)
    pg.display.set_mode(display_size, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

    if USE_MODERN_GL:
        gpu, f_indices, o_indices = init_gl_modern(display_size)
        rotation = Rotation()
    else:
        init_gl_stuff_old()

    going = True
    while going:
        # check for quit'n events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                going = False

            elif event.type == pg.KEYDOWN and event.key == pg.K_f:
                if not fullscreen:
                    print("Changing to FULLSCREEN")
                    pg.display.set_mode(
                        (640, 480), pg.OPENGL | pg.DOUBLEBUF | pg.FULLSCREEN
                    )
                else:
                    print("Changing to windowed mode")
                    pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
                fullscreen = not fullscreen
                if gl_version[0] >= 4 or (gl_version[0] == 3 and gl_version[1] >= 2):
                    gpu, f_indices, o_indices = init_gl_modern(display_size)
                    rotation = Rotation()
                else:
                    init_gl_stuff_old()

        if USE_MODERN_GL:
            draw_cube_modern(gpu, f_indices, o_indices, rotation)
        else:
            # clear screen and move camera
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            # orbit camera around by 1 degree
            GL.glRotatef(1, 0, 1, 0)
            drawcube_old()

        pg.display.flip()
        pg.time.wait(10)

    pg.quit()


def main(fin, fout, w, h):
    """smoothscale image file named fin as fout with new size (w,h)"""
    scaleit(fin, fout, w, h)


def main():
    # Set the width and height of the screen (width, height), and name the window.
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Joystick example")

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Get ready to print.
    text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))
        text_print.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        text_print.tprint(screen, f"Number of joysticks: {joystick_count}")
        text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            text_print.tprint(screen, f"Joystick {jid}")
            text_print.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            text_print.tprint(screen, f"Joystick name: {name}")

            guid = joystick.get_guid()
            text_print.tprint(screen, f"GUID: {guid}")

            power_level = joystick.get_power_level()
            text_print.tprint(screen, f"Joystick's power level: {power_level}")

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            text_print.tprint(screen, f"Number of axes: {axes}")
            text_print.indent()

            for i in range(axes):
                axis = joystick.get_axis(i)
                text_print.tprint(screen, f"Axis {i} value: {axis:>6.3f}")
            text_print.unindent()

            buttons = joystick.get_numbuttons()
            text_print.tprint(screen, f"Number of buttons: {buttons}")
            text_print.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                text_print.tprint(screen, f"Button {i:>2} value: {button}")
            text_print.unindent()

            hats = joystick.get_numhats()
            text_print.tprint(screen, f"Number of hats: {hats}")
            text_print.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                text_print.tprint(screen, f"Hat {i} value: {str(hat)}")
            text_print.unindent()

            text_print.unindent()

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


def main():
    # initialize and setup screen
    pg.init()
    screen = pg.display.set_mode((640, 480), pg.HWSURFACE | pg.DOUBLEBUF)

    # load image and quadruple
    imagename = os.path.join(main_dir, "data", "liquid.bmp")
    bitmap = pg.image.load(imagename)
    bitmap = pg.transform.scale2x(bitmap)
    bitmap = pg.transform.scale2x(bitmap)

    # get the image and screen in the same format
    if screen.get_bitsize() == 8:
        screen.set_palette(bitmap.get_palette())
    else:
        bitmap = bitmap.convert()

    # prep some variables
    anim = 0.0

    # mainloop
    xblocks = range(0, 640, 20)
    yblocks = range(0, 480, 20)
    stopevents = pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN
    while True:
        for e in pg.event.get():
            if e.type in stopevents:
                return

        anim = anim + 0.02
        for x in xblocks:
            xpos = (x + (sin(anim + x * 0.01) * 15)) + 20
            for y in yblocks:
                ypos = (y + (sin(anim + y * 0.01) * 15)) + 20
                screen.blit(bitmap, (x, y), (xpos, ypos, 20, 20))

        pg.display.flip()
        time.sleep(0.01)


def main(*args):
    """
    Display multiple images bounce off each other using collision detection

    Positional arguments:
      one or more image file names.

    This pg.masks demo will display multiple moving sprites bouncing
    off each other. More than one sprite image can be provided.
    """

    if len(args) == 0:
        raise ValueError("Require at least one image file name: non given")
    pg.init()

    screen_size = (640, 480)
    screen = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()

    images = []
    masks = []
    for image_path in args:
        images.append(pg.image.load(image_path).convert_alpha())
        masks.append(pg.mask.from_surface(images[-1]))

    sprites = []
    for i in range(20):
        j = i % len(images)
        sprite = Sprite(
            pos=(
                random.uniform(0, screen_size[0]),
                random.uniform(0, screen_size[1]),
            ),
            vel=(
                random.uniform(-5, 5),
                random.uniform(-5, 5),
            ),
            surface=images[j],
            mask=masks[j],
        )
        sprites.append(sprite)

    while True:
        for event in pg.event.get():
            if event.type in (pg.QUIT, pg.KEYDOWN):
                return

        screen.fill((240, 220, 100))

        for sprite_index, sprite in enumerate(sprites):
            for other_sprite in sprites[sprite_index + 1 :]:
                sprite.collide(other_sprite)

            sprite.update()

            # If the sprite is outside of the screen on the left
            if sprite.pos.x < -sprite.width:
                sprite.pos.x = screen_size[0]
            # right
            elif sprite.pos.x > screen_size[0]:
                sprite.pos.x = -sprite.width
            # top
            if sprite.pos.y < -sprite.height:
                sprite.pos.y = screen_size[1]
            # down
            elif sprite.pos.y > screen_size[1]:
                sprite.pos.y = -sprite.height

            screen.blit(sprite.surface, sprite.pos)

        clock.tick(30)
        pg.display.flip()


def main(mode="output", device_id=None):
    """Run a Midi example

    Arguments:
    mode - if 'output' run a midi keyboard output example
              'input' run a midi event logger input example
              'list' list available midi devices
           (default 'output')
    device_id - midi device number; if None then use the default midi input or
                output device for the system

    """

    if mode == "input":
        input_main(device_id)
    elif mode == "output":
        output_main(device_id)
    elif mode == "list":
        print_device_info()
    else:
        raise ValueError(f"Unknown mode option '{mode}'")


def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    player = load_image("player1.gif")
    entity = load_image("alien1.gif")
    background = load_image("liquid.bmp")

    # scale the background image so that it fills the window and
    # successfully overwrites the old sprite position.
    background = pg.transform.scale2x(background)
    background = pg.transform.scale2x(background)

    screen.blit(background, (0, 0))

    objects = []
    p = GameObject(player, 10, 3)
    for x in range(10):
        o = GameObject(entity, x * 40, x)
        objects.append(o)

    pg.display.set_caption("Move It!")

    # This is a simple event handler that enables player input.
    while True:
        # Get all keys currently pressed, and move when an arrow key is held.
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            p.move(up=True)
        if keys[pg.K_DOWN]:
            p.move(down=True)
        if keys[pg.K_LEFT]:
            p.move(left=True)
        if keys[pg.K_RIGHT]:
            p.move(right=True)

        # Draw the background
        screen.blit(background, (0, 0))
        for e in pg.event.get():
            # quit upon screen exit
            if e.type == pg.QUIT:
                return
        for o in objects:
            screen.blit(background, o.pos, o.pos)
        for o in objects:
            o.move(right=True)
            screen.blit(o.image, o.pos)
        screen.blit(p.image, p.pos)
        clock.tick(60)
        pg.display.update()
        pg.time.delay(100)


def main():
    global font  # this will be used by the draw_text_line function
    global volume, starting_pos
    running = True
    paused = False

    # we will be polling for key up and key down events
    # users should be able to change the volume by holding the up and down arrows
    # the change_volume variable will be set by key down events and cleared by key up events
    change_volume = 0

    pg.init()
    pg.display.set_mode((640, 480))
    font = pg.font.SysFont("Arial", 24)
    clock = pg.time.Clock()

    pg.scrap.init()
    pg.SCRAP_TEXT = pg.scrap.get_types()[0]  # TODO remove when scrap module is fixed
    scrap_get = pg.scrap.get(pg.SCRAP_TEXT)
    clipped = "" if scrap_get is None else scrap_get.decode("UTF-8")
    # store the current text from the clipboard TODO remove decode

    # add the command line arguments to the  music_file_list
    for arg in sys.argv[1:]:
        add_file(arg)
    play_file("house_lo.ogg")  # play default music included with pygame

    # draw instructions on screen
    y = draw_text_line("Drop music files or path names onto this window", 20)
    y = draw_text_line("Copy file names into the clipboard", y)
    y = draw_text_line("Or feed them from the command line", y)
    y = draw_text_line("If it's music it will play!", y)
    y = draw_text_line("SPACE to pause or UP/DOWN to change volume", y)
    y = draw_text_line("LEFT and RIGHT will skip around the track", y)
    draw_text_line("Other keys will start the next track", y)

    """
    This is the main loop
    It will respond to drag and drop, clipboard changes, and key presses
    """
    while running:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False
            elif ev.type == pg.DROPTEXT:
                play_file(ev.text)
            elif ev.type == pg.DROPFILE:
                play_file(ev.file)
            elif ev.type == MUSIC_DONE:
                play_next()
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    running = False  # exit loop
                elif ev.key in (pg.K_SPACE, pg.K_RETURN):
                    if paused:
                        pg.mixer.music.unpause()
                        paused = False
                    else:
                        pg.mixer.music.pause()
                        paused = True
                elif ev.key == pg.K_UP:
                    change_volume = VOLUME_CHANGE_AMOUNT
                elif ev.key == pg.K_DOWN:
                    change_volume = -VOLUME_CHANGE_AMOUNT
                elif ev.key == pg.K_RIGHT:
                    change_music_position(+5)
                elif ev.key == pg.K_LEFT:
                    change_music_position(-5)

                else:
                    play_next()

            elif ev.type == pg.KEYUP:
                if ev.key in (pg.K_UP, pg.K_DOWN):
                    change_volume = 0

        # is the user holding up or down?
        if change_volume:
            volume += change_volume
            volume = min(max(0, volume), 1)  # volume should be between 0 and 1
            pg.mixer.music.set_volume(volume)
            print("volume:", volume)

        # TODO remove decode when SDL2 scrap is fixed
        scrap_get = pg.scrap.get(pg.SCRAP_TEXT)
        new_text = "" if scrap_get is None else scrap_get.decode("UTF-8")

        if new_text != clipped:  # has the clipboard changed?
            clipped = new_text
            play_file(clipped)  # try to play the file if it has

        pg.display.flip()
        clock.tick(9)  # keep CPU use down by updating screen less often

    pg.quit()


def main():
    pg.init()

    pg.display.set_mode((255, 255))
    surface = pg.Surface((255, 255))

    pg.display.flip()

    # Create the PixelArray.
    ar = pg.PixelArray(surface)

    # Do some easy gradient effect.
    for y in range(255):
        r, g, b = y, y, y
        ar[:, y] = (r, g, b)
    del ar
    show(surface)

    # We have made some gradient effect, now flip it.
    ar = pg.PixelArray(surface)
    ar[:] = ar[:, ::-1]
    del ar
    show(surface)

    # Every second column will be made blue
    ar = pg.PixelArray(surface)
    ar[::2] = (0, 0, 255)
    del ar
    show(surface)

    # Every second row will be made green
    ar = pg.PixelArray(surface)
    ar[:, ::2] = (0, 255, 0)
    del ar
    show(surface)

    # Manipulate the image. Flip it around the y axis.
    surface = pg.image.load(os.path.join(data_dir, "arraydemo.bmp"))
    ar = pg.PixelArray(surface)
    ar[:] = ar[:, ::-1]
    del ar
    show(surface)

    # Flip the image around the x axis.
    ar = pg.PixelArray(surface)
    ar[:] = ar[::-1, :]
    del ar
    show(surface)

    # Every second column will be made white.
    ar = pg.PixelArray(surface)
    ar[::2] = (255, 255, 255)
    del ar
    show(surface)

    # Flip the image around both axes, restoring its original layout.
    ar = pg.PixelArray(surface)
    ar[:] = ar[::-1, ::-1]
    del ar
    show(surface)

    # Rotate 90 degrees clockwise.
    w, h = surface.get_size()
    surface2 = pg.Surface((h, w), surface.get_flags(), surface)
    ar = pg.PixelArray(surface)
    ar2 = pg.PixelArray(surface2)
    ar2[...] = ar.transpose()[::-1, :]
    del ar, ar2
    show(surface2)

    # Scale it by throwing each second pixel away.
    surface = pg.image.load(os.path.join(data_dir, "arraydemo.bmp"))
    ar = pg.PixelArray(surface)
    sf2 = ar[::2, ::2].make_surface()
    del ar
    show(sf2)

    # Replace anything looking like the blue color from the text.
    ar = pg.PixelArray(surface)
    ar.replace((60, 60, 255), (0, 255, 0), 0.06)
    del ar
    show(surface)

    # Extract anything which might be somewhat black.
    surface = pg.image.load(os.path.join(data_dir, "arraydemo.bmp"))
    ar = pg.PixelArray(surface)
    ar2 = ar.extract((0, 0, 0), 0.07)
    sf2 = ar2.surface
    del ar, ar2
    show(sf2)

    # Compare two images.
    surface = pg.image.load(os.path.join(data_dir, "alien1.gif"))
    surface2 = pg.image.load(os.path.join(data_dir, "alien2.gif"))
    ar1 = pg.PixelArray(surface)
    ar2 = pg.PixelArray(surface2)
    ar3 = ar1.compare(ar2, 0.07)
    sf3 = ar3.surface
    del ar1, ar2, ar3
    show(sf3)


def main(file_path):
    """Play an audio file with pg.mixer.music"""

    with Window(file_path) as win:
        win.write_lines("Loading ...", -1)
        pg.mixer.init(frequency=44100)
        try:
            paused = False
            pg.mixer.music.load(file_path)

            # Make sure the event loop ticks over at least every 0.5 seconds.
            pg.time.set_timer(pg.USEREVENT, 500)

            pg.mixer.music.play()
            win.write_lines("Playing ...\n", -1)

            while pg.mixer.music.get_busy() or paused:
                e = pg.event.wait()
                if e.type == pg.KEYDOWN:
                    key = e.key
                    if key == pg.K_SPACE:
                        if paused:
                            pg.mixer.music.unpause()
                            paused = False
                            win.write_lines("Playing ...\n", -1)
                        else:
                            pg.mixer.music.pause()
                            paused = True
                            win.write_lines("Paused ...\n", -1)
                    elif key == pg.K_r:
                        if file_path[-3:].lower() in ("ogg", "mp3", "mod"):
                            status = "Rewound."
                            pg.mixer.music.rewind()
                        else:
                            status = "Restarted."
                            pg.mixer.music.play()
                        if paused:
                            pg.mixer.music.pause()
                            win.write_lines(status, -1)
                    elif key == pg.K_f:
                        win.write_lines("Fading out ...\n", -1)
                        pg.mixer.music.fadeout(5000)
                        # when finished get_busy() will return False.
                    elif key in [pg.K_q, pg.K_ESCAPE]:
                        paused = False
                        pg.mixer.music.stop()
                        # get_busy() will now return False.
                elif e.type == pg.QUIT:
                    paused = False
                    pg.mixer.music.stop()
                    # get_busy() will now return False.
            pg.time.set_timer(pg.USEREVENT, 0)
        finally:
            pg.mixer.quit()
    pg.quit()


def main(imagefile, convert_alpha=False, run_speed_test=False):
    """show an interactive image scaler

    Args:
        imagefile - name of source image (required)
        convert_alpha - use convert_alpha() on the surf (default False)
        run_speed_test - (default False)
    """

    # initialize display
    pg.display.init()
    # load background image
    background = pg.image.load(imagefile)

    if run_speed_test:
        if convert_alpha:
            # convert_alpha() requires the display mode to be set
            pg.display.set_mode((1, 1))
            background = background.convert_alpha()

        SpeedTest(background)
        return

    # start fullscreen mode
    screen = pg.display.set_mode((1024, 768), pg.FULLSCREEN)
    if convert_alpha:
        background = background.convert_alpha()

    # turn off the mouse pointer
    pg.mouse.set_visible(0)
    # main loop
    bRunning = True
    bUp = False
    bDown = False
    bLeft = False
    bRight = False
    cursize = [background.get_width(), background.get_height()]
    while bRunning:
        image = pg.transform.smoothscale(background, cursize)
        imgpos = image.get_rect(centerx=512, centery=384)
        screen.fill((255, 255, 255))
        screen.blit(image, imgpos)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                bRunning = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    bUp = True
                if event.key == pg.K_DOWN:
                    bDown = True
                if event.key == pg.K_LEFT:
                    bLeft = True
                if event.key == pg.K_RIGHT:
                    bRight = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    bUp = False
                if event.key == pg.K_DOWN:
                    bDown = False
                if event.key == pg.K_LEFT:
                    bLeft = False
                if event.key == pg.K_RIGHT:
                    bRight = False
        if bUp:
            cursize[1] -= 2
            if cursize[1] < 1:
                cursize[1] = 1
        if bDown:
            cursize[1] += 2
        if bLeft:
            cursize[0] -= 2
            if cursize[0] < 1:
                cursize[0] = 1
        if bRight:
            cursize[0] += 2
    pg.quit()


def main(image_file=None):
    if image_file is None:
        image_file = os.path.join(main_dir, "data", "arraydemo.bmp")
    margin = 80
    view_size = (30, 20)
    zoom_view_size = (view_size[0] * zoom_factor, view_size[1] * zoom_factor)
    win_size = (zoom_view_size[0] + 2 * margin, zoom_view_size[1] + 2 * margin)
    background_color = pg.Color("beige")

    pg.init()
    pg.display.set_caption("Scroll Example")

    # set up key repeating so we can hold down the key to scroll.
    old_k_delay, old_k_interval = pg.key.get_repeat()
    pg.key.set_repeat(500, 30)

    try:
        screen = pg.display.set_mode(win_size)
        screen.fill(background_color)
        pg.display.flip()

        image = pg.image.load(image_file).convert()
        image_w, image_h = image.get_size()

        if image_w < view_size[0] or image_h < view_size[1]:
            print("The source image is too small for this example.")
            print("A %i by %i or larger image is required." % zoom_view_size)
            return

        regions = pg.Surface(win_size, 0, 24)
        add_arrow_button(screen, regions, (40, win_size[1] // 2), DIR_LEFT)
        add_arrow_button(
            screen, regions, (win_size[0] - 40, win_size[1] // 2), DIR_RIGHT
        )
        add_arrow_button(screen, regions, (win_size[0] // 2, 40), DIR_UP)
        add_arrow_button(
            screen, regions, (win_size[0] // 2, win_size[1] - 40), DIR_DOWN
        )
        pg.display.flip()

        screen.set_clip((margin, margin, zoom_view_size[0], zoom_view_size[1]))

        view_rect = pg.Rect(0, 0, view_size[0], view_size[1])

        scale(
            image.subsurface(view_rect),
            zoom_view_size,
            screen.subsurface(screen.get_clip()),
        )
        pg.display.flip()

        # the direction we will scroll in.
        direction = None

        clock = pg.time.Clock()
        clock.tick()

        going = True

        while going:
            # wait for events before doing anything.
            # events = [pg.event.wait()] + pg.event.get()
            events = pg.event.get()

            # During the loop, if a key is held, scroll the view.
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                scroll_view(screen, image, DIR_UP, view_rect)
            if keys[pg.K_DOWN]:
                scroll_view(screen, image, DIR_DOWN, view_rect)
            if keys[pg.K_LEFT]:
                scroll_view(screen, image, DIR_LEFT, view_rect)
            if keys[pg.K_RIGHT]:
                scroll_view(screen, image, DIR_RIGHT, view_rect)

            for e in events:
                # quit if the event is quit.
                if e.type == pg.QUIT:
                    going = False

                # handle mouse button presses on arrows.
                elif e.type == pg.MOUSEBUTTONDOWN:
                    direction = regions.get_at(e.pos)[0]

                elif e.type == pg.MOUSEBUTTONUP:
                    direction = None

            if direction:
                scroll_view(screen, image, direction, view_rect)
            clock.tick(30)

    finally:
        pg.key.set_repeat(old_k_delay, old_k_interval)
        pg.quit()


def main(file_path=None):
    """Play an audio file as a buffered sound sample

    :param str file_path: audio file (default data/secosmic_low.wav)
    """
    # choose a desired audio format
    pg.mixer.init(11025)  # raises exception on fail

    # load the sound
    sound = pg.mixer.Sound(file_path)

    # start playing
    print("Playing Sound...")
    channel = sound.play()

    # poll until finished
    while channel.get_busy():  # still playing
        print("  ...still going...")
        pg.time.wait(1000)
    print("...Finished")
    pg.quit()


def main():
    """play various sndarray effects"""

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    print(f"mixer.get_init {pg.mixer.get_init()}")

    samples_per_second = pg.mixer.get_init()[0]

    print(("-" * 30) + "\n")
    print("loading sound")
    sound = pg.mixer.Sound(os.path.join(main_dir, "data", "car_door.wav"))

    print("-" * 30)
    print("start positions")
    print("-" * 30)

    start_pos = 0.1
    sound2 = sound_from_pos(sound, start_pos, samples_per_second)

    print(f"sound.get_length {sound.get_length()}")
    print(f"sound2.get_length {sound2.get_length()}")
    sound2.play()
    while pg.mixer.get_busy():
        pg.time.wait(200)

    print("waiting 2 seconds")
    pg.time.wait(2000)
    print("playing original sound")

    sound.play()
    while pg.mixer.get_busy():
        pg.time.wait(200)

    print("waiting 2 seconds")
    pg.time.wait(2000)

    # if 0:
    #    #TODO: this is broken.
    #    print(("-" * 30) + "\n")
    #    print("Slow down the original sound.")
    #    rate = 0.2
    #    slowed_sound = slow_down_sound(sound, rate)
    #    slowed_sound.play()
    #    while pg.mixer.get_busy():
    #        pg.time.wait(200)

    print("-" * 30)
    print("echoing")
    print("-" * 30)

    t1 = time.time()
    sound2 = make_echo(sound, samples_per_second)
    print("time to make echo %i" % (time.time() - t1,))

    print("original sound")
    sound.play()
    while pg.mixer.get_busy():
        pg.time.wait(200)

    print("echoed sound")
    sound2.play()
    while pg.mixer.get_busy():
        pg.time.wait(200)

    sound = pg.mixer.Sound(os.path.join(main_dir, "data", "secosmic_lo.wav"))

    t1 = time.time()
    sound3 = make_echo(sound, samples_per_second)
    print("time to make echo %i" % (time.time() - t1,))

    print("original sound")
    sound.play()
    while pg.mixer.get_busy():
        pg.time.wait(200)

    print("echoed sound")
    sound3.play()
    while pg.mixer.get_busy():
        pg.time.wait(200)

    pg.quit()


def main():
    "This is the starfield code"
    # create our starfield
    stars = initialize_stars()

    # initialize and prepare screen
    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    pg.display.set_caption("pygame Stars Example")
    white = 255, 240, 200
    black = 20, 20, 40
    screen.fill(black)

    clock = pg.time.Clock()

    # main game loop
    done = 0
    while not done:
        draw_stars(screen, stars, black)
        move_stars(stars)
        draw_stars(screen, stars, white)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                WINCENTER[:] = list(e.pos)
        clock.tick(50)
    pg.quit()


def main(
    update_rects=True,
    use_static=False,
    use_layered_dirty=False,
    screen_dims=(640, 480),
    use_alpha=False,
    flags=0,
):
    """Show lots of sprites moving around

    Optional keyword arguments:
    update_rects - use the RenderUpdate sprite group class (default True)
    use_static - include non-moving images (default False)
    use_layered_dirty - Use the FastRenderGroup sprite group (default False)
    screen_dims - Pygame window dimensions (default [640, 480])
    use_alpha - use alpha blending (default False)
    flags - additional display mode flags (default no additional flags)

    """

    if use_layered_dirty:
        update_rects = True

    pg.init()  # needed to initialise time module for get_ticks()
    pg.display.init()

    # if "-fast" in sys.argv:

    screen = pg.display.set_mode(screen_dims, flags, vsync="-vsync" in sys.argv)

    # this is mainly for GP2X, so it can quit.
    pg.joystick.init()
    num_joysticks = pg.joystick.get_count()
    if num_joysticks > 0:
        stick = pg.joystick.Joystick(0)
        stick.init()  # now we will receive events for the joystick

    screen.fill([0, 0, 0])
    pg.display.flip()
    sprite_surface = pg.image.load(os.path.join(data_dir, "asprite.bmp"))
    sprite_surface2 = pg.image.load(os.path.join(data_dir, "static.png"))

    if use_rle:
        sprite_surface.set_colorkey([0xFF, 0xFF, 0xFF], pg.SRCCOLORKEY | pg.RLEACCEL)
        sprite_surface2.set_colorkey([0xFF, 0xFF, 0xFF], pg.SRCCOLORKEY | pg.RLEACCEL)
    else:
        sprite_surface.set_colorkey([0xFF, 0xFF, 0xFF], pg.SRCCOLORKEY)
        sprite_surface2.set_colorkey([0xFF, 0xFF, 0xFF], pg.SRCCOLORKEY)

    if use_alpha:
        sprite_surface = sprite_surface.convert_alpha()
        sprite_surface2 = sprite_surface2.convert_alpha()
    else:
        sprite_surface = sprite_surface.convert()
        sprite_surface2 = sprite_surface2.convert()

    Thingy.images = [sprite_surface]
    if use_static:
        Static.images = [sprite_surface2]

    if len(sys.argv) > 1:
        try:
            numsprites = int(sys.argv[-1])
        except Exception:
            numsprites = 100
    else:
        numsprites = 100
    sprites = None
    if use_layered_dirty:
        ##        sprites = pg.sprite.FastRenderGroup()
        sprites = pg.sprite.LayeredDirty()
    else:
        if update_rects:
            sprites = pg.sprite.RenderUpdates()
        else:
            sprites = pg.sprite.Group()

    for i in range(0, numsprites):
        if use_static and i % 2 == 0:
            sprites.add(Static())
        sprites.add(Thingy())

    frames = 0
    start = time()

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill([0, 0, 0])

    going = True
    while going:
        if not update_rects:
            screen.fill([0, 0, 0])

        ##        for sprite in sprites:
        ##            sprite.move()

        if update_rects:
            sprites.clear(screen, background)
        sprites.update()

        rects = sprites.draw(screen)
        if update_rects:
            pg.display.update(rects)
        else:
            pg.display.flip()

        for event in pg.event.get():
            if event.type in [pg.QUIT, pg.KEYDOWN, pg.QUIT, pg.JOYBUTTONDOWN]:
                going = False

        frames += 1
    end = time()
    print(f"FPS: {frames / (end - start):f}")
    pg.quit()


def main():
    game = Game("Text Input Example")
    game.main_loop()


def main():
    pg.init()
    pg.mixer.quit()  # remove ALSA underflow messages for Debian squeeze
    size = 600, 400
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    screen = pg.display.set_mode(size, pg.NOFRAME, 0)

    pg.event.set_blocked(pg.MOUSEMOTION)  # keep our queue cleaner
    pg.time.set_timer(pg.USEREVENT, 500)

    while True:
        event = pg.event.wait()
        if event.type in (pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
            break
        elif event.type == pg.USEREVENT:
            DisplayGradient(screen)

    pg.quit()


def main(args: list[str] | None = None) -> int:
    """This is preserved for old console scripts that may still be referencing
    it.

    For additional details, see https://github.com/pypa/pip/issues/7498.
    """
    from pip._internal.utils.entrypoints import _wrapper

    return _wrapper(args)


def main(args: list[str] | None = None) -> int:
    """This is preserved for old console scripts that may still be referencing
    it.

    For additional details, see https://github.com/pypa/pip/issues/7498.
    """
    from pip._internal.utils.entrypoints import _wrapper

    return _wrapper(args)


def main() -> None:
    args = get_args()
    sess = get_session()

    # Make a request to get a response
    resp = sess.get(args.url)

    # Turn on logging
    setup_logging()

    # try setting the cache
    cache_controller: CacheController = (
        sess.cache_controller  # type: ignore[attr-defined]
    )
    cache_controller.cache_response(resp.request, resp.raw)

    # Now try to get it
    if cache_controller.cached_request(resp.request):
        print("Cached!")
    else:
        print("Not cached :(")


def main() -> None:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    parser = argparse.ArgumentParser(description="OS distro info tool")
    parser.add_argument(
        "--json", "-j", help="Output in machine readable format", action="store_true"
    )

    parser.add_argument(
        "--root-dir",
        "-r",
        type=str,
        dest="root_dir",
        help="Path to the root filesystem directory (defaults to /)",
    )

    args = parser.parse_args()

    if args.root_dir:
        dist = LinuxDistribution(
            include_lsb=False,
            include_uname=False,
            include_oslevel=False,
            root_dir=args.root_dir,
        )
    else:
        dist = _distro

    if args.json:
        logger.info(json.dumps(dist.info(), indent=4, sort_keys=True))
    else:
        logger.info("Name: %s", dist.name(pretty=True))
        distribution_version = dist.version(pretty=True)
        logger.info("Version: %s", distribution_version)
        distribution_codename = dist.codename()
        logger.info("Codename: %s", distribution_codename)


def main() -> None:
    """Run the main entry point."""
    app_name = "MyApp"
    app_author = "MyCompany"

    print(f"-- platformdirs {__version__} --")  # noqa: T201

    print("-- app dirs (with optional 'version')")  # noqa: T201
    dirs = PlatformDirs(app_name, app_author, version="1.0")
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (without optional 'version')")  # noqa: T201
    dirs = PlatformDirs(app_name, app_author)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (without optional 'appauthor')")  # noqa: T201
    dirs = PlatformDirs(app_name)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201

    print("\n-- app dirs (with disabled 'appauthor')")  # noqa: T201
    dirs = PlatformDirs(app_name, appauthor=False)
    for prop in PROPS:
        print(f"{prop}: {getattr(dirs, prop)}")  # noqa: T201


def main():
    """Pretty-print the bug information as JSON."""
    print(json.dumps(info(), sort_keys=True, indent=2))


def main():
    if len(sys.argv) < 3:
        sys.exit("Needs args: hook_name, control_dir")
    hook_name = sys.argv[1]
    control_dir = sys.argv[2]
    if hook_name not in HOOK_NAMES:
        sys.exit("Unknown hook: %s" % hook_name)

    # Remove the parent directory from sys.path to avoid polluting the backend
    # import namespace with this directory.
    here = os.path.dirname(__file__)
    if here in sys.path:
        sys.path.remove(here)

    hook = globals()[hook_name]

    hook_input = read_json(pjoin(control_dir, "input.json"))

    json_out = {"unsupported": False, "return_val": None}
    try:
        json_out["return_val"] = hook(**hook_input["kwargs"])
    except BackendUnavailable as e:
        json_out["no_backend"] = True
        json_out["traceback"] = e.traceback
        json_out["backend_error"] = e.message
    except GotUnsupportedOperation as e:
        json_out["unsupported"] = True
        json_out["traceback"] = e.traceback
    except HookMissing as e:
        json_out["hook_missing"] = True
        json_out["missing_hook_name"] = e.hook_name or hook_name

    write_json(json_out, pjoin(control_dir, "output.json"), indent=2)


def main(args: list[str] | None = None) -> int:
    # NOTE: Lazy imports to speed up import of this module,
    # which is imported from the pip console script. This doesn't
    # speed up normal pip execution, but might be important in the future
    # if we use ``multiprocessing`` module,
    # which imports __main__ for each spawned subprocess.
    from pip._internal.cli.autocompletion import autocomplete
    from pip._internal.cli.main_parser import parse_command
    from pip._internal.commands import create_command
    from pip._internal.exceptions import PipError
    from pip._internal.utils import deprecation

    if args is None:
        args = sys.argv[1:]

    # Suppress the pkg_resources deprecation warning
    # Note - we use a module of .*pkg_resources to cover
    # the normal case (pip._vendor.pkg_resources) and the
    # devendored case (a bare pkg_resources)
    warnings.filterwarnings(
        action="ignore", category=DeprecationWarning, module=".*pkg_resources"
    )

    # Configure our deprecation warnings to be sent through loggers
    deprecation.install_warning_logger()

    autocomplete()

    try:
        cmd_name, cmd_args = parse_command(args)
    except PipError as exc:
        sys.stderr.write(f"ERROR: {exc}")
        sys.stderr.write(os.linesep)
        sys.exit(1)

    # Needed for locale.getpreferredencoding(False) to work
    # in pip._internal.utils.encoding.auto_decode
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error as e:
        # setlocale can apparently crash if locale are uninitialized
        logger.debug("Ignoring error %s when setting locale", e)
    command = create_command(cmd_name, isolated=("--isolated" in cmd_args))

    return command.main(cmd_args)


def main() -> None:
    import matplotlib.pyplot as plt

    p = TablePlotter()

    df1 = pd.DataFrame({"A": [10, 11, 12], "B": [20, 21, 22], "C": [30, 31, 32]})
    df2 = pd.DataFrame({"A": [10, 12], "C": [30, 32]})

    p.plot([df1, df2], pd.concat([df1, df2]), labels=["df1", "df2"], vertical=True)
    plt.show()

    df3 = pd.DataFrame({"X": [10, 12], "Z": [30, 32]})

    p.plot(
        [df1, df3], pd.concat([df1, df3], axis=1), labels=["df1", "df2"], vertical=False
    )
    plt.show()

    idx = pd.MultiIndex.from_tuples(
        [(1, "A"), (1, "B"), (1, "C"), (2, "A"), (2, "B"), (2, "C")]
    )
    column = pd.MultiIndex.from_tuples([(1, "A"), (1, "B")])
    df3 = pd.DataFrame({"v1": [1, 2, 3, 4, 5, 6], "v2": [5, 6, 7, 8, 9, 10]}, index=idx)
    df3.columns = column
    p.plot(df3, df3, labels=["df3"])
    plt.show()


def main(argv: list[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError(f'Too many command-line arguments: {argv[1:]}')

  logging.info('run_benchmarks.py started.')

  _init_jax_distributed()

  if _ENABLE_HLO_DUMP.value:
    _configure_hlo_dump(_OUTPUT_DIRECTORY.value)
  else:
    logging.info('HLO dump is disabled.')

  xla_flags = os.environ.get('XLA_FLAGS')
  if xla_flags:
    logging.info('XLA_FLAGS is set to: %s', xla_flags)
  else:
    logging.info('XLA_FLAGS is not set in environment.')

  jax.config.update('jax_enable_x64', True)
  logging.info('Set jax_enable_x64=True')

  if _GENERATE_FIXTURE.value:
    logging.info(
        'Generating fixture from %s into %s',
        _CONFIG_FILE.value,
        _OUTPUT_DIRECTORY.value,
    )
    _generate_fixture(_CONFIG_FILE.value, _OUTPUT_DIRECTORY.value)
    logging.info('Fixture generation complete.')
    return

  _run_benchmarks(
      _CONFIG_FILE.value,
      _OUTPUT_DIRECTORY.value,
      _LOCAL_DIRECTORY.value,
      remove_repeated_dir=_REMOVE_REPEATED_DIR.value,
  )

  logging.info('run_benchmarks.py finished.')


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  logging.info('run_benchmarks_pytorch.py started.')
  _init_torch_distributed()
  _run_benchmarks(
      _CONFIG_FILE.value,
      _OUTPUT_DIRECTORY.value,
      remove_repeated_dir=_REMOVE_REPEATED_DIR.value,
  )
  logging.info('run_benchmarks_pytorch.py finished.')


def main():
  """Loads test configurations and runs benchmarks."""
  config_path = 'orbax/checkpoint/_src/testing/oss/cloud_run_integration_tests.yaml'
  with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

  failures = 0
  for test in config.get('tests', []):
    if not run_benchmark(test):
      failures += 1

  if failures:
    print(f'{failures} benchmarks failed.')
    sys.exit(1)


def main():
  # 1. Parse arguments meant for launch.py
  parser = argparse.ArgumentParser(description="JAX Multihost Launcher")
  parser.add_argument(
      "--worker_mode", action="store_true", help=argparse.SUPPRESS
  )
  parser.add_argument(
      "--num_processes", type=int, default=2, help="Number of simulated hosts"
  )
  parser.add_argument(
      "--tpu_chips_per_process", type=int, default=4, help="TPU chips per host"
  )

  # `args` gets the launcher configs, `command` gets everything else
  args, command = parser.parse_known_args()

  # 2. WORKER MODE
  if args.worker_mode:
    if not command:
      raise ValueError("No command provided for the worker to execute.")
    run_worker_and_command(command)
    return

  # 3. LAUNCHER MODE
  if not command:
    logging.error(
        "Usage: python %s [LAUNCH_ARGS] <script.py> [SCRIPT_ARGS]",
        os.path.basename(__file__),
    )
    sys.exit(1)

  coordinator_port = find_free_port()
  coordinator_address = f"localhost:{coordinator_port}"

  slicebuilder_ports = [find_free_port() for _ in range(args.num_processes)]
  slicebuilder_addresses = ",".join(
      f"localhost:{port}" for port in slicebuilder_ports
  )

  logging.info(
      "🚀 Starting %s JAX processes (%s chips/process)...",
      args.num_processes,
      args.tpu_chips_per_process,
  )
  logging.info("📍 Coordinator: %s", coordinator_address)

  tpu_chips_per_process = args.tpu_chips_per_process
  num_tpu_chips = args.num_processes * args.tpu_chips_per_process
  if num_tpu_chips == 0:
    tpu_host_bounds = ""
    tpu_chips_per_host_bounds = ""
  elif num_tpu_chips == 1:
    assert tpu_chips_per_process == 1
    tpu_host_bounds = "1,1,1"
    tpu_chips_per_host_bounds = "1,1,1"
  elif num_tpu_chips == 4:
    if tpu_chips_per_process == 1:
      tpu_host_bounds = "2,2,1"
      tpu_chips_per_host_bounds = "1,1,1"
    elif tpu_chips_per_process == 2:
      tpu_host_bounds = "2,1,1"
      tpu_chips_per_host_bounds = "1,2,1"
    elif tpu_chips_per_process == 4:
      tpu_host_bounds = "1,1,1"
      tpu_chips_per_host_bounds = "2,2,1"
    else:
      raise ValueError(
          "Invalid number of TPU chips per worker {}".format(
              tpu_chips_per_process
          )
      )
  elif num_tpu_chips == 8:
    if tpu_chips_per_process == 1:
      tpu_host_bounds = "4,2,1"
      tpu_chips_per_host_bounds = "1,1,1"
    elif tpu_chips_per_process == 2:
      tpu_host_bounds = "2,2,1"
      tpu_chips_per_host_bounds = "1,2,1"
    elif tpu_chips_per_process == 4:
      # Note: this branch assumes we are using 2x4 v6e LitePod, and will not
      # work with 4x2 v5e LitePod.
      tpu_host_bounds = "1,2,1"
      tpu_chips_per_host_bounds = "2,2,1"
    elif tpu_chips_per_process == 8:
      tpu_host_bounds = "1,1,1"
      tpu_chips_per_host_bounds = "2,4,1"
    else:
      # TODO(phawkins): implement other cases.
      raise ValueError(
          "Invalid number of TPU chips per worker {}".format(
              tpu_chips_per_process
          )
      )
  else:
    raise ValueError(f"Invalid number of TPU chips {num_tpu_chips}")

  processes = []
  for rank in range(args.num_processes):
    env = os.environ.copy()

    # JAX Distributed Setup
    env["JAX_COORDINATOR_ADDRESS"] = coordinator_address
    env["JAX_NUM_PROCESSES"] = str(args.num_processes)
    env["JAX_PROCESS_ID"] = str(rank)

    device_ids = range(
        rank * args.tpu_chips_per_process,
        (rank + 1) * args.tpu_chips_per_process,
    )

    # Simulated TPU Setup
    env["CLOUD_TPU_TASK_ID"] = str(rank)
    env["TPU_CHIPS_PER_PROCESS_BOUNDS"] = tpu_chips_per_host_bounds
    env["TPU_PROCESS_BOUNDS"] = tpu_host_bounds
    env["TPU_PROCESS_ADDRESSES"] = slicebuilder_addresses
    env["TPU_PROCESS_PORT"] = str(slicebuilder_ports[rank])
    env["TPU_VISIBLE_CHIPS"] = ",".join(map(str, device_ids))
    env["ALLOW_MULTIPLE_LIBTPU_LOAD"] = "1"

    # Format the user's command to inject the current process rank where {rank}
    # is used
    worker_cmd = [c.format(rank=rank) for c in command]

    # Spawn THIS script again, triggering worker_mode
    cmd = [sys.executable, __file__, "--worker_mode"] + worker_cmd

    p = subprocess.Popen(cmd, env=env)
    processes.append(p)

  exit_codes = [p.wait() for p in processes]

  if any(c != 0 for c in exit_codes):
    logging.error("\n❌ Some processes failed.")
    sys.exit(1)
  else:
    logging.info("\n✅ All processes finished successfully.")


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  install_deps()

  try:
    with open(FLAGS.filename, 'r') as f:
      try:
        tests_by_process_count = yaml.safe_load(f)
      except yaml.YAMLError as e:
        logging.error('Failed to parse yaml file %s: %s', FLAGS.filename, e)
        sys.exit(1)
  except FileNotFoundError:
    logging.error('YAML file not found: %s', FLAGS.filename)
    sys.exit(1)

  key = f'processes:{FLAGS.processes}'
  if key not in tests_by_process_count:
    logging.error(
        'key=%s (from processes=%d) not found as a key in %s. Available'
        ' keys: %s',
        key,
        FLAGS.processes,
        FLAGS.filename,
        list(tests_by_process_count.keys()),
    )
    sys.exit(1)

  test_files = tests_by_process_count[key]
  if not test_files:
    logging.warning(
        'No test files found for processes=%d in %s.',
        FLAGS.processes,
        FLAGS.filename,
    )
    return

  results = {}
  failed_tests = []

  for test_file_yaml in test_files:
    test_path = _find_test_path(test_file_yaml)
    if test_path is None:
      results[test_file_yaml] = 'SKIPPED'
      logging.warning('Skipping %s: file not found.', test_file_yaml)
      continue

    logging.info('Running test: %s (found from %s)', test_path, test_file_yaml)
    try:
      _sync_op_id_generator(test_file_yaml)

      exit_code = pytest.main(['--import-mode=importlib', test_path])
      if exit_code == 0:
        results[test_file_yaml] = 'PASSED'
        logging.info('%s: PASSED', test_path)
      else:
        results[test_file_yaml] = 'FAILED'
        failed_tests.append(test_file_yaml)
        logging.error('%s: FAILED with exit code %s', test_path, exit_code)
    except Exception as e:  # Catching broad Exception to log any unexpected failure during pytest execution. # pylint: disable=broad-exception-caught
      results[test_file_yaml] = 'FAILED'
      failed_tests.append(test_file_yaml)
      logging.error('%s: FAILED with exception: %s', test_path, e)

  print('--- Test Summary ---')
  for test_file, status in results.items():
    print(f'{test_file}: {status}')
  print('--------------------')

  if failed_tests:
    logging.error('%d test(s) failed: %s', len(failed_tests), failed_tests)
    sys.exit(1)
  else:
    logging.info('All tests passed or skipped.')


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  # 1. Validation & Pre-flight
  cluster_exists = check_preconditions()

  # 2. Cluster Creation (if needed)
  if not cluster_exists:
    create_cluster()

  if _RAMDISK_DIRECTORY.value is not None:
    # Delete CSI driver before running any workloads, to delete any previous
    # checkpoint files.
    get_credentials()
    update_bucket_csi_driver(mount_csi_driver=False)
    # Mount CSI driver for the workload.
    update_bucket_csi_driver(mount_csi_driver=True)
    Console.print_success('Local bucket CSI driver mounted.')

  # 3. Preparation
  Console.print_step(2, 6, 'Preparing Workload')
  timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
  run_id = (
      f"{os.environ.get('USER', 'user')}-{timestamp}-{uuid.uuid4().hex[:6]}"
  )

  if _WORKLOAD_NAME.value is not None:
    workload_name_base = _WORKLOAD_NAME.value
  else:
    if _ENABLE_PATHWAYS.value:
      # XPK for pathways requires workload name < 25 chars.
      # Format: orbax-{timestamp}
      # timestamp (15) + orbax- (6) + separators (1) = 22 chars.
      workload_name_base = f'orbax-{timestamp}'.replace('_', '-').lower()
    else:
      base_name, _ = os.path.splitext(os.path.basename(_CONFIG_FILE.value))
      # XPK requires workload name < 40 chars.
      # Format: orbax-{base_name}-{timestamp}
      # timestamp (15) + orbax- (6) + separators (1) = 22 chars.
      # Max base_name = 40 - 22 = 18 chars. We use 15 to be safe.
      if len(base_name) > 5:
        base_name = base_name[:5]
      workload_name_base = (
          f'orbax-{base_name}-{timestamp}'.replace('_', '-').lower()
      )

  Console.print_info(f'Run ID:   {run_id}')

  # 4. Upload Config
  Console.print_step(3, 6, 'Uploading Configuration')
  config_root = _CONFIG_DIRECTORY.value or _OUTPUT_DIRECTORY.value
  remote_config_path = upload_config_to_gcs(
      _CONFIG_FILE.value, config_root, run_id
  )
  Console.print_success('Config uploaded.')

  # 5. Construct Commands
  Console.print_step(4, 6, 'Constructing Commands')
  hardware_type = get_hardware_type(_TPU_TYPE.value, _DEVICE_TYPE.value)
  workload_cmd = construct_workload_command(
      workload_name=workload_name_base,
      config_file=remote_config_path,
      output_directory=_OUTPUT_DIRECTORY.value,
      run_id=run_id,
      enable_pathways=_ENABLE_PATHWAYS.value,
      benchmark_binary_path=_BENCHMARK_BINARY_PATH.value,
      hardware_type=hardware_type,
      v_level=_V_LEVEL.value,
  )

  attempts = 2 if _TEST_RESTART_WORKFLOW.value else 1
  final_workload_failed = False

  for i in range(attempts):
    is_last_attempt = i == attempts - 1
    attempt_num = i + 1

    workload_name = workload_name_base
    if attempts > 1:
      workload_name = f'{workload_name}-{attempt_num}'

    Console.print_info(f'Workload: {workload_name}')

    xpk_cmd = construct_xpk_command(workload_name, workload_cmd)

    # 6. Launch
    Console.print_step(
        5,
        6,
        f'Launching Workload {workload_name} (Attempt'
        f' {attempt_num}/{attempts})',
    )
    run_command(xpk_cmd, suppress_output=not _VERBOSE.value)

    print_summary(
        workload_name=workload_name,
        run_id=run_id,
        project=_PROJECT.value,
        zone=_ZONE.value,
        cluster=_CLUSTER_NAME.value,
        output_directory=_OUTPUT_DIRECTORY.value,
    )

    # 7. Post-Launch (Wait / Delete)
    should_wait = _WAIT.value or _DELETE_CLUSTER_ON_COMPLETION.value
    if not should_wait:
      continue

    Console.print_step(
        6, 6, f'Post-Launch Actions (Attempt {attempt_num}/{attempts})'
    )
    Console.print_info(f'Waiting for workload {workload_name}...')

    if _DELETE_CLUSTER_ON_COMPLETION.value and is_last_attempt:
      Console.print_warning(
          'Cluster auto-deletion is ENABLED. Do not interrupt if you want'
          ' auto-deletion.'
      )
    else:
      Console.print_info(
          'You can Ctrl+C to stop waiting (workload will continue).'
      )

    try:
      run_command(
          [
              _XPK_PATH.value,
              'workload',
              'list',
              f'--cluster={_CLUSTER_NAME.value}',
              f'--project={_PROJECT.value}',
              f'--zone={_ZONE.value}',
              f'--wait-for-job-completion={workload_name}',
          ],
          suppress_output=not _VERBOSE.value,
      )
    except subprocess.CalledProcessError:
      Console.print_error(f'Workload {workload_name} FAILED or was preempted.')
      Console.print_info(
          'Check logs: https://console.cloud.google.com/logs/query;'
          f'query=resource.labels.pod_name:"{workload_name}"?project={_PROJECT.value}'
      )
      if is_last_attempt:
        final_workload_failed = True
    except KeyboardInterrupt:
      Console.print_warning('\nWait interrupted by user.')
      if _DELETE_CLUSTER_ON_COMPLETION.value:
        Console.print_error('Skipping cluster deletion due to interruption.')
      sys.exit(1)
    else:
      Console.print_success(
          f'Workload {workload_name} completed successfully.'
      )

  if _RAMDISK_DIRECTORY.value is not None:
    # Unmount CSI driver after running workloads, to delete
    # checkpoint files.
    update_bucket_csi_driver(mount_csi_driver=False)

  if final_workload_failed:
    sys.exit(1)

  if _DELETE_CLUSTER_ON_COMPLETION.value:
    Console.print_info(f'Deleting cluster {_CLUSTER_NAME.value}...')
    run_command(
        [
            _XPK_PATH.value,
            'cluster',
            'delete',
            f'--cluster={_CLUSTER_NAME.value}',
            f'--project={_PROJECT.value}',
            f'--zone={_ZONE.value}',
            '--force',
        ],
        suppress_output=not _VERBOSE.value,
        cwd='/tmp',
    )
    Console.print_success('Cluster deleted.')


def main() -> None:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
      "--checkpoint",
      required=True,
      help="Path (local or gs://) to the Orbax checkpoint directory.",
  )
  parser.add_argument(
      "--axis-size",
      type=int,
      required=True,
      help="Size of the single mesh axis (= number of devices participating).",
  )
  parser.add_argument(
      "--strategy",
      default="fsdp",
      choices=sorted(_STRATEGIES),
      help=(
          "Sharding strategy. `fsdp` splits dim 0 (contiguous shards);"
          " `tp_inner` splits the last dim (strided shards)."
      ),
  )
  parser.add_argument(
      "--output",
      type=pathlib.Path,
      required=True,
      help="Destination JSON path; parent dir is created if missing.",
  )
  args = parser.parse_args()

  cfg = build_config(args.checkpoint, args.axis_size, strategy=args.strategy)
  args.output.parent.mkdir(parents=True, exist_ok=True)
  args.output.write_text(json.dumps(cfg, indent=2))
  print(f"Wrote {len(cfg)} leaf entries to {args.output}")


def main(_):
  import uvicorn  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

  FLAGS.alsologtostderr = True
  logging.set_verbosity(logging.INFO)
  uvicorn.run(uvicorn_app, host="0.0.0.0", port=8080)


def main(argv: Sequence[str] | None = None) -> None:
  """Main entry point for db_cli."""
  if argv is None:
    argv = sys.argv
  uvloop.install()
  try:
    asyncio.get_event_loop()
  except RuntimeError:
    # Create the high-performance uvloop instead
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
  fire.Fire(DbCli, command=argv[1:])


def main(argv: Sequence[str] | None = None) -> None:
  """Main entry point for CTS server."""
  if argv is None:
    argv = sys.argv
  uvloop.install()
  try:
    asyncio.get_event_loop()
  except RuntimeError:
    # Create the high-performance uvloop instead
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
  fire.Fire(CtsServer, command=argv[1:])


def main(argv):
  del argv
  epath.Path(_BASE_DIR.value).mkdir(parents=True, exist_ok=True)

  test_utils.set_tensorstore_driver_for_test()

  print('Generating V0 Checkpoints...')
  # Three categories we'll generate against:
  # 1. Is Checkpoint Metadata present?
  # - Yes, No
  # 2. Item_handler type (save method which dictates item_handler contents)
  # - dict(composite), str(direct_pytree checkpoint)
  # Note we will treat v0 checkpoint handlers as unregistered by default when
  # we test loading.
  # 3. Is Pytree? (Pytree Metadata present in checkpointable dir?)
  # - Yes, No

  # The directory structure will follow the categories above:
  # base_dir /
  # 'v0_checkpoints' /
  # <'direct_checkpoint' | 'composite_checkpoint'> /
  # <checkpoint_metadata_present|missing> /
  # <pytree_checkpointable_has|missing>_metadata /

  for is_dir_ckpt, has_metadata, has_pytree in itertools.product(
      [True, False], repeat=3
  ):
    v0_generate_case(
        is_direct_checkpoint=is_dir_ckpt,
        has_checkpoint_metadata=has_metadata,
        has_pytree_metadata=has_pytree,
    )

  # --- ADDITIONAL CORRUPTIONS ---
  # The directory structure will be as follows:
  # base_dir /
  # 'v0_checkpoints' /
  # <'composite_checkpoint'|'direct_checkpoint'> /
  # <'critical_metadata_alterations'/'critical_pytree_data_alterations'> /
  # <field_to_remove> /

  # --- NON-CRITICAL METADATA ALTERATIONS ---
  # These metadata fields are safely considered non-critical for backward
  # compatibility.
  fields_to_remove = [
      'item_handlers',
      'metrics',
      'performance_metrics',
      'init_timestamp_nsecs',
      'commit_timestamp_nsecs',
      'custom_metadata',
  ]
  for field, is_dir_ckpt in itertools.product(fields_to_remove, [True, False]):
    v0_missing_checkpoint_metadata_field(field, is_dir_ckpt)

  # --- NON-CRITICAL PYTREE DATA ALTERATIONS ---
  # These files/dirs are non-critical to loading the pytree. Note: absence of
  # _sharding will only give an error if abstract pytree is not provided.
  non_critical_tasks = [
      ('_sharding', False),
      ('array_metadatas', True),
  ]
  for name, is_directory in non_critical_tasks:
    for is_dir_ckpt in [True, False]:
      v0_missing_pytree_data(
          name, is_dir_ckpt, is_dir=is_directory, is_critical=False
      )

  # --- CRITICAL PYTREE DATA ALTERATIONS ---
  # These files/dirs are critical for loading the pytree successfully.
  critical_tasks = [
      ('manifest.ocdbt', False),
      ('d', True),
  ]
  for name, is_directory in critical_tasks:
    for is_dir_ckpt in [True, False]:
      v0_missing_pytree_data(
          name, is_dir_ckpt, is_dir=is_directory, is_critical=True
      )

  print(f'V0 Checkpoints generated at {_BASE_DIR.value}')


def main(argv):
  del argv
  epath.Path(_BASE_DIR.value).mkdir(parents=True, exist_ok=True)
  test_utils.set_tensorstore_driver_for_test()
  print('Generating V1 Checkpoints...')

  # The directory structure will follow the categories above:
  # base_dir /
  # 'v1_checkpoints' /
  # <'composite_checkpoint'> /
  # <checkpoint_metadata_present|missing> /
  # <pytree_checkpointable_has|missing>_metadata /
  # Note we will be testing against unregistered handlers in our testing
  # files.
  for has_metadata, has_pytree in itertools.product(
      [True, False], repeat=2
  ):
    v1_generate_case(
        has_checkpoint_metadata=has_metadata,
        has_pytree_metadata=has_pytree,
    )

  # --- ADDITIONAL CORRUPTIONS ---
  # The directory structure will be as follows:
  # base_dir /
  # 'v1_checkpoints' /
  # 'composite_checkpoint' /
  # <Alteration_Type> /
  # <Specific_Alteration> /

  # --- NON-CRITICAL METADATA ALTERATIONS ---
  fields_to_remove = [
      'item_handlers',
      'metrics',
      'performance_metrics',
      'init_timestamp_nsecs',
      'commit_timestamp_nsecs',
      'custom_metadata',
  ]
  for field in fields_to_remove:
    v1_missing_checkpoint_metadata_field(field)

  # --- NON-CRITICAL PYTREE DATA ALTERATIONS ---
  # These files/dirs are non-critical to loading the pytree. Note: absence of
  # _sharding will only give an error if abstract pytree is not provided.
  non_critical_tasks = [
      ('_sharding', False),
      ('array_metadatas', True),
  ]
  for name, is_directory in non_critical_tasks:
    v1_missing_pytree_data(name, is_dir=is_directory, is_critical=False)

  # --- CRITICAL PYTREE DATA ALTERATIONS ---
  critical_tasks = [
      ('manifest.ocdbt', False),
      ('d', True),
  ]
  for name, is_directory in critical_tasks:
    v1_missing_pytree_data(name, is_dir=is_directory, is_critical=True)

  # --- GENERAL ALTERATIONS ---
  v1_dummy_checkpointable_present()
  v1_delete_checkpointable()

  print(f'V1 Checkpoints generated at {_BASE_DIR.value}')


def main(argv):
  if len(argv) != 2:
    print('Usage: {} YYYYMMDD'.format(sys.argv[0], file=sys.stderr))
    sys.exit(1)

  datestamp = sys.argv[1]
  if len(datestamp) != 8 or not datestamp.isdigit():
    raise Exception(
        'datestamp={} is not in the YYYYMMDD format'.format(datestamp))

  # Replacement directives go here.
  ReplaceStringsInFile(
      'MODULE.bazel', {
          'version = "head"':
              'version = "{}.0"'.format(datestamp)
      })
  ReplaceStringsInFile(
      'absl/base/config.h', {
          '#undef ABSL_LTS_RELEASE_VERSION':
              '#define ABSL_LTS_RELEASE_VERSION {}'.format(datestamp),
          '#undef ABSL_LTS_RELEASE_PATCH_LEVEL':
              '#define ABSL_LTS_RELEASE_PATCH_LEVEL 0'
      })
  ReplaceStringsInFile(
      'absl/base/options.h', {
          '#define ABSL_OPTION_USE_INLINE_NAMESPACE 0':
              '#define ABSL_OPTION_USE_INLINE_NAMESPACE 1',
          '#define ABSL_OPTION_INLINE_NAMESPACE_NAME head':
              '#define ABSL_OPTION_INLINE_NAMESPACE_NAME lts_{}'.format(
                  datestamp)
      })
  ReplaceStringsInFile(
      'CMakeLists.txt',
      {
          'project(absl LANGUAGES CXX)': (
              'project(absl LANGUAGES CXX VERSION {})'.format(datestamp)
          ),
          # Set the SOVERSION to YYMM.0.0 - The first 0 means we only have ABI
          # compatible changes, and the second 0 means we can increment it to
          # mark changes as ABI-compatible, for patch releases.  Note that we
          # only use the last two digits of the year and the month because the
          # MacOS linker requires the first part of the SOVERSION to fit into
          # 16 bits.
          # https://www.sicpers.info/2013/03/how-to-version-a-mach-o-library/
          'ABSL_SOVERSION 0': 'ABSL_SOVERSION "{}.0.0"'.format(datestamp[2:6]),
      },
  )
  StripContentBetweenTags('CMakeLists.txt', '# absl:lts-remove-begin',
                          '# absl:lts-remove-end')


def main(_):
  absltest.main()


def main(_):
  absltest.main()


def main(unused_argv):
  config = alpha_zero.Config(
      game=FLAGS.game,
      path=FLAGS.path,
      learning_rate=FLAGS.learning_rate,
      weight_decay=FLAGS.weight_decay,
      decouple_weight_decay=FLAGS.decouple_weight_decay,
      train_batch_size=FLAGS.train_batch_size,
      replay_buffer_size=FLAGS.replay_buffer_size,
      replay_buffer_reuse=FLAGS.replay_buffer_reuse,
      max_steps=FLAGS.max_steps,
      checkpoint_freq=FLAGS.checkpoint_freq,
      actors=FLAGS.actors,
      evaluators=FLAGS.evaluators,
      uct_c=FLAGS.uct_c,
      max_simulations=FLAGS.max_simulations,
      policy_alpha=FLAGS.policy_alpha,
      policy_epsilon=FLAGS.policy_epsilon,
      temperature=FLAGS.temperature,
      temperature_drop=FLAGS.temperature_drop,
      evaluation_window=FLAGS.evaluation_window,
      eval_levels=FLAGS.eval_levels,
      nn_model=FLAGS.nn_model,
      nn_width=FLAGS.nn_width,
      nn_depth=FLAGS.nn_depth,
      observation_shape=None,
      output_size=None,
      quiet=FLAGS.quiet,
      verbose=FLAGS.verbose,
      nn_api_version=FLAGS.nn_api,
  )

  alpha_zero.alpha_zero(config)


def main(_):
  if FLAGS.games == "*":
    games_list = [
        game.short_name
        for game in pyspiel.registered_games()
        if game.default_loadable
    ]
  else:
    games_list = FLAGS.games.split(";")

  logging.info("Running benchmark for %s games.", len(games_list))
  logging.info("This will take approximately %d seconds.",
               len(games_list) * FLAGS.time_limit)

  game_stats = []
  for game_name in games_list:
    logging.info("Running benchmark on %s", game_name)
    game_stats.append(
        _rollout_until_timeout(game_name, FLAGS.time_limit, FLAGS.give_up_after,
                               FLAGS.if_simultaneous_convert_to_turn_based))

  with pd.option_context("display.max_rows", None,
                         "display.max_columns", None,
                         "display.width", 200):
    df = pd.DataFrame(game_stats)
    # Use nice header names.
    df.rename(columns={
        "game_name": "Game",
        "ms_per_rollouts": "msec/rollout",
        "ms_per_moves": "msec/move",
        "giveups_per_rollout": "Give ups/rollouts",
        "time_elapsed": "Time elapsed [sec]"
    }, inplace=True)

    print("---")
    print("Results for following benchmark configuration:")
    print("time_limit =", FLAGS.time_limit)
    print("give_up_after =", FLAGS.give_up_after)
    print("---")
    print(df)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  # Make the network.
  net = hk.without_apply_rng(hk.transform(net_fn))

  # Make the optimiser.
  opt = optax.adam(1e-4)

  @jax.jit
  def loss(
      params: Params,
      inputs: np.ndarray,
      targets: np.ndarray,
  ) -> jax.Array:
    """Cross-entropy loss."""
    assert targets.dtype == np.int32
    log_probs = net.apply(params, inputs)
    return -jnp.mean(one_hot(targets, NUM_ACTIONS) * log_probs)

  @jax.jit
  def accuracy(
      params: Params,
      inputs: np.ndarray,
      targets: np.ndarray,
  ) -> jax.Array:
    """Classification accuracy."""
    predictions = net.apply(params, inputs)
    return jnp.mean(jnp.argmax(predictions, axis=-1) == targets)

  @jax.jit
  def update(
      params: Params,
      opt_state: OptState,
      inputs: np.ndarray,
      targets: np.ndarray,
  ) -> Tuple[Params, OptState]:
    """Learning rule (stochastic gradient descent)."""
    _, gradient = jax.value_and_grad(loss)(params, inputs, targets)
    updates, opt_state = opt.update(gradient, opt_state)
    new_params = optax.apply_updates(params, updates)
    return new_params, opt_state

  def output_samples(params: Params, max_samples: int):
    """Output some cases where the policy disagrees with the dataset action."""
    if max_samples == 0:
      return
    count = 0
    with open(os.path.join(FLAGS.data_path, 'test.txt')) as f:
      lines = list(f)
    np.random.shuffle(lines)
    for line in lines:
      state = GAME.new_initial_state()
      actions = _no_play_trajectory(line)
      for action in actions:
        if not state.is_chance_node():
          observation = np.array(state.observation_tensor(), np.float32)
          policy = np.exp(net.apply(params, observation))
          probs_actions = [(p, a + MIN_ACTION) for a, p in enumerate(policy)]
          pred = max(probs_actions)[1]
          if pred != action:
            print(state)
            for p, a in reversed(sorted(probs_actions)[-TOP_K_ACTIONS:]):
              print('{:7} {:.2f}'.format(state.action_to_string(a), p))
            print('Ground truth {}\n'.format(state.action_to_string(action)))
            count += 1
            break
        state.apply_action(action)
      if count >= max_samples:
        return

  # Make datasets.
  if FLAGS.data_path is None:
    raise app.UsageError(
        'Please generate your own supervised training data or download from '
        'https://console.cloud.google.com/storage/browser/openspiel-data/bridge'
        ' and supply the local location as --data_path')
  train = batch(
      make_dataset(os.path.join(FLAGS.data_path, 'train.txt')),
      FLAGS.train_batch)
  test = batch(
      make_dataset(os.path.join(FLAGS.data_path, 'test.txt')), FLAGS.eval_batch)

  # Initialize network and optimiser.
  rng = jax.random.PRNGKey(FLAGS.rng_seed)  # seed used for network weights
  inputs, unused_targets = next(train)
  params = net.init(rng, inputs)
  opt_state = opt.init(params)

  # Train/eval loop.
  for step in range(FLAGS.iterations):
    # Do SGD on a batch of training examples.
    inputs, targets = next(train)
    params, opt_state = update(params, opt_state, inputs, targets)

    # Periodically evaluate classification accuracy on the test set.
    if (1 + step) % FLAGS.eval_every == 0:
      inputs, targets = next(test)
      test_accuracy = accuracy(params, inputs, targets)
      print(f'After {1+step} steps, test accuracy: {test_accuracy}.')
      if FLAGS.save_path:
        filename = os.path.join(FLAGS.save_path, f'params-{1 + step}.pkl')
        with open(filename, 'wb') as pkl_file:
          pickle.dump(params, pkl_file)
      output_samples(params, FLAGS.num_examples)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  game = pyspiel.load_game("bridge_uncontested_bidding", {
      "relative_scoring": True,
      "rng_seed": FLAGS.rng_seed,
  })
  bots = [
      bluechip_bridge_uncontested_bidding.BlueChipBridgeBot(
          game, 0, _WBridge5Client(FLAGS.bot_cmd)),
      bluechip_bridge_uncontested_bidding.BlueChipBridgeBot(
          game, 1, _WBridge5Client(FLAGS.bot_cmd)),
  ]
  results = []

  for i_deal in range(FLAGS.num_deals):
    state = _run_once(game.new_initial_state(), bots)
    print("Deal #{}; final state:\n{}".format(i_deal, state))
    results.append(state.returns())

  stats = np.array(results)
  mean = np.mean(stats, axis=0)
  stderr = np.std(stats, axis=0, ddof=1) / np.sqrt(FLAGS.num_deals)
  print(u"Absolute score: {:+.1f}\u00b1{:.1f}".format(mean[0], stderr[0]))
  print(u"Relative score: {:+.1f}\u00b1{:.1f}".format(mean[1], stderr[1]))


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  game = pyspiel.load_game("bridge(use_double_dummy_result=false)")
  net, params = load_model()
  bots = [
      bluechip_bridge.BlueChipBridgeBot(game, 0, controller_factory),
      bluechip_bridge.BlueChipBridgeBot(game, 2, controller_factory)
  ]

  results = []

  for i_deal in range(FLAGS.num_deals):
    state = _run_once(game.new_initial_state(), bots, net, params)
    print("Deal #{}; final state:\n{}".format(i_deal, state))
    results.append(state.returns())

  stats = np.array(results)
  mean = np.mean(stats, axis=0)
  stderr = np.std(stats, axis=0, ddof=1) / np.sqrt(FLAGS.num_deals)
  print(u"Absolute score: {:+.1f}\u00b1{:.1f}".format(mean[0], stderr[0]))
  print(u"Relative score: {:+.1f}\u00b1{:.1f}".format(mean[1], stderr[1]))


def main(_):
  game = pyspiel.load_game(
      FLAGS.game,
      {"players": FLAGS.players},
  )

  solver = None
  if FLAGS.solver == "cfr":
    solver = pyspiel.CFRSolver(game)
  elif FLAGS.solver == "cfrplus":
    solver = pyspiel.CFRPlusSolver(game)
  elif FLAGS.solver == "cfrbr":
    solver = pyspiel.CFRBRSolver(game)
  else:
    print("Unknown solver")
    sys.exit(0)

  for i in range(int(FLAGS.iterations / 2)):
    solver.evaluate_and_update_policy()
    print("Iteration {} exploitability: {:.6f}".format(
        i, pyspiel.exploitability(game, solver.average_policy())))

  filename = os.path.join(
      tempfile.gettempdir(), "{}_solver.pickle".format(FLAGS.solver)
  )
  print("Persisting the model...")
  with open(filename, "wb") as file:
    pickle.dump(solver, file, pickle.HIGHEST_PROTOCOL)

  print("Loading the model...")
  with open(filename, "rb") as file:
    loaded_solver = pickle.load(file)
  print("Exploitability of the loaded model: {:.6f}".format(
      pyspiel.exploitability(game, loaded_solver.average_policy())))

  for i in range(int(FLAGS.iterations / 2)):
    loaded_solver.evaluate_and_update_policy()
    tabular_policy = loaded_solver.tabular_average_policy()
    print(f"Tabular policy length: {len(tabular_policy)}")
    print("Iteration {} exploitability: {:.6f}".format(
        int(FLAGS.iterations / 2) + i,
        pyspiel.exploitability(game, loaded_solver.average_policy())))


def main(_):
  game = pyspiel.load_game(FLAGS.game, {"players": FLAGS.players})
  cfr_solver = cfr.CFRSolver(game)

  for i in range(FLAGS.iterations):
    cfr_solver.evaluate_and_update_policy()
    if i % FLAGS.print_freq == 0:
      conv = exploitability.exploitability(game, cfr_solver.average_policy())
      print("Iteration {} exploitability {}".format(i, conv))


def main(_):
  logging.set_verbosity(logging.ERROR)  # silence internal game logging
  save_path = _SAVE_PATH.value
  config = get_config()
  im = ImitationDatasetConstructor(save_path, config)
  im.construct_dataset()


def main(_):
  logging.set_verbosity(logging.ERROR)  # silence internal game logging
  save_path = _SAVE_PATH.value
  config = get_config()
  psro = PSRO(save_path, config)
  psro.run()


def main(unused_argv):
  logging.info("Loading %s", FLAGS.game_name)

  game = pyspiel.load_game(FLAGS.game_name)
  deep_cfr_solver = deep_cfr.DeepCFRSolver(
      game,
      policy_network_layers=(64,),
      advantage_network_layers=(64,),
      num_iterations=FLAGS.num_iterations,
      num_traversals=FLAGS.num_traversals,
      reinitialize_advantage_networks=True,
      learning_rate=1e-3,
      batch_size_advantage=256,
      batch_size_strategy=256,
      memory_capacity=100000,
      policy_network_train_steps=2500,
      advantage_network_train_steps=375,
      print_nash_convs=False,  # for debugging purposes
  )

  _, advantage_losses, policy_loss = deep_cfr_solver.solve()
  for player, losses in advantage_losses.items():
    logging.info("Advantage for player %d: %s", player,
                 losses[:2] + ["..."] + losses[-2:])
    logging.info(
        f"Advantage Buffer Size for player {player}:"
        f" {len(deep_cfr_solver.advantage_buffers[player])}"
    )
  logging.info(f"Strategy Buffer Size: {len(deep_cfr_solver.strategy_buffer)}")
  logging.info(f"Final policy loss: {policy_loss}")

  average_policy = policy.tabular_policy_from_callable(
      game, deep_cfr_solver.action_probabilities)

  conv = exploitability.nash_conv(game, average_policy)
  logging.info(f"Deep CFR in {FLAGS.game_name} - NashConv: {conv}")

  average_policy_values = expected_game_score.policy_value(
      game.new_initial_state(), [average_policy] * 2)
  if FLAGS.game_name == "kuhn_poker":
    # We know EVs
    logging.info(
        f"Computed player 0 value: {average_policy_values[0]:.2f} (expected:"
        f" {-1/18:.2f})."
    )
    logging.info(
        f"Computed player 1 value: {average_policy_values[1]:.2f} (expected:"
        f" {1/18:.2f})."
    )
  else:
    logging.info(f"Computed player 0 value: {average_policy_values[0]:.2f}")
    logging.info(f"Computed player 1 value: {average_policy_values[1]:.2f}")


def main(unused_argv):
  logging.info(f"Loading {FLAGS.game_name}")
  game = pyspiel.load_game(FLAGS.game_name)

  deep_cfr_solver = deep_cfr.DeepCFRSolver(
      game,
      policy_network_layers=(64,),
      advantage_network_layers=(64,),
      num_iterations=FLAGS.num_iterations,
      num_traversals=FLAGS.num_traversals,
      reinitialize_advantage_networks=True,
      learning_rate=1e-3,
      batch_size_advantage=256,
      batch_size_strategy=256,
      memory_capacity=100000,
      policy_network_train_steps=2500,
      advantage_network_train_steps=375,
      print_nash_convs=False,  # for debugging purposes
  )

  _, advantage_losses, policy_loss = deep_cfr_solver.solve()
  for player, losses in enumerate(advantage_losses):
    logging.info("Advantage for player %d: %s", player, losses)
    assert deep_cfr_solver.advantage_buffers[player] is not None
    logging.info(
        f"Advantage Buffer Size for player {player}:"
        f" {len(deep_cfr_solver.advantage_buffers[player])}"
    )
  logging.info(f"Strategy Buffer Size: {len(deep_cfr_solver.strategy_buffer)}")
  logging.info(f"Final policy loss: {policy_loss}")

  average_policy = policy.tabular_policy_from_callable(
      game, deep_cfr_solver.action_probabilities)
  pyspiel_policy = policy.python_policy_to_pyspiel_policy(average_policy)
  conv = pyspiel.nash_conv(game, pyspiel_policy)
  logging.info(f"Deep CFR in {FLAGS.game_name} - NashConv: {conv}")

  average_policy_values = expected_game_score.policy_value(
      game.new_initial_state(), [average_policy] * 2)
  if FLAGS.game_name == "kuhn_poker":
    # We know EVs
    logging.info(
        f"Computed player 0 value: {average_policy_values[0]:.2f} (expected:"
        f" {-1/18:.2f})."
    )
    logging.info(
        f"Computed player 1 value: {average_policy_values[1]:.2f} (expected:"
        f" {1/18:.2f})."
    )
  else:
    logging.info(f"Computed player 0 value: {average_policy_values[0]:.2f}")
    logging.info(f"Computed player 1 value: {average_policy_values[1]:.2f}")


def main(unused_argv):
  logging.info("Loading %s", FLAGS.game_name)
  game = pyspiel.load_game(FLAGS.game_name)
  deep_cfr_solver = deep_cfr_tf2.DeepCFRSolver(
      game,
      policy_network_layers=(64, 64, 64, 64),
      advantage_network_layers=(64, 64, 64, 64),
      num_iterations=FLAGS.num_iterations,
      num_traversals=FLAGS.num_traversals,
      learning_rate=1e-3,
      batch_size_advantage=2048,
      batch_size_strategy=2048,
      memory_capacity=1e6,
      policy_network_train_steps=5000,
      advantage_network_train_steps=500,
      reinitialize_advantage_networks=True,
      infer_device="cpu",
      train_device="cpu")
  _, advantage_losses, policy_loss = deep_cfr_solver.solve()
  for player, losses in advantage_losses.items():
    logging.info("Advantage for player %d: %s", player,
                 losses[:2] + ["..."] + losses[-2:])
    logging.info("Advantage Buffer Size for player %s: '%s'", player,
                 len(deep_cfr_solver.advantage_buffers[player]))
  logging.info("Strategy Buffer Size: '%s'",
               len(deep_cfr_solver.strategy_buffer))
  logging.info("Final policy loss: '%s'", policy_loss)

  average_policy = policy.tabular_policy_from_callable(
      game, deep_cfr_solver.action_probabilities)

  conv = exploitability.nash_conv(game, average_policy)
  logging.info("Deep CFR in '%s' - NashConv: %s", FLAGS.game_name, conv)

  average_policy_values = expected_game_score.policy_value(
      game.new_initial_state(), [average_policy] * 2)
  print("Computed player 0 value: {}".format(average_policy_values[0]))
  print("Computed player 1 value: {}".format(average_policy_values[1]))


def main(_):
  game = pyspiel.load_game(FLAGS.game)
  discounted_cfr_solver = discounted_cfr.DCFRSolver(game)

  for i in range(FLAGS.iterations):
    discounted_cfr_solver.evaluate_and_update_policy()
    if i % FLAGS.print_freq == 0:
      conv = exploitability.exploitability(
          game, discounted_cfr_solver.average_policy())
      print("Iteration {} exploitability {}".format(i, conv))


def main(_):
  rng = np.random.RandomState(FLAGS.seed)
  games_list = pyspiel.registered_names()
  assert "dots_and_boxes" in games_list

  game_string = "dots_and_boxes(num_rows=2,num_cols=2)"
  print("Creating game: {}".format(game_string))
  game = pyspiel.load_game(game_string)

  agents = [
      LoadAgent(FLAGS.player0, 0, rng),
      LoadAgent(FLAGS.player1, 1, rng),
  ]

  state = game.new_initial_state()

  # Print the initial state
  print("INITIAL STATE")
  print(str(state))

  while not state.is_terminal():
    current_player = state.current_player()
    # Decision node: sample action for the single current player
    legal_actions = state.legal_actions()
    for action in legal_actions:
      print(
          "Legal action: {} ({})".format(
              state.action_to_string(current_player, action), action
          )
      )
    action = agents[current_player].step(state)
    action_string = state.action_to_string(current_player, action)
    print("Player ", current_player, ", chose action: ", action_string)
    state.apply_action(action)

    print("")
    print("NEXT STATE:")
    print(str(state))
    if not state.is_terminal():
      print(str(state.observation_tensor()))

  # Game is now done. Print utilities for each player
  returns = state.returns()
  for pid in range(game.num_players()):
    print("Utility for player {} is {}".format(pid, returns[pid]))


def main(_):
  game = "breakthrough"
  num_players = 2

  env_configs = {"columns": 5, "rows": 5}
  env = rl_environment.Environment(game, **env_configs)
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  # random agents for evaluation
  random_agents = [
      random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
      for idx in range(num_players)
  ]

  hidden_layers_sizes = [int(hs) for hs in FLAGS.hidden_layers_sizes]
  # pylint: disable=g-complex-comprehension

  agents = [
      dqn.DQN(
          player_id=idx,
          state_representation_size=info_state_size,
          num_actions=num_actions,
          hidden_layers_sizes=hidden_layers_sizes,
          replay_buffer_capacity=FLAGS.replay_buffer_capacity,
          batch_size=FLAGS.batch_size,
      )
      for idx in range(num_players)
  ]

  for ep in range(FLAGS.num_train_episodes):
    if (ep + 1) % FLAGS.eval_every == 0:
      r_mean = eval_against_random_bots(env, agents, random_agents, 1000)
      logging.info("[%s] Mean episode rewards %s", ep + 1, r_mean)

    if FLAGS.use_checkpoints and (ep + 1) % FLAGS.save_every == 0:
      for agent in agents:
        agent.save(FLAGS.checkpoint_dir)

    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      if env.is_turn_based:
        agent_output = agents[player_id].step(time_step)
        action_list = [agent_output.action]
      else:
        agents_output = [agent.step(time_step) for agent in agents]
        action_list = [agent_output.action for agent_output in agents_output]
      time_step = env.step(action_list)

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)


def main(_):
  game = "breakthrough"
  num_players = 2

  env_configs = {"columns": 5, "rows": 5}
  env = rl_environment.Environment(game, **env_configs)
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  # random agents for evaluation
  random_agents = [
      random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
      for idx in range(num_players)
  ]

  hidden_layers_sizes = [int(hs) for hs in FLAGS.hidden_layers_sizes]
  # pylint: disable=g-complex-comprehension
  agents = [
      dqn.DQN(
          player_id=idx,
          state_representation_size=info_state_size,
          num_actions=num_actions,
          hidden_layers_sizes=hidden_layers_sizes,
          replay_buffer_capacity=FLAGS.replay_buffer_capacity,
          batch_size=FLAGS.batch_size,
      )
      for idx in range(num_players)
  ]

  for ep in range(FLAGS.num_train_episodes):
    if (ep + 1) % FLAGS.eval_every == 0:
      r_mean = eval_against_random_bots(env, agents, random_agents, 1000)
      logging.info("[%s] Mean episode rewards %s", ep + 1, r_mean)

    if FLAGS.use_checkpoints and (ep + 1) % FLAGS.save_every == 0:
      for agent in agents:
        agent.save(FLAGS.checkpoint_dir)

    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      if env.is_turn_based:
        agent_output = agents[player_id].step(time_step)
        action_list = [agent_output.action]
      else:
        agents_output = [agent.step(time_step) for agent in agents]
        action_list = [agent_output.action for agent_output in agents_output]
      time_step = env.step(action_list)

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)


def main(_):
  game = "lewis_signaling"
  num_players = 2

  num_states = FLAGS.num_states
  num_messages = FLAGS.num_messages
  if FLAGS.payoffs == "random":
    payoffs = np.random.random((num_states, num_states))
    payoffs_str = ",".join([str(x) for x in payoffs.flatten()])
  elif FLAGS.payoffs == "climbing":
    # This is a particular payoff matrix that is hard for decentralized
    # algorithms. Introduced in C. Claus and C. Boutilier, "The dynamics of
    # reinforcement learning in cooperative multiagent systems", 1998, for
    # simultaneous action games, but it is difficult even in the case of
    # signaling games.
    payoffs = np.array([[11, -30, 0], [-30, 7, 6], [0, 0, 5]]) / 30
    payoffs_str = ",".join([str(x) for x in payoffs.flatten()])
  else:
    payoffs_str = FLAGS.payoffs
    try:
      payoffs_list = [float(x) for x in payoffs_str.split(",")]
      payoffs = np.array(payoffs_list).reshape((num_states, num_states))
    except ValueError:
      raise ValueError(
          "There should be {} (states * actions) elements in payoff. "
          "Found {} elements".format(num_states * num_states, len(payoffs_list))
      ) from None

  env_configs = {
      "num_states": num_states,
      "num_messages": num_messages,
      "payoffs": payoffs_str,
  }

  env = rl_environment.Environment(game, **env_configs)
  state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]
  replay_buffer_capacity = FLAGS.replay_buffer_capacity

  # Results to store
  num_runs = FLAGS.num_runs
  training_episodes = FLAGS.num_episodes
  log_interval = FLAGS.log_interval
  rewards = np.zeros((num_runs, training_episodes // log_interval))
  opts = np.zeros((num_runs, training_episodes // log_interval))
  converge_point = np.zeros((num_states, num_states))
  percent_opt = 0

  # Repeat the experiment num_runs times
  for i in range(num_runs):
    # pylint: disable=g-complex-comprehension
    agents = [
        dqn.DQN(
            player_id=idx,
            state_representation_size=state_size,
            num_actions=num_actions,
            learning_rate=FLAGS.step_size,
            replay_buffer_capacity=replay_buffer_capacity,
            epsilon_start=FLAGS.eps_init,
            epsilon_end=FLAGS.eps_final,
            epsilon_decay_duration=FLAGS.eps_decay_steps * 2,
        )
        for idx in range(num_players)
    ]

    # 1. Train the agents
    for cur_episode in range(training_episodes):
      time_step = env.reset()
      # Find cur_state for logging. See lewis_signaling.cc for info_state
      # details
      cur_state = time_step.observations["info_state"][0][3:].index(1)
      while not time_step.last():
        player_id = time_step.observations["current_player"]
        agent_output = agents[player_id].step(time_step)
        time_step = env.step([agent_output.action])

      # Episode is over, step all agents with final info state.
      for agent in agents:
        agent.step(time_step)

      # Store rewards
      reward = time_step.rewards[0]
      max_reward = payoffs[cur_state].max()
      cur_idx = (i, cur_episode // log_interval)
      rewards[cur_idx] += reward / log_interval
      opts[cur_idx] += np.isclose(reward, max_reward) / log_interval

    base_info_state0 = [1.0, 0.0, 0.0] + [0.0] * num_states
    base_info_state1 = [0.0, 1.0, 0.0] + [0.0] * num_states

    for s in range(num_states):
      info_state0 = copy.deepcopy(base_info_state0)
      info_state0[3 + s] = 1.0
      # pylint: disable=protected-access
      m, _ = agents[0].act_epsilon_greedy(
          info_state0, np.arange(num_messages), 0
      )
      info_state1 = copy.deepcopy(base_info_state1)
      info_state1[3 + m] = 1.0
      a, _ = agents[1].act_epsilon_greedy(info_state1, np.arange(num_states), 0)
      converge_point[s, a] += 1
      best_act = payoffs[s].argmax()
      percent_opt += int(a == best_act) / num_runs / num_states

  if FLAGS.plot:
    try:
      # pylint: disable=g-import-not-at-top
      import matplotlib as mpl  # pyright: ignore[reportMissingModuleSource]
      # pyright: ignore[reportMissingModuleSource]
      import matplotlib.pyplot as plt
    except ModuleNotFoundError:
      print("'matplotlib' not found, install it with pip and rerun.")
      return percent_opt

    from scipy import stats  # pylint: disable=g-import-not-at-top

    params = {
        "font.size": 13,
        "axes.labelsize": 13,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
    }
    mpl.rcParams.update(params)

    def init_fig():
      fig, ax = plt.subplots(1, 1)
      ax.spines["top"].set_visible(False)
      ax.spines["right"].set_visible(False)
      return fig, ax

    def plot_scalars(
        scalars,
        repetition_axis=0,
        scalar_labels=None,
        title=None,
        ax_labels=None,
    ):
      """Plots scalar on ax by filling 1 standard error.

      Args:
          scalars: List of scalars to plot (mean taken over repetition axis)
          repetition_axis: Axis to take the mean over
          scalar_labels: Labels for the scalars (for legend)
          title: Figure title
          ax_labels: Labels for x and y axis (list of 2 strings)
      """
      if not all([len(s.shape) == 2 for s in scalars]):
        raise ValueError("Only 2D arrays supported for plotting")

      if scalar_labels is None:
        scalar_labels = [None] * len(scalars)

      if len(scalars) != len(scalar_labels):
        raise ValueError(
            "Wrong number of scalar labels, expected {} but received {}".format(
                len(scalars), len(scalar_labels)
            )
        )

      _, plot_axis = init_fig()
      for i, scalar in enumerate(scalars):
        xs = np.arange(scalar.shape[1 - repetition_axis]) * FLAGS.log_interval
        mean = scalar.mean(axis=repetition_axis)
        sem = stats.sem(scalar, axis=repetition_axis)
        plot_axis.plot(xs, mean, label=scalar_labels[i])
        plot_axis.fill_between(xs, mean - sem, mean + sem, alpha=0.5)

      if title is not None:
        plot_axis.set_title(title)
      if ax_labels is not None:
        plot_axis.set_xlabel(ax_labels[0])
        plot_axis.set_ylabel(ax_labels[1])

    def plot_confusion_matrix(cm, cmap=plt.cm.Blues, title=None):
      """Plot the confusion matrix.

      Args:
          cm (np.ndarray): Confusion matrix to plot
          cmap: Color map to be used in matplotlib's imshow
          title: Figure title

      Returns:
          Figure and axis on which the confusion matrix is plotted.
      """
      fig, ax = plt.subplots()
      ax.imshow(cm, interpolation="nearest", cmap=cmap)
      ax.set_xticks([])
      ax.set_yticks([])
      ax.set_xlabel("Receiver's action", fontsize=14)
      ax.set_ylabel("Sender's state", fontsize=14)
      # Loop over data dimensions and create text annotations.
      fmt = "d"
      thresh = cm.max() / 2.0
      for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
          ax.text(
              j,
              i,
              format(cm[i, j], fmt),
              ha="center",
              va="center",
              color="white" if cm[i, j] > thresh else "black",
          )
      fig.tight_layout()
      if title is not None:
        ax.set_title(title)
      return fig, ax

    plot_scalars(
        [rewards],
        title="Reward graph (DQN)",
        ax_labels=["Episodes", "Reward per episode"],
    )
    plot_scalars(
        [opts],
        title="Percentage of optimal actions (DQN)",
        ax_labels=["Episodes", "% optimal actions"],
    )

    plot_confusion_matrix(
        converge_point.astype(int), title="Final policy (DQN)"
    )

    plt.show()

  return percent_opt


def main(_):
  game = "skat"
  num_players = 3

  env_configs = {}
  env = rl_environment.Environment(game, **env_configs)
  observation_tensor_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  # random agents for evaluation
  random_agents = [
      random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
      for idx in range(num_players)
  ]

  hidden_layers_sizes = [int(s) for s in FLAGS.hidden_layers_sizes]
  # pylint: disable=g-complex-comprehension
  agents = [
      dqn.DQN(
          player_id=idx,
          state_representation_size=observation_tensor_size,
          num_actions=num_actions,
          hidden_layers_sizes=hidden_layers_sizes,
          replay_buffer_capacity=FLAGS.replay_buffer_capacity,
          batch_size=FLAGS.batch_size,
      )
      for idx in range(num_players)
  ]

  for ep in range(FLAGS.num_train_episodes):
    if (ep + 1) % FLAGS.eval_every == 0:
      r_mean = eval_against_random_bots(
          env, agents, random_agents, FLAGS.num_eval_games
      )
      logging.info("[%s] Mean episode rewards %s", ep + 1, r_mean)
      # If you want saving, uncomment
      if FLAGS.use_checkpoints:
        for i in range(num_players):
          agents[i].save(FLAGS.checkpoint_dir)

    time_step = env.reset()
    # Randomize position.
    if FLAGS.randomize_positions:
      positions = random.sample(range(len(agents)), len(agents))
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      if FLAGS.randomize_positions:
        position = positions[player_id]
        agents[position].player_id = player_id
      else:
        position = player_id
      agent_output = agents[position].step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)


def main(unused_argv):
  logging.info(f"Loading {FLAGS.game_name}")
  game = pyspiel.load_game(FLAGS.game_name)

  agent = escher.Agent(game, escher.Config())
  train_cfg = escher.TrainConfig(game)
  train_cfg.iterations = 100
  train_cfg.evaluation_interval = 20
  train_cfg.nashconv = True

  escher.train(train_cfg, agent)

  average_policy = policy.tabular_policy_from_callable(
      game, lambda s: _action_probabilities(agent, s)
  )
  pyspiel_policy = policy.python_policy_to_pyspiel_policy(average_policy)
  conv = pyspiel.nash_conv(game, pyspiel_policy)
  logging.info(f"ESCHER in {FLAGS.game_name} - NashConv: {conv}")

  avg_policy_vals = expected_game_score.policy_value(
      game.new_initial_state(), [average_policy] * 2
  )
  if FLAGS.game_name == "kuhn_poker":
    # We know EVs
    logging.info(
        f"Computed player 0 value: {avg_policy_vals[0]:.2f} (expected:"
        f" {-1/18:.2f})."
    )
    logging.info(
        f"Computed player 1 value: {avg_policy_vals[1]:.2f} (expected:"
        f" {1/18:.2f})."
    )
  else:
    logging.info(f"Computed player 0 value: {avg_policy_vals[0]:.2f}")
    logging.info(f"Computed player 1 value: {avg_policy_vals[1]:.2f}")


def main(_):
  games_list = pyspiel.registered_games()
  print("Registered games:")
  print(games_list)

  action_string = None

  print("Creating game: " + FLAGS.game_string)
  game = pyspiel.load_game(FLAGS.game_string)

  # Create the initial state
  state = game.new_initial_state()

  # Print the initial state
  print(str(state))

  while not state.is_terminal():
    # The state can be three different types: chance node,
    # simultaneous node, or decision node
    if state.is_chance_node():
      # Chance node: sample an outcome
      outcomes = state.chance_outcomes()
      num_actions = len(outcomes)
      print("Chance node, got " + str(num_actions) + " outcomes")
      action_list, prob_list = zip(*outcomes)
      action = np.random.choice(action_list, p=prob_list)
      print("Sampled outcome: ",
            state.action_to_string(state.current_player(), action))
      state.apply_action(action)
    elif state.is_simultaneous_node():
      # Simultaneous node: sample actions for all players.
      random_choice = lambda a: np.random.choice(a) if a else [0]
      chosen_actions = [
          random_choice(state.legal_actions(pid))
          for pid in range(game.num_players())
      ]
      print("Chosen actions: ", [
          state.action_to_string(pid, action)
          for pid, action in enumerate(chosen_actions)
      ])
      state.apply_actions(chosen_actions)
    else:
      # Decision node: sample action for the single current player
      action = random.choice(state.legal_actions(state.current_player()))
      action_string = state.action_to_string(state.current_player(), action)
      print("Player ", state.current_player(), ", randomly sampled action: ",
            action_string)
      state.apply_action(action)
    print(str(state))

  # Game is now done. Print utilities for each player
  returns = state.returns()
  for pid in range(game.num_players()):
    print("Utility for player {} is {}".format(pid, returns[pid]))


def main(_):
  game = pyspiel.load_game(FLAGS.game, {"players": FLAGS.players})
  xfp_solver = fictitious_play.XFPSolver(game)
  for i in range(FLAGS.iterations):
    xfp_solver.iteration()
    conv = exploitability.exploitability(game, xfp_solver.average_policy())
    if i % FLAGS.print_freq == 0:
      print("Iteration: {} Conv: {}".format(i, conv))
      sys.stdout.flush()


def main(argv):
  del argv

  game = pyspiel.load_game(FLAGS.game)
  game_type = game.get_type()

  if game_type.dynamics == pyspiel.GameType.Dynamics.SIMULTANEOUS:
    logging.warn("%s is not turn-based. Trying to reload game as turn-based.",
                 FLAGS.game)
    game = pyspiel.load_game_as_turn_based(FLAGS.game)

  gametree = export_gambit(game)  # use default decorators
  if FLAGS.print:
    print(gametree)
  else:
    with open(FLAGS.out, "w") as f:
      f.write(gametree)
    logging.info("Game tree for %s saved to file: %s", FLAGS.game, FLAGS.out)


def main(_):
  game = pyspiel.load_game(_GAME_STRING.value)
  game_stats = GameStats()
  state = game.new_initial_state()
  traverse_game_tree(game, state, game_stats)
  print(game_stats)


def main(_):
  games_list = pyspiel.registered_games()
  print("Registered games:")
  for game in games_list:
    print(" ", game.short_name)
  print()

  print("Creating game:", FLAGS.game)
  params = {}
  if FLAGS.players is not None:
    params["players"] = FLAGS.players
  game = pyspiel.load_game(FLAGS.game, params)

  print("Getting all states; depth_limit = {}".format(FLAGS.depth_limit))
  all_states = get_all_states.get_all_states(game, FLAGS.depth_limit,
                                             FLAGS.include_terminals,
                                             FLAGS.include_chance_states)

  count = 0
  for state in all_states:
    print(state)
    count += 1

  print()
  print("Total: {} states.".format(count))


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  if FLAGS.hidden_layer_sizes is None:
    # Cannot pass default arguments as lists due to style requirements, so we
    # override it here if they are not set.
    FLAGS.hidden_layer_sizes = DEFAULT_LAYER_SIZES

  # Make the network.
  net = hk.without_apply_rng(hk.transform(net_fn))

  # Make the optimiser.
  opt = optax.adam(FLAGS.step_size)

  @jax.jit
  def loss(
      params: Params,
      inputs: np.ndarray,
      targets: np.ndarray,
  ) -> jax.Array:
    """Cross-entropy loss."""
    assert targets.dtype == np.int32
    log_probs = net.apply(params, inputs)
    return -jnp.mean(one_hot(targets, NUM_ACTIONS) * log_probs)

  @jax.jit
  def accuracy(
      params: Params,
      inputs: np.ndarray,
      targets: np.ndarray,
  ) -> jax.Array:
    """Classification accuracy."""
    predictions = net.apply(params, inputs)
    return jnp.mean(jnp.argmax(predictions, axis=-1) == targets)

  @jax.jit
  def update(
      params: Params,
      opt_state: OptState,
      inputs: np.ndarray,
      targets: np.ndarray,
  ) -> Tuple[Params, OptState]:
    """Learning rule (stochastic gradient descent)."""
    _, gradient = jax.value_and_grad(loss)(params, inputs, targets)
    updates, opt_state = opt.update(gradient, opt_state)
    new_params = optax.apply_updates(params, updates)
    return new_params, opt_state

  def output_samples(params: Params, max_samples: int):
    """Output some cases where the policy disagrees with the dataset action."""
    if max_samples == 0:
      return
    count = 0
    with open(os.path.join(FLAGS.data_path, 'test.txt')) as f:
      lines = list(f)
    np.random.shuffle(lines)
    for line in lines:
      state = GAME.new_initial_state()
      actions = _trajectory(line)
      for action in actions:
        if not state.is_chance_node():
          observation = np.array(state.information_state_tensor(), np.float32)
          policy = np.exp(net.apply(params, observation))
          probs_actions = [(p, a) for a, p in enumerate(policy)]
          pred = max(probs_actions)[1]
          if pred != action:
            print(state)
            for p, a in reversed(sorted(probs_actions)[-TOP_K_ACTIONS:]):
              print('{:7} {:.2f}'.format(state.action_to_string(a), p))
            print('Ground truth {}\n'.format(state.action_to_string(action)))
            count += 1
            break
        state.apply_action(action)
      if count >= max_samples:
        return

  # Store what we need to rebuild the Haiku net.
  if FLAGS.save_path:
    filename = os.path.join(FLAGS.save_path, 'layers.txt')
    with open(filename, 'w') as layer_def_file:
      for s in FLAGS.hidden_layer_sizes:
        layer_def_file.write(f'{s} ')
      layer_def_file.write('\n')

  # Make datasets.
  if FLAGS.data_path is None:
    raise app.UsageError(
        'Please generate your own supervised training data and supply the local'
        'location as --data_path')
  train = batch(
      make_dataset(os.path.join(FLAGS.data_path, 'train.txt')),
      FLAGS.train_batch)
  test = batch(
      make_dataset(os.path.join(FLAGS.data_path, 'test.txt')), FLAGS.eval_batch)

  # Initialize network and optimiser.
  if FLAGS.checkpoint_file:
    with open(FLAGS.checkpoint_file, 'rb') as pkl_file:
      params, opt_state = pickle.load(pkl_file)
  else:
    rng = jax.random.PRNGKey(FLAGS.rng_seed)  # seed used for network weights
    inputs, unused_targets = next(train)
    params = net.init(rng, inputs)
    opt_state = opt.init(params)

  # Train/eval loop.
  for step in range(FLAGS.iterations):
    # Do SGD on a batch of training examples.
    inputs, targets = next(train)
    params, opt_state = update(params, opt_state, inputs, targets)

    # Periodically evaluate classification accuracy on the test set.
    if (1 + step) % FLAGS.eval_every == 0:
      inputs, targets = next(test)
      test_accuracy = accuracy(params, inputs, targets)
      print(f'After {1+step} steps, test accuracy: {test_accuracy}.')
      if FLAGS.save_path:
        filename = os.path.join(FLAGS.save_path, f'checkpoint-{1 + step}.pkl')
        with open(filename, 'wb') as pkl_file:
          pickle.dump((params, opt_state), pkl_file)
      output_samples(params, FLAGS.num_examples)


def main(_):
  env = rl_environment.Environment(FLAGS.game)
  num_players = env.num_players
  num_actions = env.action_spec()["num_actions"]

  agents = []
  if FLAGS.epsilon_schedule is not None:
    for idx in range(num_players):
      agents.append(
          tabular_qlearner.QLearner(
              player_id=idx,
              num_actions=num_actions,
              epsilon_schedule=create_epsilon_schedule(FLAGS.epsilon_schedule)))
  else:
    agents = [
        tabular_qlearner.QLearner(player_id=idx, num_actions=num_actions)
        for idx in range(num_players)
    ]

  # 1. Train the agents
  training_episodes = FLAGS.num_train_episodes
  for cur_episode in range(training_episodes):
    if cur_episode % int(FLAGS.eval_freq) == 0:
      avg_rewards = eval_agents(env, agents, FLAGS.num_eval_episodes)
      print("Training episodes: {}, Avg rewards: {}".format(
          cur_episode, avg_rewards))
    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      agent_output = agents[player_id].step(time_step)
      time_step = env.step([agent_output.action])

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)


def main(_):
  game = pyspiel.load_game(FLAGS.game)
  evaluator = pyspiel.RandomRolloutEvaluator(1, SEED)
  min_expl = game.max_utility() -  game.min_utility()

  print("{:>5} {:>10} {:>50} {:>20}".format(
      "max_sims", "uct_c", "final_policy_type", "exploitability"))
  for max_simulations in [10, 100, 1000, 10000]:
    for uct_c in [0.2, 0.5, 1.0, 2.0, 4.0]:  # These values are for Kuhn.
      for final_policy_type in [
          pyspiel.ISMCTSFinalPolicyType.NORMALIZED_VISIT_COUNT,
          pyspiel.ISMCTSFinalPolicyType.MAX_VISIT_COUNT,
          pyspiel.ISMCTSFinalPolicyType.MAX_VALUE
      ]:
        tabular_policy = policy.TabularPolicy(game)
        bot = pyspiel.ISMCTSBot(SEED, evaluator, uct_c, max_simulations, -1,
                                final_policy_type, False, False)
        searched = {}
        construct_is_mcts_policy(game, game.new_initial_state(), tabular_policy,
                                 bot, searched)
        expl = exploitability.exploitability(game, tabular_policy)
        print("{:>5} {:>10} {:>50} {:>20}".format(max_simulations, uct_c,
                                                  str(final_policy_type), expl))
        if expl < min_expl:
          min_expl = expl
  print("Min expl: {}".format(min_expl))


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  game = get_game(FLAGS.game)
  jpsro.run_loop(
      game=game,
      game_name=FLAGS.game,
      seed=FLAGS.seed,
      iterations=FLAGS.iterations,
      policy_init=FLAGS.policy_init,
      update_players_strategy=FLAGS.update_players_strategy,
      target_equilibrium=FLAGS.target_equilibrium,
      br_selection=FLAGS.br_selection,
      train_meta_solver=FLAGS.train_meta_solver,
      eval_meta_solver=FLAGS.eval_meta_solver,
      action_value_tolerance=FLAGS.action_value_tolerance,
      ignore_repeats=FLAGS.ignore_repeats)


def main(_):
  game = pyspiel.load_game("kuhn_poker")

  cfr_solver = cfr.CFRSolver(game)
  iterations = 1000

  for i in range(iterations):
    cfr_value = cfr_solver.evaluate_and_update_policy()
    print("Game util at iteration {}: {}".format(i, cfr_value))

  average_policy = cfr_solver.average_policy()
  average_policy_values = expected_game_score.policy_value(
      game.new_initial_state(), [average_policy] * 2)
  print("Computed player 0 value: {}".format(average_policy_values[0]))
  print("Expected player 0 value: {}".format(-1 / 18))


def main(_):
  game = "lewis_signaling"
  num_players = 2

  num_states = FLAGS.num_states
  num_messages = FLAGS.num_messages
  if FLAGS.payoffs == "random":
    payoffs = np.random.random((num_states, num_states))
    payoffs_str = ",".join([str(x) for x in payoffs.flatten()])
  elif FLAGS.payoffs == "climbing":
    # This is a particular payoff matrix that is hard for decentralized
    # algorithms. Introduced in C. Claus and C. Boutilier, "The dynamics of
    # reinforcement learning in cooperative multiagent systems", 1998, for
    # simultaneous action games, but it is difficult even in the case of
    # signaling games.
    payoffs = np.array([[11, -30, 0], [-30, 7, 6], [0, 0, 5]]) / 30
    payoffs_str = ",".join([str(x) for x in payoffs.flatten()])
  else:
    payoffs_str = FLAGS.payoffs
    try:
      payoffs_list = [float(x) for x in payoffs_str.split(",")]
      payoffs = np.array(payoffs_list).reshape((num_states, num_states))
    except ValueError:
      raise ValueError(
          "There should be {} (states * actions) elements in payoff. Found {} elements"
          .format(num_states * num_states, len(payoffs_list))) from None

  env_configs = {
      "num_states": num_states,
      "num_messages": num_messages,
      "payoffs": payoffs_str
  }

  env = rl_environment.Environment(game, **env_configs)

  if FLAGS.compare:
    rewards_list = []
    opts_list = []
    converge_point_list = []
    percent_opt_list = []
    for centralized in [True, False]:
      rewards, opts, converge_point, percent_opt = run_experiment(
          num_players, env, payoffs, centralized)
      rewards_list += [rewards]
      opts_list += [opts]
      converge_point_list += [converge_point]
      percent_opt_list += [percent_opt]
  else:
    rewards, opts, converge_point, percent_opt = run_experiment(
        num_players, env, payoffs, FLAGS.centralized)
    rewards_list = [rewards]
    opts_list = [opts]
    converge_point_list = [converge_point]
    percent_opt_list = [percent_opt]

  if FLAGS.plot:
    # pylint: disable=g-import-not-at-top
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from scipy import stats

    params = {
        "font.size": 12,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
    }
    mpl.rcParams.update(params)

    def init_fig():
      fig, ax = plt.subplots(1, 1)
      ax.spines["top"].set_visible(False)
      ax.spines["right"].set_visible(False)
      return fig, ax

    def plot_scalars(scalars,
                     repetition_axis=0,
                     scalar_labels=None,
                     title=None,
                     ax_labels=None):
      """Plots scalar on ax by filling 1 standard error.

      Args:
          scalars: List of scalars to plot (mean taken over repetition
            axis)
          repetition_axis: Axis to take the mean over
          scalar_labels: Labels for the scalars (for legend)
          title: Figure title
          ax_labels: Labels for x and y axis (list of 2 strings)
      """
      if not all([len(s.shape) == 2 for s in scalars]):
        raise ValueError("Only 2D arrays supported for plotting")

      if scalar_labels is None:
        scalar_labels = [None] * len(scalars)

      if len(scalars) != len(scalar_labels):
        raise ValueError(
            "Wrong number of scalar labels, expected {} but received {}".format(
                len(scalars), len(scalar_labels)))

      _, plot_axis = init_fig()
      for i, scalar in enumerate(scalars):
        xs = np.arange(scalar.shape[1 - repetition_axis]) * FLAGS.log_interval
        mean = scalar.mean(axis=repetition_axis)
        sem = stats.sem(scalar, axis=repetition_axis)
        plot_axis.plot(xs, mean, label=scalar_labels[i])
        plot_axis.fill_between(xs, mean - sem, mean + sem, alpha=0.5)

      if title is not None:
        plot_axis.set_title(title)
      if ax_labels is not None:
        plot_axis.set_xlabel(ax_labels[0])
        plot_axis.set_ylabel(ax_labels[1])

    def plot_confusion_matrix(cm, cmap=plt.cm.Blues, title=None):
      """Plots the confusion matrix.

      Args:
          cm (np.ndarray): Confusion matrix to plot
          cmap: Color map to be used in matplotlib's imshow
          title: Figure title

      Returns:
          Figure and axis on which the confusion matrix is plotted
      """
      fig, ax = plt.subplots()
      ax.imshow(cm, interpolation="nearest", cmap=cmap)
      ax.set_xticks([])
      ax.set_yticks([])
      ax.set_xlabel("Receiver's action", fontsize=14)
      ax.set_ylabel("Sender's state", fontsize=14)
      # Loop over data dimensions and create text annotations.
      fmt = "d"
      thresh = cm.max() / 2.
      for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
          ax.text(
              j,
              i,
              format(cm[i, j], fmt),
              ha="center",
              va="center",
              color="white" if cm[i, j] > thresh else "black")
      fig.tight_layout()
      if title is not None:
        ax.set_title(title)
      return fig, ax

    if FLAGS.compare:
      labels = ["Centralized", "Decentralized"]
    else:
      labels = ["Centralized"] if FLAGS.centralized else ["Decentralized"]
    plot_scalars(
        rewards_list,
        scalar_labels=labels,
        title="Reward graph (Tabular Q-Learning)",
        ax_labels=["Episodes", "Reward per episode"])
    plt.legend()
    plot_scalars(
        opts_list,
        scalar_labels=labels,
        title="Percentage of optimal actions (Tabular Q-Learning)",
        ax_labels=["Episodes", "% optimal actions"])
    plt.legend()

    for i, cp in enumerate(converge_point_list):
      plot_confusion_matrix(
          cp.astype(int),
          title="Final policy (Tabular {})".format(labels[i]))

    plt.show()

  return percent_opt_list


def main(_):
  # lp_solver.solve_zero_sum_matrix_game(pyspiel.load_matrix_game("matrix_mp"))
  # lp_solver.solve_zero_sum_matrix_game(pyspiel.load_matrix_game("matrix_rps"))
  p0_sol, p1_sol, p0_sol_val, p1_sol_val = lp_solver.solve_zero_sum_matrix_game(
      pyspiel.create_matrix_game(
          [[0.0, -0.25, 0.5], [0.25, 0.0, -0.05], [-0.5, 0.05, 0.0]],
          [[0.0, 0.25, -0.5], [-0.25, 0.0, 0.05], [0.5, -0.05, 0.0]]))
  print("p0 val = {}, policy = {}".format(p0_sol_val, p0_sol))
  print("p1 val = {}, policy = {}".format(p1_sol_val, p1_sol))

  payoff_matrix = [[1., 1., 1.], [2., 0., 1.], [0., 2., 2.]]
  mixture = lp_solver.is_dominated(
      0,
      payoff_matrix,
      0,
      lp_solver.DominanceType.DOMINANCE_WEAK,
      return_mixture=True,
  )
  print("mixture strategy : {}".format(mixture))
  print("payoff vector    : {}".format(mixture.dot(payoff_matrix)))


def main(_):
  games_list = pyspiel.registered_games()
  print("Registered games:")
  print(games_list)

  # Load a two-player normal-form game as a two-player matrix game.
  blotto_matrix_game = pyspiel.load_matrix_game("blotto")
  print("Number of rows in 2-player Blotto with default settings is {}".format(
      blotto_matrix_game.num_rows()))

  # Several ways to load/create the same game of matching pennies.
  print("Creating matrix game...")
  game = pyspiel.load_matrix_game("matrix_mp")
  game = _manually_create_game()
  game = _import_data_create_game()
  game = _easy_create_game()
  game = _even_easier_create_game()

  # Quick test: inspect top-left utility values:
  print("Values for joint action ({},{}) is {},{}".format(
      game.row_action_name(0), game.col_action_name(0),
      game.player_utility(0, 0, 0), game.player_utility(1, 0, 0)))

  state = game.new_initial_state()

  # Print the initial state
  print("State:")
  print(str(state))

  assert state.is_simultaneous_node()

  # Simultaneous node: sample actions for all players.
  chosen_actions = [
      random.choice(state.legal_actions(pid))
      for pid in range(game.num_players())
  ]
  print("Chosen actions: ", [
      state.action_to_string(pid, action)
      for pid, action in enumerate(chosen_actions)
  ])
  state.apply_actions(chosen_actions)

  assert state.is_terminal()

  # Game is now done. Print utilities for each player
  returns = state.returns()
  for pid in range(game.num_players()):
    print("Utility for player {} is {}".format(pid, returns[pid]))


def main(_):
  game = pyspiel.load_game(FLAGS.game)
  print("loaded game")

  # convert game to matrix form if it isn't already a matrix game
  if not isinstance(game, pyspiel.MatrixGame):
    game = pyspiel.extensive_to_matrix_game(game)
    num_rows, num_cols = game.num_rows(), game.num_cols()
    print("converted to matrix form with shape (%d, %d)" % (num_rows, num_cols))

  # use iterated dominance to reduce the space unless the solver is LP (fast)
  if FLAGS.solver != "linear":
    if FLAGS.mode == "all":
      game, _ = lp_solver.iterated_dominance(
          game, tol=FLAGS.tol, mode=lp_solver.DominanceType.DOMINANCE_STRICT
      )
      num_rows, num_cols = game.num_rows(), game.num_cols()
      print("discarded strictly dominated actions yielding shape (%d, %d)" %
            (num_rows, num_cols))
    if FLAGS.mode == "one":
      game, _ = lp_solver.iterated_dominance(
          game, tol=FLAGS.tol, mode=lp_solver.DominanceType.DOMINANCE_VERY_WEAK
      )
      num_rows, num_cols = game.num_rows(), game.num_cols()
      print("discarded very weakly dominated actions yielding shape (%d, %d)" %
            (num_rows, num_cols))

  # game is now finalized
  equilibria = None
  num_rows, num_cols = game.num_rows(), game.num_cols()
  row_actions = [game.row_action_name(row) for row in range(num_rows)]
  col_actions = [game.col_action_name(col) for col in range(num_cols)]
  row_payoffs, col_payoffs = utils.game_payoffs_array(game)
  pure_nash = list(
      zip(*((row_payoffs >= row_payoffs.max(0, keepdims=True) - FLAGS.tol)
            & (col_payoffs >= col_payoffs.max(1, keepdims=True) - FLAGS.tol)
           ).nonzero()))
  if pure_nash:
    print("found %d pure equilibria" % len(pure_nash))
  if FLAGS.mode == "pure":
    if not pure_nash:
      print("found no pure equilibria")
      return
    print("pure equilibria:")
    for row, col in pure_nash:
      print("payoffs %f, %f:" % (row_payoffs[row, col], col_payoffs[row, col]))
      print("row action:")
      print(row_actions[row])
      print("col action:")
      print(col_actions[col])
      print("")
    return
  if FLAGS.mode == "one" and pure_nash:
    print("pure equilibrium:")
    row, col = pure_nash[0]
    print("payoffs %f, %f:" % (row_payoffs[row, col], col_payoffs[row, col]))
    print("row action:")
    print(row_actions[row])
    print("col action:")
    print(col_actions[col])
    print("")
    return
  for row, action in enumerate(row_actions):
    print("row action %s:" % row)
    print(action)
  print("--")
  for col, action in enumerate(col_actions):
    print("col action %s:" % col)
    print(action)
  print("--")
  if num_rows == 1 or num_cols == 1:
    equilibria = itertools.product(np.eye(num_rows), np.eye(num_cols))
  elif FLAGS.solver == "linear":
    if FLAGS.mode != "one" or (row_payoffs + col_payoffs).max() > (
        row_payoffs + col_payoffs).min() + FLAGS.tol:
      raise ValueError("can't use linear solver for non-constant-sum game or "
                       "for finding all optima!")
    print("using linear solver")

    def gen():
      p0_sol, p1_sol, _, _ = lp_solver.solve_zero_sum_matrix_game(
          pyspiel.create_matrix_game(row_payoffs - col_payoffs,
                                     col_payoffs - row_payoffs))
      yield (np.squeeze(p0_sol, 1), np.squeeze(p1_sol, 1))

    equilibria = gen()
  elif FLAGS.solver == "lrsnash":
    print("using lrsnash solver")
    equilibria = matrix_nash.lrs_solve(row_payoffs, col_payoffs,
                                       FLAGS.lrsnash_max_denom,
                                       FLAGS.lrsnash_path)
  elif FLAGS.solver == "nashpy":
    if FLAGS.mode == "all":
      print("using nashpy vertex enumeration")
      equilibria = nashpy.Game(row_payoffs, col_payoffs).vertex_enumeration()
    else:
      print("using nashpy Lemke-Howson solver")
      equilibria = matrix_nash.lemke_howson_solve(row_payoffs, col_payoffs)
  print("equilibria:" if FLAGS.mode == "all" else "an equilibrium:")
  assert equilibria is not None
  equilibria = iter(equilibria)
  # check that there's at least one equilibrium
  try:
    equilibria = itertools.chain([next(equilibria)], equilibria)
  except StopIteration:
    print("not found!")
  for row_mixture, col_mixture in equilibria:
    print("payoffs %f, %f for %s, %s" %
          (row_mixture.dot(row_payoffs.dot(col_mixture)),
           row_mixture.dot(
               col_payoffs.dot(col_mixture)), row_mixture, col_mixture))
    if FLAGS.mode == "one":
      return


def main(_):
  game = pyspiel.load_game(
      FLAGS.game,
      {"players": FLAGS.players},
  )

  if FLAGS.sampling == "external":
    solver = pyspiel.ExternalSamplingMCCFRSolver(
        game,
        avg_type=pyspiel.MCCFRAverageType.FULL,
    )
  elif FLAGS.sampling == "outcome":
    solver = pyspiel.OutcomeSamplingMCCFRSolver(game)

  run_iterations(game, solver)

  print("Persisting the model...")
  with open(MODEL_FILE_NAME.format(FLAGS.sampling), "wb") as file:
    pickle.dump(solver, file, pickle.HIGHEST_PROTOCOL)

  print("Loading the model...")
  with open(MODEL_FILE_NAME.format(FLAGS.sampling), "rb") as file:
    loaded_solver = pickle.load(file)
  print("Exploitability of the loaded model: {:.6f}".format(
      pyspiel.exploitability(game, loaded_solver.average_policy())))

  run_iterations(game, solver, start_iteration=int(FLAGS.iterations / 2))


def main(_):
  game = pyspiel.load_game(FLAGS.game, {"players": FLAGS.players})
  if FLAGS.sampling == "external":
    cfr_solver = external_mccfr.ExternalSamplingSolver(
        game, external_mccfr.AverageType.SIMPLE)
  else:
    cfr_solver = outcome_mccfr.OutcomeSamplingSolver(game)
  for i in range(FLAGS.iterations):
    cfr_solver.iteration()
    if i % FLAGS.print_freq == 0:
      conv = exploitability.nash_conv(game, cfr_solver.average_policy())
      print("Iteration {} exploitability {}".format(i, conv))


def main(argv):
  game = pyspiel.load_game(FLAGS.game)
  if game.num_players() > 2:
    sys.exit("This game requires more players than the example can handle.")
  bots = [
      _init_bot(FLAGS.player1, game, 0),
      _init_bot(FLAGS.player2, game, 1),
  ]
  histories = collections.defaultdict(int)
  overall_returns = [0, 0]
  overall_wins = [0, 0]
  game_num = 0
  try:
    for game_num in range(FLAGS.num_games):
      returns, history = _play_game(game, bots, argv[1:])
      histories[" ".join(history)] += 1
      for i, v in enumerate(returns):
        overall_returns[i] += v
        if v > 0:
          overall_wins[i] += 1
  except (KeyboardInterrupt, EOFError):
    game_num -= 1
    print("Caught a KeyboardInterrupt, stopping early.")
  print("Number of games played:", game_num + 1)
  print("Number of distinct games played:", len(histories))
  print("Players:", FLAGS.player1, FLAGS.player2)
  print("Overall wins", overall_wins)
  print("Overall returns", overall_returns)


def main(_):
  print("Creating game.")
  game = pyspiel.load_game(FLAGS.game_string)
  state = game.new_initial_state()
  print(state)

  print("Creating minimax oracle and solving.")
  solver = minimax_solver.MinimaxSolver(FLAGS.game_string)
  solver.solve()

  print("Playing game.")
  while not state.is_terminal():
    print("")
    print(state)
    # Decision node: sample action for the single current player
    action_values = solver.action_values_from_state(state)
    best_value = float("-inf")
    best_action = pyspiel.INVALID_ACTION
    for action in state.legal_actions():
      action_value = action_values[action]
      print(
          f"Action {state.action_to_string(action)} "
          + f"has minimax value: {action_value}"
      )
      if action_value > best_value:
        best_value = action_value
        best_action = action
    print(
        f"Applying action {best_action}: "
        + f"{state.action_to_string(best_action)}"
    )
    state.apply_action(best_action)

  # Game is now done. Print utilities for each player
  print("")
  print(str(state))
  returns = state.returns()
  for pid in range(game.num_players()):
    print("Utility for player {} is {}".format(pid, returns[pid]))


def main(_):
  game = pyspiel.load_game(FLAGS.game)
  mmd = mmd_dilated.MMDDilatedEnt(game, FLAGS.alpha)

  for i in range(FLAGS.iterations):
    mmd.update_sequences()
    if i % FLAGS.print_freq == 0:
      conv = mmd.get_gap()
      print("Iteration {} gap {}".format(i, conv))


def main(_):
  mmd = mmd_dilated.MMDDilatedEnt(game, FLAGS.alpha)
  for i in range(FLAGS.iterations):
    mmd.update_sequences()
    if i % FLAGS.print_freq == 0:
      conv = mmd.get_gap()
      print("Iteration {} gap {}".format(i, conv))

  # Extract policies for both players
  print(mmd.get_policies().action_probability_array)
  # Note the sequence form and behavioural-form coincide
  # for a normal-form game (sequence form has extra root value of 1)
  print(mmd.current_sequences())


def main(_):
  game = pyspiel.load_game(FLAGS.game)
  # need to manually set stepsize if alpha = 0
  mmd = mmd_dilated.MMDDilatedEnt(game, alpha=0, stepsize=1)

  for i in range(FLAGS.iterations):
    mmd.update_sequences()
    if i % FLAGS.print_freq == 0:
      conv = exploitability.exploitability(game, mmd.get_avg_policies())
      print("Iteration {} exploitability {}".format(i, conv))


def main(_):
  assert FLAGS.data_file is not None
  _, negotiations = parse_dataset(FLAGS.data_file)

  print(f"Writing instances database: {FLAGS.instances_file}")
  write_instances_file(negotiations, FLAGS.instances_file)

  # Human averages + NBS
  human_rewards = np.zeros(2, dtype=np.float64)
  avg_human_nbs = 0
  for neg in negotiations:
    human_rewards += neg.rewards
  human_rewards /= len(negotiations)
  avg_human_nbs += np.prod(human_rewards)
  print(f"Average human rewards: {human_rewards}")
  print(f"Average human NBS: {avg_human_nbs}")

  game = pyspiel.load_game("bargaining",
                           {"instances_file": FLAGS.instances_file})

  # Max bot
  bots = [MaxBot(), MaxBot()]
  avg_max_nbs = compute_nbs_from_simulations(game, 6796, bots)
  print(f"Average max NBS: {avg_max_nbs}")

  # Uniform random NBS
  bots = [
      pyspiel.make_uniform_random_bot(0, np.random.randint(0, 1000000)),
      pyspiel.make_uniform_random_bot(1, np.random.randint(0, 1000000)),
  ]
  avg_uniform_nbs = compute_nbs_from_simulations(game, 6796, bots)
  print(f"Average uniform NBS: {avg_uniform_nbs}")

  # IS-MCTS NBS
  evaluator = pyspiel.RandomRolloutEvaluator(1, np.random.randint(0, 1000000))
  bots = [
      pyspiel.ISMCTSBot(
          np.random.randint(0, 1000000), evaluator, 10.0, 1000, -1,
          pyspiel.ISMCTSFinalPolicyType.MAX_VISIT_COUNT, False, False),
      pyspiel.ISMCTSBot(
          np.random.randint(0, 1000000), evaluator, 10.0, 1000, -1,
          pyspiel.ISMCTSFinalPolicyType.MAX_VISIT_COUNT, False, False)
  ]
  avg_ismcts_nbs = compute_nbs_from_simulations(game, 6796, bots)
  print(f"Average IS-MCTS NBS: {avg_ismcts_nbs}")


def main(_):
  game = pyspiel.load_game(FLAGS.game)
  nfg_text = pyspiel.game_to_nfg_string(game)

  if FLAGS.outfile is None:
    print(nfg_text)
  else:
    print("Exporting to {}".format(FLAGS.outfile))
    outfile = open(FLAGS.outfile, "w")
    outfile.write(nfg_text)
    outfile.close()


def main(unused_argv):
  game = "kuhn_poker"
  num_players = 2

  env_configs = {"players": num_players}
  env = rl_environment.Environment(game, **env_configs)
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  hidden_layers_sizes = [int(s) for s in FLAGS.hidden_layers_sizes]
  kwargs = {
      "replay_buffer_capacity": FLAGS.replay_buffer_capacity,
      "epsilon_decay_duration": FLAGS.num_train_episodes,
      "epsilon_start": 0.06,
      "epsilon_end": 0.001,
  }

  # pylint: disable=g-complex-comprehension
  agents = [
      nfsp.NFSP(
          idx,
          info_state_size,
          num_actions,
          hidden_layers_sizes,
          FLAGS.reservoir_buffer_capacity,
          FLAGS.anticipatory_param,
          **kwargs
      )
      for idx in range(num_players)
  ]
  expl_policies_avg = NFSPPolicies(env, agents, nfsp.MODE.AVERAGE_POLICY)

  for ep in range(FLAGS.num_train_episodes):
    if (ep + 1) % FLAGS.eval_every == 0:
      losses = [agent.loss for agent in agents]
      logging.info("Losses: %s", losses)
      expl = exploitability.exploitability(env.game, expl_policies_avg)
      logging.info("[%s] Exploitability AVG %s", ep + 1, expl)
      logging.info("_____________________________________________")

    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      agent_output = agents[player_id].step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)


def main(unused_argv):
  game = "kuhn_poker"
  num_players = 2

  env_configs = {"players": num_players}
  env = rl_environment.Environment(game, **env_configs)
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  hidden_layers_sizes = [int(s) for s in FLAGS.hidden_layers_sizes]
  kwargs = {
      "replay_buffer_capacity": FLAGS.replay_buffer_capacity,
      "epsilon_decay_duration": FLAGS.num_train_episodes,
      "epsilon_start": 0.06,
      "epsilon_end": 0.001,
  }

  # pylint: disable=g-complex-comprehension
  agents = [
      nfsp.NFSP(
          idx,
          info_state_size,
          num_actions,
          hidden_layers_sizes,
          FLAGS.reservoir_buffer_capacity,
          FLAGS.anticipatory_param,
          **kwargs
      )
      for idx in range(num_players)
  ]
  expl_policies_avg = NFSPPolicies(env, agents, nfsp.MODE.AVERAGE_POLICY)

  for ep in range(FLAGS.num_train_episodes):
    if (ep + 1) % FLAGS.eval_every == 0:
      losses = [agent.loss for agent in agents]
      logging.info("Losses: %s", losses)
      expl = exploitability.exploitability(env.game, expl_policies_avg)
      logging.info("[%s] Exploitability AVG %s", ep + 1, expl)
      logging.info("_____________________________________________")

    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      agent_output = agents[player_id].step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)


def main(unused_argv):
  logging.info("Loading %s", FLAGS.game_name)
  game = FLAGS.game_name
  num_players = FLAGS.num_players

  env_configs = {"players": num_players}
  env = rl_environment.Environment(game, **env_configs)
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  hidden_layers_sizes = [int(s) for s in FLAGS.hidden_layers_sizes]

  kwargs = {
      "replay_buffer_capacity": FLAGS.replay_buffer_capacity,
      "reservoir_buffer_capacity": FLAGS.reservoir_buffer_capacity,
      "min_buffer_size_to_learn": FLAGS.min_buffer_size_to_learn,
      "anticipatory_param": FLAGS.anticipatory_param,
      "batch_size": FLAGS.batch_size,
      "learn_every": FLAGS.learn_every,
      "rl_learning_rate": FLAGS.rl_learning_rate,
      "sl_learning_rate": FLAGS.sl_learning_rate,
      "optimizer_str": FLAGS.optimizer_str,
      "loss_str": FLAGS.loss_str,
      "update_target_network_every": FLAGS.update_target_network_every,
      "discount_factor": FLAGS.discount_factor,
      "epsilon_decay_duration": FLAGS.epsilon_decay_duration,
      "epsilon_start": FLAGS.epsilon_start,
      "epsilon_end": FLAGS.epsilon_end,
  }

  # pylint: disable=g-complex-comprehension
  agents = [
      nfsp.NFSP(
          idx, info_state_size, num_actions, hidden_layers_sizes, **kwargs
      )
      for idx in range(num_players)
  ]
  joint_avg_policy = NFSPPolicies(env, agents, nfsp.MODE.AVERAGE_POLICY)

  if FLAGS.use_checkpoints:
    for agent in agents:
      agent.restore(FLAGS.checkpoint_dir)

  for ep in range(FLAGS.num_train_episodes):
    if (ep + 1) % FLAGS.eval_every == 0:
      losses = [agent.loss for agent in agents]
      logging.info("Losses: %s", losses)
      if FLAGS.evaluation_metric == "exploitability":
        # Avg exploitability is implemented only for 2 players constant-sum
        # games, use nash_conv otherwise.
        expl = exploitability.exploitability(env.game, joint_avg_policy)
        logging.info("[%s] Exploitability AVG %s", ep + 1, expl)
      elif FLAGS.evaluation_metric == "nash_conv":
        nash_conv = exploitability.nash_conv(env.game, joint_avg_policy)
        logging.info("[%s] NashConv %s", ep + 1, nash_conv)
      else:
        raise ValueError(
            " ".join((
                "Invalid evaluation metric, choose from",
                "'exploitability', 'nash_conv'.",
            ))
        )
      if FLAGS.use_checkpoints:
        for agent in agents:
          agent.save(FLAGS.checkpoint_dir)
      logging.info("_____________________________________________")

    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      agent_output = agents[player_id].step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)


def main(unused_argv):
  if FLAGS.update_path:
    generate_playthrough.update_path(FLAGS.update_path, FLAGS.shard,
                                     FLAGS.num_shards)
  else:
    if not FLAGS.game:
      raise ValueError("Must specify game")
    actions = FLAGS.actions
    if actions is not None:
      actions = [int(x) for x in actions]
    text = generate_playthrough.playthrough(
        FLAGS.game, actions, alsologtostdout=FLAGS.alsologtostdout)
    if FLAGS.output_file:
      with open(FLAGS.output_file, "w") as f:
        f.write(text)
    else:
      logging.info(text)


def main(argv):
  del argv
  game = pyspiel.load_game(FLAGS.game_name)

  # TODO(author1): Add support for bots from neural networks.
  bots = [
      uniform_random.UniformRandomBot(i, random)
      for i in range(game.num_players())
  ]
  scenarios.play_bot_in_scenarios(game, bots)


def main(_):
  game = pyspiel.load_game(_GAME_STRING.value)
  state = game.new_initial_state()
  bots = []
  bots.append(load_bot(_PLAYER0_TYPE.value, 0))
  bots.append(load_bot(_PLAYER1_TYPE.value, 1))
  play_game(state, bots)


def main(_):
  rng = np.random.RandomState(FLAGS.seed)

  # Make sure poker is compiled into the library, as it requires an optional
  # dependency: the ACPC poker code. To ensure it is compiled in, prepend both
  # the install.sh and build commands with OPEN_SPIEL_BUILD_WITH_ACPC=ON.
  # See here:
  # https://github.com/deepmind/open_spiel/blob/master/docs/install.md#configuration-conditional-dependencies
  # for more details on optional dependencies.
  games_list = pyspiel.registered_names()
  assert "universal_poker" in games_list

  fcpa_game_string = pyspiel.hunl_game_string("fcpa")
  print("Creating game: {}".format(fcpa_game_string))
  game = pyspiel.load_game(fcpa_game_string)

  agents = [
      LoadAgent(FLAGS.player0, game, 0, rng),
      LoadAgent(FLAGS.player1, game, 1, rng)
  ]

  state = game.new_initial_state()

  # Print the initial state
  print("INITIAL STATE")
  print(str(state))

  while not state.is_terminal():
    # The state can be three different types: chance node,
    # simultaneous node, or decision node
    current_player = state.current_player()
    if state.is_chance_node():
      # Chance node: sample an outcome
      outcomes = state.chance_outcomes()
      num_actions = len(outcomes)
      print("Chance node with " + str(num_actions) + " outcomes")
      action_list, prob_list = zip(*outcomes)
      action = rng.choice(action_list, p=prob_list)
      print("Sampled outcome: ",
            state.action_to_string(state.current_player(), action))
      state.apply_action(action)
    else:
      # Decision node: sample action for the single current player
      legal_actions = state.legal_actions()
      for action in legal_actions:
        print("Legal action: {} ({})".format(
            state.action_to_string(current_player, action), action))
      action = agents[current_player].step(state)
      action_string = state.action_to_string(current_player, action)
      print("Player ", current_player, ", chose action: ",
            action_string)
      state.apply_action(action)

    print("")
    print("NEXT STATE:")
    print(str(state))

  # Game is now done. Print utilities for each player
  returns = state.returns()
  for pid in range(game.num_players()):
    print("Utility for player {} is {}".format(pid, returns[pid]))


def main(unused_argv):
  env = rl_environment.Environment(FLAGS.game_name)

  policies = [[  # pylint: disable=g-complex-comprehension
      policy.TabularPolicy(env.game).copy_with_noise(alpha=float(i), beta=1.0)
      for i in range(2)
  ] for _ in range(2)]

  probabilities = [
      list(np.ones(len(policies[i])) / len(policies[i])) for i in range(2)
  ]

  pol_ag = policy_aggregator.PolicyAggregator(env.game)
  aggr_policies = pol_ag.aggregate([0, 1], policies, probabilities)

  exploitabilities = exploitability.nash_conv(env.game, aggr_policies)
  print("Exploitability : {}".format(exploitabilities))

  print(policies[0][0].action_probability_array)
  print(policies[0][1].action_probability_array)
  print(aggr_policies.policy)

  print("\nCopy Example")

  mother_policy = policy.TabularPolicy(env.game).copy_with_noise(1, 10)
  policies = [[mother_policy.__copy__() for _ in range(2)] for _ in range(2)]
  probabilities = [
      list(np.ones(len(policies)) / len(policies)) for _ in range(2)
  ]

  pol_ag = policy_aggregator.PolicyAggregator(env.game)
  aggr_policy = pol_ag.aggregate([0], policies, probabilities)

  for state, value in aggr_policy.policy[0].items():
    polici = mother_policy.policy_for_key(state)

    value_normal = {
        action: probability
        for action, probability in enumerate(polici)
        if probability > 0
    }
    for key in value.keys():
      print("State : {}. Key : {}. Aggregated : {}. Real : {}. Passed : {}"
            .format(state, key, value[key], value_normal[key],
                    np.abs(value[key] - value_normal[key]) < 1e-8))


def main(_):
  setup_logging()

  batch_size = int(FLAGS.num_envs * FLAGS.num_steps)

  if FLAGS.game_name == "atari":
    # pylint: disable=unused-import
    # pylint: disable=g-import-not-at-top
    import open_spiel.python.games.atari

  current_day = datetime.now().strftime("%d")
  current_month_text = datetime.now().strftime("%h")
  run_name = f"{FLAGS.game_name}__{FLAGS.exp_name}__"
  if FLAGS.game_name == "atari":
    run_name += f"{FLAGS.gym_id}__"
  run_name += f"{FLAGS.seed}__{current_month_text}__{current_day}__{int(time.time())}"

  writer = SummaryWriter(f"runs/{run_name}")
  writer.add_text(
      "hyperparameters",
      "|param|value|\n|-|-|\n%s" %
      ("\n".join([f"|{key}|{value}|" for key, value in vars(FLAGS).items()])),
  )

  random.seed(FLAGS.seed)
  np.random.seed(FLAGS.seed)
  torch.manual_seed(FLAGS.seed)
  torch.backends.cudnn.deterministic = FLAGS.torch_deterministic

  device = torch.device(
      "cuda" if torch.cuda.is_available() and FLAGS.cuda else "cpu")
  logging.info("Using device: %s", str(device))

  if FLAGS.game_name == "atari":
    envs = SyncVectorEnv([
        make_single_atari_env(FLAGS.gym_id, FLAGS.seed + i, i, False,
                              run_name)() for i in range(FLAGS.num_envs)
    ])
    agent_fn = PPOAtariAgent
  else:
    envs = SyncVectorEnv([
        make_single_env(FLAGS.game_name, FLAGS.seed + i)()
        for i in range(FLAGS.num_envs)
    ])
    agent_fn = PPOAgent

  game = envs.envs[0]._game  # pylint: disable=protected-access
  info_state_shape = game.observation_tensor_shape()

  num_updates = FLAGS.total_timesteps // batch_size
  agent = PPO(
      input_shape=info_state_shape,
      num_actions=game.num_distinct_actions(),
      num_players=game.num_players(),
      player_id=0,
      num_envs=FLAGS.num_envs,
      steps_per_batch=FLAGS.num_steps,
      num_minibatches=FLAGS.num_minibatches,
      update_epochs=FLAGS.update_epochs,
      learning_rate=FLAGS.learning_rate,
      gae=FLAGS.gae,
      gamma=FLAGS.gamma,
      gae_lambda=FLAGS.gae_lambda,
      normalize_advantages=FLAGS.norm_adv,
      clip_coef=FLAGS.clip_coef,
      clip_vloss=FLAGS.clip_vloss,
      entropy_coef=FLAGS.ent_coef,
      value_coef=FLAGS.vf_coef,
      max_grad_norm=FLAGS.max_grad_norm,
      target_kl=FLAGS.target_kl,
      device=device,
      writer=writer,
      agent_fn=agent_fn,
  )

  n_reward_window = 50
  recent_rewards = collections.deque(maxlen=n_reward_window)
  time_step = envs.reset()
  for update in range(num_updates):
    for _ in range(FLAGS.num_steps):
      agent_output = agent.step(time_step)
      time_step, reward, done, unreset_time_steps = envs.step(
          agent_output, reset_if_done=True)

      if FLAGS.game_name == "atari":
        # Get around the fact that
        # stable_baselines3.common.atari_wrappers.EpisodicLifeEnv will modify
        # rewards at the LIFE and not GAME level by only counting
        # rewards of finished episodes
        for ts in unreset_time_steps:
          info = ts.observations.get("info")
          if info and "episode" in info:
            real_reward = info["episode"]["r"]
            writer.add_scalar("charts/player_0_training_returns", real_reward,
                              agent.total_steps_done)
            recent_rewards.append(real_reward)
      else:
        for ts in unreset_time_steps:
          if ts.last():
            real_reward = ts.rewards[0]
            writer.add_scalar("charts/player_0_training_returns", real_reward,
                              agent.total_steps_done)
            recent_rewards.append(real_reward)

      agent.post_step(reward, done)

    if FLAGS.anneal_lr:
      agent.anneal_learning_rate(update, num_updates)

    agent.learn(time_step)

    if update % FLAGS.eval_every == 0:
      logging.info("-" * 80)
      logging.info("Step %s", agent.total_steps_done)
      logging.info("Summary of past %i rewards\n %s",
                   n_reward_window,
                   pd.Series(recent_rewards).describe())

  writer.close()
  logging.info("All done. Have a pleasant day :)")


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  np.random.seed(FLAGS.seed)

  game = pyspiel.load_game_as_turn_based(FLAGS.game_name,
                                         {"players": FLAGS.n_players})
  env = rl_environment.Environment(game)

  # Initialize oracle and agents
  if FLAGS.oracle_type == "DQN":
    oracle, agents = init_dqn_responder(env)
  elif FLAGS.oracle_type == "PG":
    oracle, agents = init_pg_responder(env)
  elif FLAGS.oracle_type == "BR":
    oracle, agents = init_br_responder(env)
  gpsro_looper(env, oracle, agents)


def main(_):
  print("Creating game: " + FLAGS.game)
  game = pyspiel.load_game(FLAGS.game)

  state = game.new_initial_state()

  print(str(state))

  # Need to apply the first chance node for items and utilities to be generated
  state.apply_action(0)

  print("Item pool: {}".format(state.item_pool()))
  print("Player 0 utils: {}".format(state.agent_utils(0)))
  print("Player 1 utils: {}".format(state.agent_utils(1)))

  state = game.new_initial_state()

  print(str(state))

  # Need to apply the first chance node for items and utilities to be generated
  state.apply_action(0)

  print("Item pool: {}".format(state.item_pool()))
  print("Player 0 utils: {}".format(state.agent_utils(0)))
  print("Player 1 utils: {}".format(state.agent_utils(1)))


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  mean_payoffs = get_example_2x2_payoffs()
  game = response_graph_ucb_utils.BernoulliGameSampler(
      [2, 2], mean_payoffs, payoff_bounds=[-1., 1.])
  game.p_max = mean_payoffs
  game.means = mean_payoffs
  print('Game means:\n', game.means)

  exploration_strategy = 'uniform-exhaustive'
  confidence_method = 'ucb-standard'
  r_ucb = response_graph_ucb.ResponseGraphUCB(
      game,
      exploration_strategy=exploration_strategy,
      confidence_method=confidence_method,
      delta=0.1)
  results = r_ucb.run()

  # Plotting
  print('Number of total samples: {}'.format(np.sum(r_ucb.count[0])))
  r_ucb.visualise_2x2x2(real_values=game.means, graph=results['graph'])
  r_ucb.visualise_count_history(figsize=(5, 3))
  plt.gca().xaxis.label.set_fontsize(15)
  plt.gca().yaxis.label.set_fontsize(15)

  # Compare to ground truth graph
  real_graph = r_ucb.construct_real_graph()
  r_ucb.plot_graph(real_graph)
  plt.show()


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  # Parameters to run
  deltas = [0.01, 0.025, 0.05, 0.1, 0.25, 0.5]
  sampling_methods = [
      'uniform-exhaustive', 'uniform', 'valence-weighted', 'count-weighted'
  ]
  conf_methods = [
      'ucb-standard', 'ucb-standard-relaxed', 'clopper-pearson-ucb',
      'clopper-pearson-ucb-relaxed'
  ]

  methods = list(itertools.product(sampling_methods, conf_methods))
  mean_counts = {m: [[] for _ in range(len(deltas))] for m in methods}
  edge_errs = {m: [[] for _ in range(len(deltas))] for m in methods}

  if FLAGS.game_name == 'bernoulli':
    max_total_interactions = 50000
    repetitions = 20
  elif FLAGS.game_name == 'soccer':
    max_total_interactions = 100000
    repetitions = 5
  elif FLAGS.game_name == 'kuhn_poker_3p':
    max_total_interactions = 100000
    repetitions = 5
  else:
    raise ValueError(
        'game_name must be "bernoulli", "soccer", or "kuhn_poker_3p".')

  for r in range(repetitions):
    print('Iteration {}'.format(r + 1))
    G = utils.get_game_for_sampler(FLAGS.game_name)  # pylint: disable=invalid-name

    for m in methods:
      print('  Method: {}'.format(m))
      for ix, d in enumerate(deltas):
        print('    Delta: {}'.format(d))
        r_ucb = response_graph_ucb.ResponseGraphUCB(
            G,
            exploration_strategy=m[0],
            confidence_method=m[1],
            delta=d,
            ucb_eps=1e-1)
        results = r_ucb.run(max_total_iterations=max_total_interactions)

        # Updated
        mean_counts[m][ix].append(results['interactions'])
        real_graph = r_ucb.construct_real_graph()
        edge_errs[m][ix].append(
            utils.digraph_edge_hamming_dist(real_graph, results['graph']))

  # Plotting
  _, axes = plt.subplots(1, 2, figsize=(10, 4))
  max_mean_count = 0
  for m in methods:
    utils.plot_timeseries(
        axes,
        id_ax=0,
        data=np.asarray(mean_counts[m]).T,
        xticks=deltas,
        xlabel=r'$\delta$',
        ylabel='Interactions required',
        label=utils.get_method_tuple_acronym(m),
        logx=True,
        logy=True,
        linespecs=utils.get_method_tuple_linespecs(m))
    if np.max(mean_counts[m]) > max_mean_count:
      max_mean_count = np.max(mean_counts[m])
  plt.xlim(left=np.min(deltas), right=np.max(deltas))
  plt.ylim(top=max_mean_count * 1.05)

  max_error = 0
  for m in methods:
    utils.plot_timeseries(
        axes,
        id_ax=1,
        data=np.asarray(edge_errs[m]).T,
        xticks=deltas,
        xlabel=r'$\delta$',
        ylabel='Response graph errors',
        label=utils.get_method_tuple_acronym(m),
        logx=True,
        logy=False,
        linespecs=utils.get_method_tuple_linespecs(m))
    if np.max(edge_errs[m]) > max_error:
      max_error = np.max(edge_errs[m])
  plt.xlim(left=np.min(deltas), right=np.max(deltas))
  plt.ylim(bottom=0, top=max_error*1.05)

  # Shared legend
  plt.figure(figsize=(1, 6))
  plt.figlegend(
      *axes[0].get_legend_handles_labels(),
      loc='center right',
      bbox_to_anchor=(0.8, 0.5),
      bbox_transform=plt.gcf().transFigure,
      ncol=1,
      handlelength=1.7)
  plt.tight_layout()
  plt.show()


def main(_):
  np.random.seed(FLAGS.seed)

  num_players = FLAGS.num_players

  env = rl_environment.Environment(FLAGS.game, include_full_state=True)
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  # Exploitee agents
  if FLAGS.exploitee == "first":
    exploitee_agents = [
        FirstActionAgent(idx, num_actions) for idx in range(num_players)
    ]
  elif FLAGS.exploitee == "random":
    exploitee_agents = [
        random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
        # FirstActionAgent(player_id=idx, num_actions=num_actions)
        for idx in range(num_players)
    ]
  else:
    raise RuntimeError("Unknown exploitee")

  rolling_averager = RollingAverage(FLAGS.window_size)
  rolling_averager_p0 = RollingAverage(FLAGS.window_size)
  rolling_averager_p1 = RollingAverage(FLAGS.window_size)
  rolling_value = 0
  total_value = 0
  total_value_n = 0

  hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
  # pylint: disable=g-complex-comprehension
  learning_agents = create_training_agents(
      num_players, num_actions, info_state_size, hidden_layers_sizes
  )

  print("Starting...")

  for ep in range(FLAGS.num_train_episodes):
    if (ep + 1) % FLAGS.eval_every == 0:
      r_mean = eval_against_fixed_bots(
          env, learning_agents, exploitee_agents, FLAGS.eval_episodes
      )
      value = r_mean[0] + r_mean[1]
      rolling_averager.add(value)
      rolling_averager_p0.add(r_mean[0])
      rolling_averager_p1.add(r_mean[1])
      rolling_value = rolling_averager.mean()
      rolling_value_p0 = rolling_averager_p0.mean()
      rolling_value_p1 = rolling_averager_p1.mean()
      total_value += value
      total_value_n += 1
      avg_value = total_value / total_value_n
      print(
          (
              "[{}] Mean episode rewards {}, value: {}, "
              + "rval: {} (p0/p1: {} / {}), aval: {}"
          ).format(
              ep + 1,
              r_mean,
              value,
              rolling_value,
              rolling_value_p0,
              rolling_value_p1,
              avg_value,
          )
      )

    agents_round1 = [learning_agents[0], exploitee_agents[1]]
    agents_round2 = [exploitee_agents[0], learning_agents[1]]

    for agents in [agents_round1, agents_round2]:
      time_step = env.reset()
      while not time_step.last():
        player_id = time_step.observations["current_player"]
        if env.is_turn_based:
          agent_output = agents[player_id].step(time_step)
          action_list = [agent_output.action]
        else:
          agents_output = [agent.step(time_step) for agent in agents]
          action_list = [agent_output.action for agent_output in agents_output]
        time_step = env.step(action_list)

      # Episode is over, step all agents with final info state.
      for agent in agents:
        agent.step(time_step)


def main(_):
  np.random.seed(FLAGS.seed)

  if FLAGS.bot_table_file is not None:
    analyze_bot_table(FLAGS.bot_table_file)
    return

  # Note that the include_full_state variable has to be enabled because the
  # BotAgent needs access to the full state.
  env = rl_environment.Environment(
      "repeated_game(stage_game=matrix_rps(),num_repetitions=" +
      f"{pyspiel.ROSHAMBO_NUM_THROWS}," +
      f"recall={FLAGS.env_recall})",
      include_full_state=True)
  num_players = 2
  num_actions = env.action_spec()["num_actions"]
  # Learning agents might need this:
  # info_state_size = env.observation_spec()["info_state"][0]

  print("Loading population...")
  pop_size = pyspiel.ROSHAMBO_NUM_BOTS
  print(f"Population size: {pop_size}")
  roshambo_bot_names = pyspiel.roshambo_bot_names()
  roshambo_bot_names.sort()
  print_roshambo_bot_names_and_ids(roshambo_bot_names)

  bot_id = 0
  roshambo_bot_ids = {}
  for name in roshambo_bot_names:
    roshambo_bot_ids[name] = bot_id
    bot_id += 1

  # Create two bot agents
  agents = [
      create_roshambo_bot_agent(0, num_actions, roshambo_bot_names,
                                FLAGS.player0_pop_id),
      create_roshambo_bot_agent(1, num_actions, roshambo_bot_names,
                                FLAGS.player1_pop_id)
  ]

  print("Starting eval run.")
  print(f"Player 0 is (pop_id {FLAGS.player0_pop_id}: " +
        f"{roshambo_bot_names[FLAGS.player0_pop_id]})")
  print(f"Player 1 is (pop_id {FLAGS.player1_pop_id}: " +
        f"{roshambo_bot_names[FLAGS.player1_pop_id]})")
  avg_eval_returns = eval_agents(env, agents, num_players, 100)
  print(avg_eval_returns)


def main(_):
  game = "tic_tac_toe"
  num_players = 2
  env = rl_environment.Environment(game)
  state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  hidden_layers_sizes = [32, 32]
  replay_buffer_capacity = int(1e4)
  train_episodes = FLAGS.num_episodes
  loss_report_interval = 1000

  dqn_agent = dqn.DQN(
      player_id=0,
      state_representation_size=state_size,
      num_actions=num_actions,
      hidden_layers_sizes=hidden_layers_sizes,
      replay_buffer_capacity=replay_buffer_capacity,
  )
  tabular_q_agent = tabular_qlearner.QLearner(
      player_id=1, num_actions=num_actions
  )
  agents = [dqn_agent, tabular_q_agent]

  # Train agent
  for ep in range(train_episodes):
    if ep and ep % loss_report_interval == 0:
      logging.info("[%s/%s] DQN loss: %s", ep, train_episodes, agents[0].loss)
    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      agent_output = agents[player_id].step(time_step)
      action_list = [agent_output.action]
      time_step = env.step(action_list)

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)

  # Evaluate against random agent
  random_agents = [
      random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
      for idx in range(num_players)
  ]
  r_mean = eval_against_random_bots(env, agents, random_agents, 1000)
  logging.info("Mean episode rewards: %s", r_mean)

  if not FLAGS.interactive_play:
    return

  # Play from the command line against the trained DQN agent.
  human_player = 1
  while True:
    logging.info("You are playing as %s", "X" if human_player else "0")
    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      if player_id == human_player:
        agent_out = agents[human_player].step(time_step, is_evaluation=True)
        logging.info("\n%s", agent_out.probs.reshape((3, 3)))
        logging.info("\n%s", pretty_board(time_step))
        action = command_line_action(time_step)
      else:
        agent_out = agents[1 - human_player].step(time_step, is_evaluation=True)
        action = agent_out.action
      time_step = env.step([action])

    logging.info("\n%s", pretty_board(time_step))

    logging.info("End of game!")
    if time_step.rewards[human_player] > 0:
      logging.info("You win")
    elif time_step.rewards[human_player] < 0:
      logging.info("You lose")
    else:
      logging.info("Draw")
    # Switch order of players
    human_player = 1 - human_player


def main(_: Sequence[str]) -> None:
  game = "tic_tac_toe"
  num_players = 2

  env = rl_environment.Environment(game)
  num_actions = env.action_spec()["num_actions"]

  agents = [
      tabular_qlearner.QLearner(player_id=idx, num_actions=num_actions)
      for idx in range(num_players)
  ]

  # random agents for evaluation
  random_agents = [
      random_agent.RandomAgent(player_id=idx, num_actions=num_actions)
      for idx in range(num_players)
  ]

  # 1. Train the agents
  training_episodes = FLAGS.num_episodes
  for cur_episode in range(training_episodes):
    if cur_episode % int(1e4) == 0:
      win_rates = eval_against_random_bots(env, agents, random_agents, 1000)
      logging.info("Starting episode %s, win_rates %s", cur_episode, win_rates)
    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      agent_output = agents[player_id].step(time_step)
      time_step = env.step([agent_output.action])

    # Episode is over, step all agents with final info state.
    for agent in agents:
      agent.step(time_step)

  if not FLAGS.interactive_play:
    return

  # 2. Play from the command line against the trained agent.
  human_player = 1
  while True:
    logging.info("You are playing as %s", "O" if human_player else "X")
    time_step = env.reset()
    while not time_step.last():
      player_id = time_step.observations["current_player"]
      if player_id == human_player:
        agent_out = agents[human_player].step(time_step, is_evaluation=True)
        logging.info("\n%s", agent_out.probs.reshape((3, 3)))
        logging.info("\n%s", pretty_board(time_step))
        action = command_line_action(time_step)
      else:
        agent_out = agents[1 - human_player].step(time_step, is_evaluation=True)
        action = agent_out.action
      time_step = env.step([action])

    logging.info("\n%s", pretty_board(time_step))

    logging.info("End of game!")
    if time_step.rewards[human_player] > 0:
      logging.info("You win")
    elif time_step.rewards[human_player] < 0:
      logging.info("You lose")
    else:
      logging.info("Draw")
    # Switch order of players
    human_player = 1 - human_player


def main(argv):
  del argv

  game = pyspiel.load_game(FLAGS.game)
  game_type = game.get_type()

  if game_type.dynamics == pyspiel.GameType.Dynamics.SIMULTANEOUS:
    logging.warn("%s is not turn-based. Trying to reload game as turn-based.",
                 FLAGS.game)
    game = pyspiel.load_game_as_turn_based(FLAGS.game)
    game_type = game.get_type()

  if game_type.dynamics != pyspiel.GameType.Dynamics.SEQUENTIAL:
    raise ValueError("Game must be sequential, not {}".format(
        game_type.dynamics))

  if (game_type.utility == pyspiel.GameType.Utility.ZERO_SUM and
      game.num_players() == 2):
    logging.info("Game is zero-sum: only showing first-player's returns.")
    gametree = treeviz.GameTree(
        game,
        node_decorator=_zero_sum_node_decorator,
        group_infosets=FLAGS.group_infosets,
        group_terminal=FLAGS.group_terminal,
        group_pubsets=FLAGS.group_pubsets,
        target_pubset=FLAGS.target_pubset)
  else:
    # use default decorators
    gametree = treeviz.GameTree(
        game,
        group_infosets=FLAGS.group_infosets,
        group_terminal=FLAGS.group_terminal,
        group_pubsets=FLAGS.group_pubsets,
        target_pubset=FLAGS.target_pubset)

  if FLAGS.verbose:
    logging.info("Game tree:\n%s", gametree.to_string())

  gametree.draw(FLAGS.out, prog=FLAGS.prog)
  logging.info("Game tree saved to file: %s", FLAGS.out)


def main(_):
  n_tuple_network = NTupleNetwork(
      6,
      15,
      [
          [0, 1, 2, 3, 4, 5],
          [4, 5, 6, 7, 8, 9],
          [0, 1, 2, 4, 5, 6],
          [4, 5, 6, 8, 9, 10],
      ],
  )
  game = pyspiel.load_game(FLAGS.game)
  sum_rewards = 0
  largest_tile = 0
  max_score = 0
  for ep in range(FLAGS.num_train_episodes):
    state = game.new_initial_state()
    states_in_episode = []
    while not state.is_terminal():
      if state.is_chance_node():
        outcomes = state.chance_outcomes()
        action_list, prob_list = zip(*outcomes)
        action = np.random.choice(action_list, p=prob_list)
        state.apply_action(action)
      else:
        legal_actions = state.legal_actions(state.current_player())
        # pylint: disable=cell-var-from-loop
        best_action = max(
            legal_actions,
            key=lambda action: n_tuple_network.evaluator(state, action),
        )
        state.apply_action(best_action)
        states_in_episode.append(state.clone())

    sum_rewards += state.returns()[0]
    largest_tile_from_episode = max(state.observation_tensor(0))
    if largest_tile_from_episode > largest_tile:
      largest_tile = largest_tile_from_episode
    if state.returns()[0] > max_score:
      max_score = state.returns()[0]

    n_tuple_network.learn(states_in_episode)

    if (ep + 1) % FLAGS.eval_every == 0:
      logging.info(
          "[%s] Average Score: %s, Max Score: %s, Largest Tile Reached: %s",
          ep + 1,
          int(sum_rewards / FLAGS.eval_every),
          int(max_score),
          int(largest_tile),
      )
      sum_rewards = 0
      largest_tile = 0
      max_score = 0


def main(_):
  game = pyspiel.load_game(FLAGS.game)
  expl = exploitability.exploitability(game, policy.UniformRandomPolicy(game))
  print("Exploitability: {}".format(expl))


def main(_):
  game = universal_poker.load_universal_poker_from_acpc_gamedef(
      CUSTOM_LIMIT_HOLDEM_ACPC_GAMEDEF
  )

  solver = None
  if FLAGS.solver == "cfr":
    solver = pyspiel.CFRSolver(game)
  elif FLAGS.solver == "cfrplus":
    solver = pyspiel.CFRPlusSolver(game)
  elif FLAGS.solver == "cfrbr":
    solver = pyspiel.CFRBRSolver(game)
  else:
    print("Unknown solver")
    sys.exit(0)

  for i in range(int(_ITERATIONS.value / 2)):
    solver.evaluate_and_update_policy()
    print("Iteration {} exploitability: {:.6f}".format(
        i, pyspiel.exploitability(game, solver.average_policy())))

  filename = os.path.join(
      tempfile.gettempdir(), "{}_solver.pickle".format(FLAGS.solver)
  )
  print("Persisting the model...")
  with open(filename, "wb") as file:
    pickle.dump(solver, file, pickle.HIGHEST_PROTOCOL)

  print("Loading the model...")
  with open(filename, "rb") as file:
    loaded_solver = pickle.load(file)
  print("Exploitability of the loaded model: {:.6f}".format(
      pyspiel.exploitability(game, loaded_solver.average_policy())))

  for i in range(int(_ITERATIONS.value / 2)):
    loaded_solver.evaluate_and_update_policy()
    tabular_policy = loaded_solver.tabular_average_policy()
    print(f"Tabular policy length: {len(tabular_policy)}")
    print(
        "Iteration {} exploitability: {:.6f}".format(
            int(_ITERATIONS.value / 2) + i,
            pyspiel.exploitability(game, loaded_solver.average_policy()),
        )
    )


def main(argv):
  del argv
  if FLAGS.game == "tic_tac_toe":
    play_tic_tac_toe()
  else:
    raise NotImplementedError("This example only works for Tic-Tac-Toe.")


def main(_):
  torch.manual_seed(SEED)
  absltest.main()


def main(_):
  absltest.main()


def main(_):
  absltest.main()


def main(_):
  print("Loading dataset(s)...")
  dataset_filename = (_DATASET_PATH_PREFIX.value + "/" +
                      atari_datasets.RAINBOW_TABLE5)
  dataset = atari_datasets.parse_atari_table(dataset_filename)

  # If you load others, you can merge some columns from them like this:
  # dataset.add_column(dataset_ag57.get_column("random"), "random")
  # dataset.add_column(dataset_ag57.get_column("human"), "human")

  print(dataset.agent_names)
  print(dataset.game_names)
  print(f"Num agents: {len(dataset.agent_names)}")
  print(f"Num games: {len(dataset.game_names)}")

  # Alts for rainbow table 5:
  # dqn a3c ddqn prior-ddqn dueling-ddqn distrib-dqn noisy-dqn rainbow

  game_names = []
  profile = base.PreferenceProfile(alternatives=dataset.agent_names)
  for game_name, scores in dataset.table_data.items():
    profile.add_vote_from_values(scores)
    game_names.append(game_name)

  # Group up the profile and then print it to show that every vote is unique.
  profile.group()
  print(profile)

  print("Margin matrix:")
  margin_matrix = profile.margin_matrix()
  print(margin_matrix)
  print(
      "Weak Condorcet winners? "
      + f"{profile.condorcet_winner(False, margin_matrix)}"
  )
  print(
      "Strong Condorcet winner? "
      + f"{profile.condorcet_winner(True, margin_matrix)}"
  )

  voting_methods = [
      approval.ApprovalVoting(k=3),
      borda.BordaVoting(),
      copeland.CopelandVoting(),
      kemeny_young.KemenyYoungVoting(),
      maximal_lotteries.MaximalLotteriesVoting(iterative=True),
      plurality.PluralityVoting(),
      ranked_pairs.RankedPairsVoting(),
      schulze.SchulzeVoting(),
      stv.STVVoting(num_winners=3),
  ]
  for method in voting_methods:
    print("")
    print(method.name())
    outcome = method.run_election(profile)
    print(outcome.pretty_table_string())

  print("Soft Condorcet Optimization (Python):")
  py_sco_solver = sco.SoftCondorcetOptimizer(
      profile,
      batch_size=4,
      rating_lower_bound=-100.0,
      rating_upper_bound=100.0,
      temperature=1,
  )
  start_time = time.time()
  ratings, ranking = py_sco_solver.run_solver(10000, learning_rate=0.01)
  end_time = time.time()
  print(f"Time taken: {end_time - start_time}")
  alt_idx = profile.alternatives_dict
  for alt in ranking:
    print(f"  {alt}: {ratings[alt_idx[alt]]}")

  print("Soft Condorcet Optimization Sigmoid (C++):")
  cpp_sco_solver = pyspiel.sco.SoftCondorcetOptimizer(
      profile.to_list_of_tuples(),
      rating_lower_bound=-100.0,
      rating_upper_bound=100.0,
      batch_size=4,
      temperature=1,
      rng_seed=0,
  )
  start_time = time.time()
  cpp_sco_solver.run_solver(10000, learning_rate=0.01)
  end_time = time.time()
  print(f"Time taken: {end_time - start_time}")
  ratings_dict = cpp_sco_solver.ratings()
  for alt in ranking:
    print(f"  {alt}: {ratings_dict[alt]}")

  print("Soft Condorcet Optimization Fenchel-Young (C++):")
  cpp_fy_solver = pyspiel.sco.FenchelYoungOptimizer(
      profile.to_list_of_tuples(),
      rating_lower_bound=-100.0,
      rating_upper_bound=100.0,
      batch_size=4,
      temperature=1,
      rng_seed=0,
  )
  start_time = time.time()
  cpp_fy_solver.run_solver(10000, learning_rate=0.01)
  end_time = time.time()
  print(f"Time taken: {end_time - start_time}")
  ratings_dict = cpp_fy_solver.ratings()
  for alt in ranking:
    print(f"  {alt}: {ratings_dict[alt]}")


def main(_):
  model_names, dataset = parse_battles_dataset()
  model_names.sort()
  print(f"{len(model_names)} models.")
  print(f"{len(dataset)} datapoints.")
  chatbot_arena_vase(model_names, dataset)
  ranked_pairs_viz(model_names, dataset)


def main(_):
  # Create a preference profile that represents the following votes:
  #   A > B > C
  #   A > C > B
  #   C > A > B
  #   C > A > B
  #   B > C > A
  # This profile has three alternatives: A, B, and C. The strings here "A", "B",
  # "C" represent the alternative's ID and is of type base.AlternativeId.
  # (They can be strings or integers.)
  alternatives = ["A", "B", "C"]

  # Easiest way to make this profile:
  _ = base.PreferenceProfile(alternatives=alternatives, votes=[
      ["A", "B", "C"], ["A", "C", "B"], ["C", "A", "B"], ["C", "A", "B"],
      ["B", "C", "A"]
  ])

  # Note that the C > A > B vote is there twice, so another common way to show
  # this is:
  #   1: A > B > C
  #   1: A > C > B
  #   2: C > A > B
  #   1: B > C > A
  # and can be created with the WeightedVote type directly.
  profile = base.PreferenceProfile(alternatives=alternatives, votes=[
      base.WeightedVote(1, ["A", "B", "C"]),
      base.WeightedVote(1, ["A", "C", "B"]),
      base.WeightedVote(2, ["C", "A", "B"]),
      base.WeightedVote(1, ["B", "C", "A"])
  ])

  # Print some information about the profile
  print(f"Number of alternatives: {profile.num_alternatives()}")
  print(f"Number of votes: {profile.num_votes()}")
  print(f"Alternatives: {profile.alternatives}")
  print("Profile:")
  print(profile)

  # Print a reverse mapping of AlternativeId -> index
  # indices will always be numbered 0 to num_alternatives - 1.
  # Some methods work directly with the indices.
  alt_idx = profile.alternatives_dict
  print("Alternative ids -> index map:")
  print(alt_idx)

  # Iterating through a profile
  print("Iterating through profile:")
  for vote in profile.votes:
    # Each item is a weighted vote:
    print(f"  {vote.weight}: {vote.vote}")

  # Margin matrix and Condorcet winner check
  margin_matrix = profile.margin_matrix()
  cond_winners = profile.condorcet_winner(strong=True,
                                          margin_matrix=margin_matrix)
  print("Margin matrix:")
  print(margin_matrix)
  print(f"Condorcet winners: {cond_winners}")

  # Run Copeland on this profile and print the results
  method = copeland.CopelandVoting()
  outcome = method.run_election(profile)
  print("Copeland outcome:")
  print(outcome.pretty_table_string())


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  param_names, param_values = zip(
      *[convert_param_spec(spec) for spec in FLAGS.parameters])
  header = (['game_name'] + list(param_names) +
            ['fictitious_play_iteration_time'])
  timing_results = []
  for game_name in FLAGS.games:
    for param_tuple in itertools.product(*param_values):
      result_line = [game_name] + [str(p) for p in param_tuple]
      print('Computing timings for:', ' '.join(result_line))
      param_dict = dict(zip(param_names, param_tuple))
      game = pyspiel.load_game(game_name, param_dict)
      t0 = time.time()
      fp = fictitious_play.FictitiousPlay(game)
      fp.iteration()
      elapsed = time.time() - t0
      result_line.append(f'{elapsed:.4f}s')
      print(' '.join(result_line))
      timing_results.append(result_line)

  print('\nRESULTS:')
  print(' '.join(header))
  for line in timing_results:
    print(' '.join([str(v) for v in line]))


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')
  mfg_game = pyspiel.load_game(
      FLAGS.game, {
          'dt': FLAGS.dt,
          'size': FLAGS.size,
          'horizon': FLAGS.horizon,
          'n_actions_per_side': FLAGS.n_actions_per_side,
          'volatility': FLAGS.volatility
      })

  uniform_policy = policy.UniformRandomPolicy(mfg_game)
  nash_conv_fp = nash_conv.NashConv(mfg_game, uniform_policy)
  print('Uniform Policy Nashconv:', nash_conv_fp.nash_conv())

  # Optimal control in the continuous setting.
  theoretical_control = LinearPolicy(mfg_game,
                                     list(range(mfg_game.num_players())))
  theoretical_distribution = distribution.DistributionPolicy(
      mfg_game, theoretical_control)
  discretized_optimal_value = policy_value.PolicyValue(
      mfg_game, theoretical_distribution,
      theoretical_control).eval_state(mfg_game.new_initial_state())

  th_expl = nash_conv.NashConv(mfg_game, theoretical_control).nash_conv()
  print('Theoretical policy NashConv : {}'.format(th_expl))
  print('Theoretical policy Value : {}'.format(discretized_optimal_value))

  fp = fictitious_play.FictitiousPlay(mfg_game)
  md = mirror_descent.MirrorDescent(mfg_game)
  for j in range(1000):
    print('\n\nIteration', j, '\n')
    fp.iteration()
    fp_policy = fp.get_policy()
    nash_conv_fp = nash_conv.NashConv(mfg_game, fp_policy)
    print('Nashconv of the current FP policy', nash_conv_fp.nash_conv())
    fp_current_distribution = distribution.DistributionPolicy(
        mfg_game, fp.get_policy())
    fp_l1_dist = get_l1_distribution_dist(fp_current_distribution,
                                          theoretical_distribution)
    print(
        'L1 distance between FP and theoretical policy : {}'.format(fp_l1_dist))
    md.iteration()
    md_policy = md.get_policy()
    nash_conv_md = nash_conv.NashConv(mfg_game, md_policy)

    print('')

    print('Nashconv of the current MD policy', nash_conv_md.nash_conv())
    md_current_distribution = md._distribution  # pylint:disable=protected-access
    md_l1_dist = get_l1_distribution_dist(md_current_distribution,
                                          theoretical_distribution)
    print('L1 distance between OMD and theoretical policy : {}'.format(
        md_l1_dist))


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  game = factory.create_game_with_setting(_GAME_NAME.value, _ENV_SETTING.value)
  num_players = game.num_players()

  # Create the environments with uniform initial policy.
  uniform_policy = policy_std.UniformRandomPolicy(game)
  uniform_dist = distribution.DistributionPolicy(game, uniform_policy)

  envs = [
      rl_environment.Environment(
          game, mfg_distribution=uniform_dist, mfg_population=p)
      for p in range(num_players)
  ]

  env = envs[0]
  info_state_size = env.observation_spec()['info_state'][0]
  num_actions = env.action_spec()['num_actions']

  # Best response policy agents.
  kwargs_dqn = {
      'batch_size': _BATCH_SIZE.value,
      'discount_factor': _DISCOUNT_FACTOR.value,
      'epsilon_decay_duration': _EPSILON_DECAY_DURATION.value,
      'epsilon_end': _EPSILON_END.value,
      'epsilon_start': _EPSILON_START.value,
      'gradient_clipping': _GRADIENT_CLIPPING.value,
      'hidden_layers_sizes': [int(l) for l in _HIDDEN_LAYERS_SIZES.value],
      'huber_loss_parameter': _HUBER_LOSS_PARAMETER.value,
      'learn_every': _LEARN_EVERY.value,
      'learning_rate': _LEARNING_RATE.value,
      'loss_str': _LOSS.value,
      'min_buffer_size_to_learn': _MIN_BUFFER_SIZE_TO_LEARN.value,
      'optimizer_str': _OPTIMIZER.value,
      'replay_buffer_capacity': _REPLAY_BUFFER_CAPACITY.value,
      'seed': _SEED.value,
      'update_target_network_every': _UPDATE_TARGET_NETWORK_EVERY.value,
  }
  br_rl_agents = [
      dqn.DQN(p, info_state_size, num_actions, **kwargs_dqn)
      for p in range(num_players)
  ]

  num_training_steps_per_iteration = (
      _AVG_POL_NUM_TRAINING_STEPS_PER_ITERATION.value)

  # Metrics writer will also log the metrics to stderr.
  just_logging = _LOGDIR.value is None or jax.process_index() > 0
  writer = metrics.create_default_writer(
      _LOGDIR.value, just_logging=just_logging)

  def logging_fn(it, step, vals):
    writer.write_scalars(it * num_training_steps_per_iteration + step, vals)

  # Average policy agents.
  kwargs_avg = {
      'batch_size': _AVG_POL_BATCH_SIZE.value,
      'hidden_layers_sizes': [
          int(l) for l in _AVG_POL_HIDDEN_LAYERS_SIZES.value
      ],
      'reservoir_buffer_capacity': _AVG_POL_RESERVOIR_BUFFER_CAPACITY.value,
      'learning_rate': _AVG_POL_LEARNING_RATE.value,
      'min_buffer_size_to_learn': _AVG_POL_MIN_BUFFER_SIZE_TO_LEARN.value,
      'optimizer_str': _AVG_POL_OPTIMIZER.value,
      'gradient_clipping': _AVG_GRADIENT_CLIPPING.value,
      'seed': _SEED.value,
      'tau': _AVG_POL_TAU.value
  }
  fp = average_network_fictitious_play.AverageNetworkFictitiousPlay(
      game,
      envs,
      br_rl_agents,
      _AVG_POL_NUM_EPISODES_PER_ITERATION.value,
      num_training_steps_per_iteration,
      eval_every=_EVAL_EVERY.value,
      logging_fn=logging_fn,
      **kwargs_avg)

  def log_metrics(it):
    """Logs the training metrics for each iteration."""
    initial_states = game.new_initial_states()
    distrib = distribution.DistributionPolicy(game, fp.policy)
    pi_value = policy_value.PolicyValue(game, distrib, fp.policy)
    m = {
        f'best_response/{state}': pi_value.eval_state(state)
        for state in initial_states
    }
    m.update({
        f'br_agent{i}/loss': agent.loss for i, agent in enumerate(br_rl_agents)
    })
    nash_conv_fp = nash_conv.NashConv(game, fp.policy)
    m['nash_conv_fp'] = nash_conv_fp.nash_conv()
    logging_fn(it, 0, m)

    # Also save the distribution.
    if _LOG_DISTRIBUTION.value and not just_logging:
      filename = os.path.join(_LOGDIR.value, f'distribution_{it}.pkl')
      utils.save_parametric_distribution(nash_conv_fp.distribution, filename)

  for it in range(_NUM_ITERATIONS.value):
    # Train the RL agent to learn a best response.
    training.run_episodes(
        envs,
        br_rl_agents,
        num_episodes=_NUM_DQN_EPISODES_PER_ITERATION.value,
        is_evaluation=False)

    # Run an iteration of average-network fictitious play and log the metrics.
    fp.iteration()
    log_metrics(it + 1)

  # Make sure all values were written.
  writer.flush()


def main(unused_argv):
  game = factory.create_game_with_setting(FLAGS.game_name, FLAGS.env_setting)
  uniform_policy = policy.UniformRandomPolicy(game)
  mfg_dist = distribution.DistributionPolicy(game, uniform_policy)

  envs = [
      rl_environment.Environment(
          game, mfg_distribution=mfg_dist, mfg_population=p)
      for p in range(game.num_players())
  ]
  info_state_size = envs[0].observation_spec()["info_state"][0]
  num_actions = envs[0].action_spec()["num_actions"]

  hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
  kwargs = {
      "replay_buffer_capacity": FLAGS.replay_buffer_capacity,
      "min_buffer_size_to_learn": FLAGS.min_buffer_size_to_learn,
      "batch_size": FLAGS.batch_size,
      "learn_every": FLAGS.learn_every,
      "learning_rate": FLAGS.rl_learning_rate,
      "optimizer_str": FLAGS.optimizer_str,
      "loss_str": FLAGS.loss_str,
      "update_target_network_every": FLAGS.update_target_network_every,
      "discount_factor": FLAGS.discount_factor,
      "epsilon_decay_duration": FLAGS.epsilon_decay_duration,
      "epsilon_start": FLAGS.epsilon_start,
      "epsilon_end": FLAGS.epsilon_end,
  }

  # pylint: disable=g-complex-comprehension
  agents = [
      dqn.DQN(idx, info_state_size, num_actions, hidden_layers_sizes, **kwargs)
      for idx in range(game.num_players())
  ]
  joint_avg_policy = rl_agent_policy.JointRLAgentPolicy(
      game, {idx: agent for idx, agent in enumerate(agents)},
      envs[0].use_observation)

  if FLAGS.use_checkpoints:
    for agent in agents:
      if agent.has_checkpoint(FLAGS.checkpoint_dir):
        agent.restore(FLAGS.checkpoint_dir)

  # Metrics writer will also log the metrics to stderr.
  just_logging = FLAGS.logdir is None or jax.process_index() > 0
  writer = metrics.create_default_writer(
      logdir=FLAGS.logdir, just_logging=just_logging)

  # Save the parameters.
  writer.write_hparams(kwargs)

  fp = fictitious_play.FictitiousPlay(game)
  num_episodes_per_iteration = FLAGS.num_episodes_per_iteration

  def log_metrics(it, episode=0):
    initial_states = game.new_initial_states()
    fp_policy = fp.get_policy()
    distrib = distribution.DistributionPolicy(game, fp_policy)
    pi_value = policy_value.PolicyValue(game, distrib, fp_policy)
    m = {
        f"dqn_br/{state}": pi_value.eval_state(state)
        for state in initial_states
    }
    # Loss will be None at the beginning.
    if agents[0].loss is not None:
      m.update({
          f"agent{i}/loss": float(agent.loss) for i, agent in enumerate(agents)
      })
    nash_conv_fp = nash_conv.NashConv(game, fp_policy).nash_conv()
    m["nash_conv_fp"] = nash_conv_fp
    # We log using the total number of episode steps so that runs with different
    # training regimes are comparable.
    writer.write_scalars(it * num_episodes_per_iteration + episode, m)

  log_metrics(0)
  for it in range(FLAGS.num_iterations):
    # Update the Fictitious Play policy.
    fp.iteration(br_policy=joint_avg_policy)

    # Update the distribution of the environments.
    distrib = distribution.DistributionPolicy(game, fp.get_policy())
    for env in envs:
      env.update_mfg_distribution(distrib)

    # Train the RL agent to learn a best response.
    for _ in range(num_episodes_per_iteration):
      for p in range(game.num_players()):
        time_step = envs[p].reset()
        while not time_step.last():
          agent_output = agents[p].step(time_step)
          action_list = [agent_output.action]
          time_step = envs[p].step(action_list)

        # Episode is over, step all agents with final info state.
        agents[p].step(time_step)

    # Check point the agents.
    if FLAGS.use_checkpoints:
      for agent in agents:
        agent.save(FLAGS.checkpoint_dir)

    # Log the final metrics.
    log_metrics(it + 1)

  # Make sure all values were written.
  writer.flush()


def main(unused_argv):
  game = factory.create_game_with_setting(FLAGS.game_name, FLAGS.env_setting)
  uniform_policy = policy.UniformRandomPolicy(game)
  mfg_dist = distribution.DistributionPolicy(game, uniform_policy)

  envs = [
      rl_environment.Environment(
          game, mfg_distribution=mfg_dist, mfg_population=p)
      for p in range(game.num_players())
  ]
  info_state_size = envs[0].observation_spec()["info_state"][0]
  num_actions = envs[0].action_spec()["num_actions"]

  hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
  kwargs = {
      "replay_buffer_capacity": FLAGS.replay_buffer_capacity,
      "min_buffer_size_to_learn": FLAGS.min_buffer_size_to_learn,
      "batch_size": FLAGS.batch_size,
      "learn_every": FLAGS.learn_every,
      "learning_rate": FLAGS.rl_learning_rate,
      "optimizer_str": FLAGS.optimizer_str,
      "loss_str": FLAGS.loss_str,
      "update_target_network_every": FLAGS.update_target_network_every,
      "discount_factor": FLAGS.discount_factor,
      "epsilon_decay_duration": FLAGS.epsilon_decay_duration,
      "epsilon_start": FLAGS.epsilon_start,
      "epsilon_end": FLAGS.epsilon_end,
  }

  # pylint: disable=g-complex-comprehension
  agents = [
      dqn.DQN(idx, info_state_size, num_actions, hidden_layers_sizes, **kwargs)
      for idx in range(game.num_players())
  ]
  joint_avg_policy = rl_agent_policy.JointRLAgentPolicy(
      game, {idx: agent for idx, agent in enumerate(agents)},
      envs[0].use_observation)
  if FLAGS.use_checkpoints:
    for agent in agents:
      if agent.has_checkpoint(FLAGS.checkpoint_dir):
        agent.restore(FLAGS.checkpoint_dir)

  # Metrics writer will also log the metrics to stderr.
  just_logging = FLAGS.logdir is None or jax.process_index() > 0
  writer = metrics.create_default_writer(
      logdir=FLAGS.logdir, just_logging=just_logging)

  # Save the parameters.
  writer.write_hparams(kwargs)

  for ep in range(1, FLAGS.num_train_episodes + 1):
    if ep % FLAGS.eval_every == 0:
      writer.write_scalars(ep, {
          f"agent{i}/loss": float(agent.loss) for i, agent in enumerate(agents)
      })

      initial_states = game.new_initial_states()

      # Exact best response to uniform.
      nash_conv_obj = nash_conv.NashConv(game, uniform_policy)
      writer.write_scalars(
          ep, {
              f"exact_br/{state}": value
              for state, value in zip(initial_states, nash_conv_obj.br_values())
          })

      # DQN best response to uniform.
      pi_value = policy_value.PolicyValue(game, mfg_dist, joint_avg_policy)
      writer.write_scalars(ep, {
          f"dqn_br/{state}": pi_value.eval_state(state)
          for state in initial_states
      })

      if FLAGS.use_checkpoints:
        for agent in agents:
          agent.save(FLAGS.checkpoint_dir)

    for p in range(game.num_players()):
      time_step = envs[p].reset()
      while not time_step.last():
        agent_output = agents[p].step(time_step)
        action_list = [agent_output.action]
        time_step = envs[p].step(action_list)

      # Episode is over, step all agents with final info state.
      agents[p].step(time_step)

  # Make sure all values were written.
  writer.flush()


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  game = factory.create_game_with_setting(FLAGS.game_name, FLAGS.setting)

  # Metrics writer will also log the metrics to stderr.
  just_logging = _LOGDIR.value is None
  writer = metrics.create_default_writer(
      logdir=_LOGDIR.value, just_logging=just_logging)

  # Save the parameters.
  learning_rate = FLAGS.learning_rate
  writer.write_hparams({'learning_rate': learning_rate})

  fp = fictitious_play.FictitiousPlay(game)

  for it in range(FLAGS.num_iterations):
    fp.iteration(learning_rate=learning_rate)
    fp_policy = fp.get_policy()
    nash_conv_fp = nash_conv.NashConv(game, fp_policy)
    exploitability = nash_conv_fp.nash_conv()
    writer.write_scalars(it, {'exploitability': exploitability})
    if _LOG_DISTRIBUTION.value and not just_logging:
      filename = os.path.join(_LOGDIR.value, f'distribution_{it}.pkl')
      utils.save_parametric_distribution(nash_conv_fp.distribution, filename)

  writer.flush()


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  game = factory.create_game_with_setting(_GAME_NAME.value, _SETTING.value)

  # Metrics writer will also log the metrics to stderr.
  just_logging = _LOGDIR.value is None
  writer = metrics.create_default_writer(
      logdir=_LOGDIR.value, just_logging=just_logging)

  # Save the parameters.
  learning_rate = _LEARNING_RATE.value
  writer.write_hparams({'learning_rate': learning_rate})

  md = mirror_descent.MirrorDescent(game, lr=learning_rate)

  for it in range(_NUM_ITERATIONS.value):
    md.iteration()
    md_policy = md.get_policy()
    exploitability = nash_conv.NashConv(game, md_policy).nash_conv()
    writer.write_scalars(it, {'exploitability': exploitability})
    if _LOG_DISTRIBUTION.value and not just_logging:
      filename = os.path.join(_LOGDIR.value, f'distribution_{it}.pkl')
      utils.save_parametric_distribution(md.distribution, filename)

  writer.flush()


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  game = factory.create_game_with_setting(FLAGS.game_name, _ENV_SETTING.value)

  num_players = game.num_players()

  # Create the environments with uniform initial policy.
  uniform_policy = policy.UniformRandomPolicy(game)
  uniform_dist = distribution.DistributionPolicy(game, uniform_policy)

  envs = [
      rl_environment.Environment(  # pylint: disable=g-complex-comprehension
          game,
          mfg_distribution=uniform_dist,
          mfg_population=p,
          observation_type=rl_environment.ObservationType.OBSERVATION,
      )
      for p in range(num_players)
  ]

  env = envs[0]
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]

  # Create the agents.
  kwargs = {
      "alpha": FLAGS.alpha,
      "batch_size": _BATCH_SIZE.value,
      "discount_factor": _DISCOUNT_FACTOR.value,
      "epsilon_decay_duration": _EPSILON_DECAY_DURATION.value,
      "epsilon_end": FLAGS.epsilon_end,
      "epsilon_power": FLAGS.epsilon_power,
      "epsilon_start": FLAGS.epsilon_start,
      "gradient_clipping": FLAGS.gradient_clipping,
      "hidden_layers_sizes": [int(l) for l in _HIDDEN_LAYERS_SIZES.value],
      "huber_loss_parameter": FLAGS.huber_loss_parameter,
      "learn_every": _LEARN_EVERY.value,
      "learning_rate": FLAGS.learning_rate,
      "loss": FLAGS.loss,
      "min_buffer_size_to_learn": _MIN_BUFFER_SIZE_TO_LEARN.value,
      "optimizer": FLAGS.optimizer,
      "replay_buffer_capacity": _REPLAY_BUFFER_CAPACITY.value,
      "reset_replay_buffer_on_update": _RESET_REPLAY_BUFFER_ON_UPDATE.value,
      "seed": FLAGS.seed,
      "tau": FLAGS.tau,
      "update_target_network_every": _UPDATE_TARGET_NETWORK_EVERY.value,
      "with_munchausen": _WITH_MUNCHAUSEN.value,
  }
  agents = [
      munchausen_deep_mirror_descent.MunchausenDQN(
          p, info_state_size, num_actions, **kwargs
      )
      for p in range(num_players)
  ]

  # Metrics writer will also log the metrics to stderr.
  just_logging = _LOGDIR.value is None or jax.process_index() > 0
  writer = metrics.create_default_writer(
      logdir=_LOGDIR.value, just_logging=just_logging
  )

  # # Save the parameters.
  writer.write_hparams(kwargs)

  def logging_fn(it, episode, vals):
    writer.write_scalars(it * num_episodes_per_iteration + episode, vals)

  num_episodes_per_iteration = _NUM_EPISODES_PER_ITERATION.value
  md = munchausen_deep_mirror_descent.DeepOnlineMirrorDescent(
      game,
      envs,
      agents,
      eval_every=_EVAL_EVERY.value,
      num_episodes_per_iteration=num_episodes_per_iteration,
      logging_fn=logging_fn,
  )

  def log_metrics(it):
    """Logs the training metrics for each iteration."""
    initial_states = game.new_initial_states()
    pi_value = policy_value.PolicyValue(game, md.distribution, md.policy)
    m = {
        f"best_response/{state}": pi_value.eval_state(state)
        for state in initial_states
    }
    nash_conv_md = nash_conv.NashConv(game, md.policy).nash_conv()
    m["nash_conv_md"] = nash_conv_md
    if _LOG_DISTRIBUTION.value and _LOGDIR.value:
      # We log distribution directly to a Pickle file as it may be large for
      # logging as a metric.
      filename = os.path.join(_LOGDIR.value, f"distribution_{it}.pkl")
      utils.save_parametric_distribution(md.distribution, filename)
    logging_fn(it, 0, m)

  log_metrics(0)
  for it in range(1, FLAGS.num_iterations + 1):
    md.iteration()
    log_metrics(it)

  # Make sure all values were written.
  writer.flush()


def main(unused_argv):
  """Main function to run the experiment."""

  # Set the random seed for reproducibility
  set_seed(FLAGS.seed)

  # Set the device (in our experiments CPU vs GPU does not improve time at all)
  # we recommend CPU
  device = torch.device(
      "cuda" if torch.cuda.is_available() and FLAGS.cuda else "cpu"
  )

  # Set the name of the experiment's folder
  fname = "./mfppo_experiments/"

  # Log the experiments
  run_name = (
      f"{FLAGS.exp_name}_{FLAGS.game_setting}_{FLAGS.optimizer}_num_update_epochs_"
      "     "
      f" {FLAGS.update_epochs}_num_episodes_per_rollout_{FLAGS.num_episodes}_number_of_mini_batches_"
      "     "
      f" {FLAGS.num_minibatches}_{time.asctime(time.localtime(time.time()))}"
  )
  log_name = os.path.join(fname, run_name)
  tb_writer = SummaryWriter(log_name)
  logging.basicConfig(
      filename=log_name + "_log.txt",
      filemode="a",
      level=logging.DEBUG,
      force=True,
  )

  # Console handler
  console = logging.StreamHandler()
  console.setLevel(logging.ERROR)
  logging.getLogger("").addHandler(console)

  logger = logging.getLogger()
  logger.debug("Initialization")

  tb_writer.add_text(
      "hyperparameters",
      "|param|value|\n|-|-|\n%s"
      % "\n".join([f"|{key}|{value}" for key, value in vars(FLAGS).items()]),
  )
  # Create the game instance
  game = factory.create_game_with_setting(
      "mfg_crowd_modelling_2d", FLAGS.game_setting
  )

  # Set the initial policy to uniform and generate the distribution
  uniform_policy = policy_std.UniformRandomPolicy(game)
  mfg_dist = distribution.DistributionPolicy(game, uniform_policy)
  env = rl_environment.Environment(
      game, mfg_distribution=mfg_dist, mfg_population=0
  )

  # Set the environment seed for reproduciblility
  env.seed(FLAGS.seed)

  # Creat the agent and population policies
  info_state_size = env.observation_spec()["info_state"][0]
  num_actions = env.action_spec()["num_actions"]
  agent = mfg_ppo_agent(info_state_size, num_actions).to(device)
  ppo_policy = mfg_ppo_policy(game, agent, None, device)
  pop_agent = mfg_ppo_agent(info_state_size, num_actions).to(device)

  if FLAGS.optimizer == "Adam":
    optimizer_actor = optim.Adam(
        agent.actor.parameters(), lr=FLAGS.lr, eps=1e-5
    )
    optimizer_critic = optim.Adam(
        agent.critic.parameters(), lr=FLAGS.lr, eps=1e-5
    )
  else:
    optimizer_actor = optim.SGD(
        agent.actor.parameters(), lr=FLAGS.lr, momentum=0.9
    )
    optimizer_critic = optim.SGD(
        agent.critic.parameters(), lr=FLAGS.lr, momentum=0.9
    )

  # Used to log data for debugging
  steps = FLAGS.num_episodes * env.max_game_length
  episode_entropy = []
  total_entropy = []
  nash_con_vect = []
  eps_reward = []
  total_reward = []

  for k in range(FLAGS.update_iterations):
    for _ in range(FLAGS.update_episodes):
      # collect rollout data
      history = rollout(
          env, pop_agent, agent, FLAGS.num_episodes, steps, device
      )
      # store rewards and entropy for debugging
      episode_entropy.append(history["entropies"].mean().item())
      eps_reward.append(history["rewards"].sum().item() / FLAGS.num_episodes)
      # Calculate the advantage function
      adv, returns = calculate_advantage(
          FLAGS.gamma,
          True,
          history["rewards"],
          history["values"],
          history["dones"],
          device,
      )
      history["advantages"] = adv
      history["returns"] = returns
      # Update the learned policy and report loss for debugging
      v_loss = learn(
          history,
          optimizer_actor,
          optimizer_critic,
          agent,
          num_minibatches=FLAGS.num_minibatches,
          update_epochs=FLAGS.update_epochs,
          itr_eps=FLAGS.itr_eps,
          eps_eps=FLAGS.eps_eps,
          alpha=FLAGS.alpha,
          ent_coef=FLAGS.ent_coef,
          max_grad_norm=FLAGS.max_grad_norm,
      )

    # Collect and print the metrics
    total_reward.append(np.mean(eps_reward))
    total_entropy.append(np.mean(episode_entropy))

    print("Value_loss", v_loss.item())
    print("iteration num:", k + 1)
    print("Mean reward", total_reward[-1])

    # Update the iteration policy with the new policy
    pop_agent.load_state_dict(agent.state_dict())

    # Update the distribution
    distrib = distribution.DistributionPolicy(game, ppo_policy)

    # calculate the exploitability
    m = calculate_explotability(game, distrib, ppo_policy)
    nashc = m["nash_conv_ppo"]
    nash_con_vect.append(nashc)

    # log the results to tensor board
    tb_writer.add_scalar("initial_state_value", m["ppo_br/initial"], k + 1)
    tb_writer.add_scalar("rewards", total_reward[-1], k + 1)
    tb_writer.add_scalar("entorpy", total_entropy[-1], k + 1)
    tb_writer.add_scalar("nash_conv_ppo", nashc, k + 1)
    logger.debug(
        "ppo_br: %s, and nash_conv: %s, reward: %s, entropy: %s",
        m["ppo_br/initial"],
        nashc,
        total_reward[-1],
        total_entropy[-1],
    )
    print(
        "ppo_br: %s, and nash_conv: %s, reward: %s, entropy: %s"
        % (m["ppo_br/initial"], nashc, total_reward[-1], total_entropy[-1])
    )

    # Update the environment distribution
    env.update_mfg_distribution(distrib)

  # if lower than upper_nash we save the weights and distribution
  upper_nash = 300
  if nash_con_vect[-1] < upper_nash:
    # Save the distribution and weights for further analysis
    filename = os.path.join(fname, f"distribution_{run_name}.pkl")
    utils.save_parametric_distribution(distrib, filename)
    torch.save(
        agent.actor.state_dict(),
        fname
        + f"alpha_{FLAGS.alpha},                itr_eps_{FLAGS.itr_eps},"
        f" eps_eps_{FLAGS.eps_eps}_agent_actor_weights.pth",
    )
    torch.save(
        agent.critic.state_dict(),
        fname
        + f"alpha_{FLAGS.alpha},                itr_eps_{FLAGS.itr_eps},"
        f" eps_eps_{FLAGS.eps_eps}_agent_critic_weights.pth",
    )


def main(unused_argv):
  logging.info("Loading %s", FLAGS.game_name)
  mfg_game = pyspiel.load_game(
      FLAGS.game_name, GAME_SETTINGS.get(FLAGS.game_name, {})
  )

  eta = FLAGS.eta
  regret_steps_per_step = FLAGS.regret_steps_per_step

  best_responder = FLAGS.best_responder
  compute_ce_gap = FLAGS.compute_ce_gap
  compute_internal_regret = FLAGS.compute_internal_regret

  if FLAGS.value_estimator == "sampled":
    value_estimator = utils.sample_value
  elif FLAGS.value_estimator == "exact":
    value_estimator = utils.get_exact_value
  else:
    raise NameError(
        "Unknown value estimator {}. Valid names are `sampled`, `exact`."
        .format(FLAGS.value_estimator)
    )

  if FLAGS.regret_minimizer == "hedge":
    regret_minimizer = hedge.Hedge(
        mfg_game,
        [],
        eta,
        regret_steps_per_step,
        compress_nus=True,
        compress_every=FLAGS.compress_every,
        compress_lbd=FLAGS.compress_lbd,
        value_estimator=value_estimator,
        value_estimation_n=FLAGS.value_estimation_n,
        compute_internal_regret=compute_internal_regret,
    )
  elif FLAGS.regret_minimizer == "rm":
    regret_minimizer = regret_matching.RegretMatching(
        mfg_game,
        [],
        eta,
        regret_steps_per_step,
        compress_nus=True,
        compress_every=FLAGS.compress_every,
        compress_lbd=FLAGS.compress_lbd,
        value_estimator=value_estimator,
        value_estimation_n=FLAGS.value_estimation_n,
        compute_internal_regret=compute_internal_regret,
    )
  elif FLAGS.regret_minimizer == "poly":
    regret_minimizer = polynomial_weights.PolynomialWeightAlgorithm(
        mfg_game,
        [],
        eta,
        regret_steps_per_step,
        compress_nus=True,
        compress_every=FLAGS.compress_every,
        compress_lbd=FLAGS.compress_lbd,
        value_estimator=value_estimator,
        value_estimation_n=FLAGS.value_estimation_n,
        compute_internal_regret=compute_internal_regret,
    )
  else:
    raise NameError(
        "Unknown regret minimizer {}.".format(FLAGS.regret_minimizer)
    )

  if best_responder == "cce":
    best_responder = correlated_equilibrium.cce_br
  elif best_responder == "ce":
    best_responder = correlated_equilibrium.ce_br
  elif best_responder == "ce_partial":
    best_responder = correlated_equilibrium.partial_ce_br
  else:
    raise NameError(
        "Unknown best responder {}. Valid names are `cce` and `ce`.".format(
            FLAGS.best_responder
        )
    )

  mfpsro = mf_psro.MeanFieldPSRO(
      mfg_game,
      regret_minimizer,
      regret_steps_per_step,
      best_responder=best_responder,
  )

  for j in range(FLAGS.n_iter):
    logging.info("Iteration {} of MF-PSRO".format(j))  # pylint: disable=logging-format-interpolation
    print("PSRO Step")
    mfpsro.step()

    print("Equilibrium Computation")
    policies, nus, mus, rhos = mfpsro.get_equilibrium()

    print("Welfare Computation")
    average_welfare = correlated_equilibrium.compute_average_welfare(
        mfg_game, policies, mus, rhos, nus
    )

    print("CCE Gap Computation")
    cce_gap_value = correlated_equilibrium.cce_gap(
        mfg_game, policies, rhos, mus, nus, compute_true_rewards=True
    )
    if compute_ce_gap:
      print("CE Gap Computation")
      ce_gap_value = correlated_equilibrium.ce_gap(
          mfg_game, policies, rhos, mus, nus, compute_true_rewards=True
      )
    else:
      ce_gap_value = 0.0

    print("CCE Gap value : {}".format(cce_gap_value))
    print("CE Gap value : {}".format(ce_gap_value))
    print("Average welfare : {}".format(average_welfare))
    print("")


def main(_):
  """Main function. Runs the experiment."""
  if FLAGS.exp_name is None:
    FLAGS.exp_name = f'{FLAGS.game}_{FLAGS.seed}'
  if not FLAGS.debug:
    wandb.login(key=os.environ.get('WANDB_API_KEY', None))
  wandb.init(
      project='open-spiel-opponent-modelling',
      group=FLAGS.exp_name,
      config={
          'game': FLAGS.game,
          'seed': FLAGS.seed,
          'epochs': FLAGS.epochs,
          'batch_size': FLAGS.batch_size,
          'critic_mini_batches': FLAGS.critic_mini_batches,
          'game_iterations': FLAGS.game_iterations,
          'policy_lr': FLAGS.policy_lr,
          'opp_policy_lr': FLAGS.opp_policy_lr,
          'critic_lr': FLAGS.critic_lr,
          'correction_type': FLAGS.correction_type,
          'n_lookaheads': FLAGS.n_lookaheads,
          'correction_max_grad_norm': FLAGS.correction_max_grad_norm,
          'discount': FLAGS.discount,
          'policy_update_interval': FLAGS.policy_update_interval,
          'use_opponent_modelling': FLAGS.use_opponent_modelling,
          'opp_policy_mini_batches': FLAGS.opp_policy_mini_batches,
          'opponent_model_learning_rate': FLAGS.opponent_model_learning_rate,
      },
      mode='disabled' if FLAGS.debug else 'online',
  )

  rng = hk.PRNGSequence(key_or_seed=FLAGS.seed)
  env = make_env(
      iterations=FLAGS.game_iterations,
      batch_size=FLAGS.batch_size,
      game=FLAGS.game,
  )
  agents = setup_agents(env=env, rng=rng)

  if not FLAGS.use_opponent_modelling:
    update_weights(agents)

  batch = collect_batch(env=env, agents=agents, eval_mode=True)
  log_epoch_data(epoch=0, agents=agents, eval_batch=batch)
  for epoch in range(1, FLAGS.epochs + 1):
    batch = collect_batch(env=env, agents=agents, eval_mode=False)
    if not FLAGS.use_opponent_modelling:
      update_weights(agents)
    log_epoch_data(epoch=epoch, agents=agents, eval_batch=batch)
    print('#' * 100)

  wandb.finish()


def main(_):
  np.random.seed(FLAGS.seed)

  envs = [None, None]
  envs[0] = rl_environment.Environment(
      "repeated_game(stage_game=matrix_rps(),num_repetitions="
      + f"{pyspiel.ROSHAMBO_NUM_THROWS},"
      + f"recall={FLAGS.env_recall})",
      include_full_state=True,
  )
  envs[1] = rl_environment.Environment(
      "repeated_game(stage_game=matrix_rps(),num_repetitions="
      + f"{pyspiel.ROSHAMBO_NUM_THROWS},"
      + f"recall={FLAGS.env_recall})",
      include_full_state=True,
  )
  num_players = 2
  max_abs_reward = max(
      abs(envs[0].game.min_utility()), abs(envs[0].game.max_utility())
  )

  info_state_size = envs[0].observation_spec()["info_state"][0]
  num_actions = envs[0].action_spec()["num_actions"]

  print("Loading population...")
  pop_size = pyspiel.ROSHAMBO_NUM_BOTS
  print(f"Population size: {pop_size}")
  roshambo_bot_names = pyspiel.roshambo_bot_names()
  roshambo_bot_names.sort()
  print_roshambo_bot_names_and_ids(roshambo_bot_names)

  bot_id = 0
  roshambo_bot_ids = {}
  for name in roshambo_bot_names:
    roshambo_bot_ids[name] = bot_id
    bot_id += 1

  print(f"Leave out set size: {FLAGS.leave_out_set_size}")
  train_pop_ids, test_pop_ids = train_test_split(roshambo_bot_ids)
  print(f"Training ids: {train_pop_ids}")
  print(f"Test pop ids: {test_pop_ids}")

  if FLAGS.eval_checkpoint is not None:
    prediction_logger = PredictionLogger(FLAGS.pred_logs_dir)
    eval_checkpoint(roshambo_bot_names, prediction_logger)
    return

  rolling_averager = RollingAverage(FLAGS.window_size)
  expl_rolling_averagers = []
  for _ in range(pyspiel.ROSHAMBO_NUM_BOTS):
    expl_rolling_averagers.append(RollingAverage(FLAGS.window_size))

  print("Looking for checkpoint.")
  if FLAGS.cp_dir is None:
    print("cp_dir is None, disabling checkpointing.")
    # checkpoint = phoenix.Checkpoint()
    checkpoint = None
  else:
    print(f"Looking for checkpoint in {FLAGS.cp_dir}")
    checkpoint = Checkpoint(FLAGS.cp_dir)
    checkpoint.restore_or_save()
    print(f"Checkpoint loaded. ep = {checkpoint.state.ep}")

  if FLAGS.interactive_mode is not None:
    # Must restore an agent from a checkpoint
    assert checkpoint.state.ep is not None
    assert checkpoint.state.learning_agents is not None
    interactive_episode(
        envs[0],
        num_players,
        num_actions,
        roshambo_bot_names,
        checkpoint.state.learning_agent,
    )

  ep = None
  if checkpoint is not None:
    ep = checkpoint.state.ep
    if checkpoint.state.rolling_averager is not None:
      rolling_averager = checkpoint.state.rolling_averager
    if checkpoint.state.expl_rolling_averagers is not None:
      expl_rolling_averagers = checkpoint.state.expl_rolling_averagers
    if checkpoint.state.np_rng_state is not None:
      print("Restoring numpy random state")
      np.random.set_state(checkpoint.state.np_rng_state)

  if ep is None:
    ep = 0
  prediction_logger = PredictionLogger(FLAGS.pred_logs_dir)
  if FLAGS.pred_logs_dir is not None:
    pass  # TODO(author5): Add back in (make full director)

  hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
  # pylint: disable=g-complex-comprehension
  if checkpoint is None or checkpoint.state.learning_agents is None:
    learning_agents = [
        create_training_agent(
            FLAGS.learner,
            num_actions,
            info_state_size,
            hidden_layers_sizes,
            max_abs_reward,
            np.random.randint(100000000),
            player_id,
        )
        for player_id in [0, 1]
    ]
  else:
    learning_agents = checkpoint.state.learning_agents

  print(f"Starting at ep {ep}.")
  total_train_time = 0

  print("Starting training loop...")
  while ep < FLAGS.num_train_episodes:
    # Checkpoint save.
    if checkpoint is not None and ep > 0 and ep % FLAGS.cp_freq == 0:
      print("")
      print(f"Saving checkpoint at ep {ep}...")
      checkpoint.state.ep = ep
      checkpoint.state.np_rng_state = np.random.get_state()
      checkpoint.state.learning_agents = learning_agents
      checkpoint.state.rolling_averager = rolling_averager
      checkpoint.state.expl_rolling_averagers = expl_rolling_averagers
      checkpoint.save()
      print("Done saving checkpoint.")

    if (ep + 1) % FLAGS.eval_every == 0:
      print("")
      eps_per_sec = (ep + 1) / total_train_time
      print(f"Starting eval at ep {ep}. Avg train eps per sec: {eps_per_sec}")
      start_time_eval = time.time()
      eval_returns, pop_expl = eval_agent(
          envs[0],
          num_players,
          num_actions,
          roshambo_bot_names,
          learning_agents[1],
          prediction_logger,
          ep + 1,
      )
      value = eval_returns[1]
      rolling_averager.add(value)
      max_pop_exp = -1000
      for i in range(pyspiel.ROSHAMBO_NUM_BOTS):
        expl_rolling_averagers[i].add(pop_expl[i])
        max_pop_exp = max(max_pop_exp, expl_rolling_averagers[i].mean())
      r_mean = rolling_averager.mean()
      end_time_eval = time.time()
      print(f"Time for eval: {end_time_eval - start_time_eval}")
      data = {
          "episodes": ep + 1,
          "value": value,
          "swa_value": r_mean,
          "expl_swa_value": max_pop_exp,
          "agg_score_swa": r_mean - max_pop_exp,
          "eps_per_sec": eps_per_sec,
      }
      print(data)
      sys.stdout.flush()

    ep_start_time = time.time()
    for learner_pid in range(2):
      agents = [None, None]
      agents[learner_pid] = learning_agents[learner_pid]
      env = envs[learner_pid]
      assert env is not None
      # print(f"Learner pid: {learner_pid}")
      roll = np.random.uniform()

      if roll < FLAGS.prob_selfplay:
        agents[1 - learner_pid] = learning_agents[1 - learner_pid]
        env.set_prediction_label(pyspiel.ROSHAMBO_NUM_BOTS)
      else:
        pop_agent, pop_idx = sample_bot_agent(
            1 - learner_pid, roshambo_bot_names, train_pop_ids, num_actions
        )
        agents[1 - learner_pid] = pop_agent
        env.set_prediction_label(pop_idx)

      time_step = env.reset()
      while not time_step.last():
        time_step2 = copy.deepcopy(time_step)
        player_id = time_step.observations["current_player"]
        agents_output = [agents[0].step(time_step), agents[1].step(time_step2)]
        action_list = [agent_output.action for agent_output in agents_output]
        time_step = env.step(action_list)

      # Episode is over, step all agents with final info state.
      time_step2 = copy.deepcopy(time_step)
      assert agents[0] is not None
      assert agents[1] is not None
      agents[0].step(time_step)
      agents[1].step(time_step2)

    ep_end_time = time.time()
    total_train_time += ep_end_time - ep_start_time
    ep += 1
    print(".", end="")
    sys.stdout.flush()


def main(argv: Sequence[str]) -> None:
  del argv
  config = {"players": FLAGS.players}
  random_seeds_eval = np.random.choice(
      np.array(list(range(1000))), size=FLAGS.random_seed_size, replace=False)

  # Train a meta-cfr agent
  meta_cfr_agent = meta_learning.MetaCFRRegretAgent(
      training_epochs=1,
      meta_learner_training_epochs=FLAGS.meta_learner_training_epochs,
      game_name=FLAGS.game,
      game_config=config,
      perturbation=FLAGS.perturbation,
      seed=FLAGS.random_seed,
      model_type=FLAGS.model_type,
      best_response=True)
  meta_cfr_agent.train()

  cfr_vals = np.zeros((FLAGS.meta_learner_training_epochs,))
  cfr_plus_vals = np.zeros((FLAGS.meta_learner_training_epochs,))

  for seed in list(random_seeds_eval):

    # Evaluate a meta-cfr agent
    world_state = openspiel_api.WorldState(
        FLAGS.game, config, perturbation=True, random_seed=seed)
    meta_cfr_vals = evaluation.CFRBREvaluation(meta_cfr_agent, world_state)

    # Evaluate a cfr plus agent
    game_tree = game_tree_utils.build_game_tree(
        openspiel_api.WorldState(
            FLAGS.game,
            config,
            perturbation=FLAGS.perturbation,
            random_seed=seed))
    _, cfr_plus_vals = cfr.compute_cfr_plus_values(
        game_tree, FLAGS.meta_learner_training_epochs)

    # Evaluate a cfr agent
    game_tree = game_tree_utils.build_game_tree(
        openspiel_api.WorldState(
            FLAGS.game,
            config,
            perturbation=FLAGS.perturbation,
            random_seed=seed))
    _, cfr_vals = cfr.compute_cfr_values(
        game_tree, FLAGS.meta_learner_training_epochs)

  print("Evaluation seed:", random_seeds_eval)
  print("Meta_cfr agent:", meta_cfr_vals)
  print("cfr_plus agent:", cfr_plus_vals)
  print("cfr agent:", cfr_vals)


def main(unused_arg):
  # Construct meta-game payoff tables
  payoff_tables = get_kuhn_poker_data()
  payoffs_are_hpt_format = utils.check_payoffs_are_hpt(payoff_tables)
  strat_labels = utils.get_strat_profile_labels(payoff_tables,
                                                payoffs_are_hpt_format)

  # Run AlphaRank
  rhos, rho_m, pi, _, _ = alpharank.compute(payoff_tables, alpha=1e2)

  # Report & plot results
  alpharank.print_results(
      payoff_tables, payoffs_are_hpt_format, rhos=rhos, rho_m=rho_m, pi=pi)
  utils.print_rankings_table(payoff_tables, pi, strat_labels)
  m_network_plotter = alpharank_visualizer.NetworkPlot(
      payoff_tables, rhos, rho_m, pi, strat_labels, num_top_profiles=8)
  m_network_plotter.compute_and_draw_network()


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  with gfile.Open(os.path.join(FLAGS.path, "config.json")) as f:
    config = json.load(f)
  data = load_jsonl_data(os.path.join(FLAGS.path, "learner.jsonl"))

  print("config:")
  print_columns(sorted("{}: {}\n".format(k, v) for k, v in config.items()))
  print("data keys:")
  try:
    print_columns(sorted(data[0].keys()))
  except IndexError:
    print("The data is not ready")
    return
  print(
      "\ntraining time:", datetime.timedelta(seconds=int(data[-1]["time_rel"]))
  )
  print("training steps: %d" % (data[-1]["step"]))
  print("total states: %d" % (data[-1]["total_states"]))
  print("total trajectories: %d\n" % (data[-1]["total_trajectories"]))

  try:
    plot_data(config, data)
  except KeyboardInterrupt:
    pass


def main(unused_argv):
  model = build_model()

  if FLAGS.visualise:
    nnx_model = (
        utils.linen_to_nnx(model._model)  # pylint: disable=protected-access
        if not isinstance(model, nnx.Module)
        else model
    )
    nnx.display(nnx_model)
  else:
    # In essence, just prepared the model graph for training
    model.save_checkpoint(0)


def main():
    description = "Amalgamate C source and header files."
    usage = " ".join([
        "amalgamate.py",
        "[-v]",
        "-c path/to/config.json",
        "-s path/to/source/dir",
        "[-p path/to/prologue.(c|h)]"
    ])
    argsparser = argparse.ArgumentParser(
        description=description, usage=usage)

    argsparser.add_argument("-v", "--verbose", dest="verbose",
                            choices=["yes", "no"], metavar="", help="be verbose")

    argsparser.add_argument("-c", "--config", dest="config",
                            required=True, metavar="", help="path to a JSON config file")

    argsparser.add_argument("-s", "--source", dest="source_path",
                            required=True, metavar="", help="source code path")

    argsparser.add_argument("-p", "--prologue", dest="prologue",
                            required=False, metavar="", help="path to a C prologue file")

    amalgamation = Amalgamation(argsparser.parse_args())
    amalgamation.generate()


def main(_):
  absltest.main()


def main():
  parser = argparse.ArgumentParser(
      description="Generates abseil.podspec from BUILD.bazel")
  parser.add_argument(
      "-v", "--version", help="The version of podspec", required=True)
  parser.add_argument(
      "-t",
      "--tag",
      default=None,
      help="The name of git tag (default: version)")
  parser.add_argument(
      "-o",
      "--output",
      default="abseil.podspec",
      help="The name of output file (default: abseil.podspec)")
  args = parser.parse_args()
  if args.tag is None:
    args.tag = args.version
  generate(args)


def main(argv):
  if len(argv) > 1:
    raise RuntimeError("generate_copts needs no command line args")

  generate_copt_file(StarlarkStyle())
  generate_copt_file(CMakeStyle())


def main() -> int:
    args = get_args()
    export_lora_parameters(args.npz_file_path, args.adapter_version, args.model_version, args.output_file_path)
    return 0


def main():
    args = parse_arguments()
    data_reader = OnnxModelCalibrationDataReader(model_path=args.input_model_path)
    arg2quant_type = {
        "qint8": QuantType.QInt8,
        "quint8": QuantType.QUInt8,
        "qint16": QuantType.QInt16,
        "quint16": QuantType.QUInt16,
        "qint4": QuantType.QInt4,
        "quint4": QuantType.QUInt4,
        "qfloat8e4m3fn": QuantType.QFLOAT8E4M3FN,
    }
    activation_type = arg2quant_type[args.activation_type]
    weight_type = arg2quant_type[args.weight_type]
    qdq_op_type_per_channel_support_to_axis = dict(args.op_per_channel_axis)
    extra_options = {
        "EnableSubgraph": args.enable_subgraph,
        "ForceQuantizeNoInputCheck": args.force_quantize_no_input_check,
        "MatMulConstBOnly": args.matmul_const_b_only,
        "AddQDQPairToWeight": args.add_qdq_pair_to_weight,
        "OpTypesToExcludeOutputQuantization": args.op_types_to_exclude_output_quantization,
        "DedicatedQDQPair": args.dedicated_qdq_pair,
        "QDQOpTypePerChannelSupportToAxis": qdq_op_type_per_channel_support_to_axis,
        "CalibTensorRangeSymmetric": args.calib_tensor_range_symmetric,
        "CalibMovingAverage": args.calib_moving_average,
        "QuantizeBias": not args.disable_quantize_bias,
        "UseQDQContribOps": args.use_qdq_contrib_ops,
        "MinimumRealRange": args.minimum_real_range,
        "QDQKeepRemovableActivations": args.qdq_keep_removable_activations,
        "QDQDisableWeightAdjustForInt32Bias": args.qdq_disable_weight_adjust_for_int32_bias,
        # Load json file for encoding override
        "TensorQuantOverrides": get_tensor_quant_overrides(args.tensor_quant_overrides),
    }
    arg2calib_method = {
        "minmax": CalibrationMethod.MinMax,
        "entropy": CalibrationMethod.Entropy,
        "percentile": CalibrationMethod.Percentile,
        "distribution": CalibrationMethod.Distribution,
    }
    arg2quant_format = {
        "qdq": QuantFormat.QDQ,
        "qoperator": QuantFormat.QOperator,
    }
    sqc = StaticQuantConfig(
        calibration_data_reader=data_reader,
        calibrate_method=arg2calib_method[args.calibration_method],
        quant_format=arg2quant_format[args.quant_format],
        activation_type=activation_type,
        weight_type=weight_type,
        op_types_to_quantize=None,
        nodes_to_quantize=args.nodes_to_quantize,
        nodes_to_exclude=args.nodes_to_exclude,
        per_channel=args.per_channel,
        reduce_range=False,
        use_external_data_format=False,
        calibration_providers=None,  # Use CPUExecutionProvider
        extra_options=extra_options,
    )
    quantize(model_input=args.input_model_path, model_output=args.output_quantized_model_path, quant_config=sqc)


def main():
    args = parse_args()
    if args.cmd == "extract":
        tuning_results = extract(onnx.load_model(args.input_onnx))
        if tuning_results is None:
            sys.stderr.write(f"{args.input_onnx} does not have tuning results embedded!\n")
            sys.exit(-1)
        json.dump(tuning_results, open(args.output_json, "w"))  # noqa: SIM115
    elif args.cmd == "embed":
        model = onnx.load_model(args.input_onnx)
        merger = Merger()
        for tuning_results in [json.load(open(f)) for f in args.input_json]:  # noqa: SIM115
            merger.merge(tuning_results)
        model = embed(model, merger.get_merged(), args.force)
        onnx.save_model(model, args.output_onnx)
    elif args.cmd == "merge":
        merger = Merger()
        for tuning_results in [json.load(open(f)) for f in args.input_json]:  # noqa: SIM115
            merger.merge(tuning_results)
        json.dump(merger.get_merged(), open(args.output_json, "w"))  # noqa: SIM115
    elif args.cmd == "pprint":
        tuning_results = None
        try:  # noqa: SIM105
            tuning_results = json.load(open(args.json_or_onnx))  # noqa: SIM115
        except Exception:
            # it might be an onnx file otherwise, try it latter
            pass

        if tuning_results is None:
            try:
                model = onnx.load_model(args.json_or_onnx)
                tuning_results = extract(model)
                if tuning_results is None:
                    sys.stderr.write(f"{args.input_onnx} does not have tuning results embedded!\n")
                    sys.exit(-1)
            except Exception:
                pass

        if tuning_results is None:
            sys.stderr.write(f"{args.json_or_onnx} is not a valid tuning results file or onnx file!")
            sys.exit(-1)

        pprint(tuning_results)
    else:
        # invalid choice will be handled by the parser
        pass


def main():
    parser = argparse.ArgumentParser(description="Simple ONNX Runtime Test Tool.")
    parser.add_argument("model_path", help="model path")
    parser.add_argument(
        "num_iters",
        nargs="?",
        type=int,
        default=1000,
        help="model run iterations. default=1000",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="pause execution to allow attaching a debugger.",
    )
    parser.add_argument("--profile", action="store_true", help="enable chrome timeline trace profiling.")
    parser.add_argument(
        "--symbolic_dims",
        default={},
        type=lambda s: dict(x.split("=") for x in s.split(",")),
        help="Comma separated name=value pairs for any symbolic dimensions in the model input. "
        "e.g. --symbolic_dims batch=1,seqlen=5. "
        "If not provided, the value of 1 will be used for all symbolic dimensions.",
    )

    args = parser.parse_args()
    exit_code, _, _ = run_model(args.model_path, args.num_iters, args.debug, args.profile, args.symbolic_dims)
    sys.exit(exit_code)


def main():
    parser = argparse.ArgumentParser(description="Randomize the weights of an ONNX model")
    parser.add_argument("-m", type=str, required=True, help="input onnx model path")
    parser.add_argument("-o", type=str, required=True, help="output onnx model path")
    parser.add_argument(
        "--use_external_data_format",
        required=False,
        action="store_true",
        help="Store or Save in external data format",
    )
    parser.add_argument(
        "--all_tensors_to_one_file",
        required=False,
        action="store_true",
        help="Save all tensors to one file",
    )
    args = parser.parse_args()

    data_path = None
    if args.use_external_data_format:
        if Path(args.m).parent == Path(args.o).parent:
            raise RuntimeError("Please specify output directory with different parent path to input directory.")
        if args.all_tensors_to_one_file:
            data_path = Path(args.o).name + ".data"

    Path(args.o).parent.mkdir(parents=True, exist_ok=True)
    onnx_model = load_model(args.m, load_external_data=args.use_external_data_format)
    graph_iterator(onnx_model, randomize_graph_initializer)
    save_model(
        onnx_model,
        args.o,
        save_as_external_data=args.use_external_data_format,
        all_tensors_to_one_file=args.all_tensors_to_one_file,
        location=data_path,
    )


def main():
    args = parse_arguments()

    setup_logger(args.verbose)

    if args.precision == Precision.FLOAT16 and not args.use_gpu:
        logger.error("fp16 is for GPU only")
        return

    if args.precision == Precision.INT8 and args.use_gpu and args.provider not in ["migraphx"]:
        logger.error("int8 is for CPU only")
        return

    if len(args.models) == 1 and MODELS[args.models[0]][3] in ["vit", "swim"]:
        args.sequence_lengths = [""]

    args.num_threads = sorted({cpu_count if x <= 0 else x for x in args.num_threads})

    logger.info(f"Arguments: {args}")

    if not os.path.exists(args.cache_dir):
        try:
            os.mkdir(args.cache_dir)
        except OSError:
            logger.error("Creation of the directory %s failed", args.cache_dir)

    enable_torch = "torch" in args.engines
    enable_torch2 = "torch2" in args.engines
    enable_torchscript = "torchscript" in args.engines
    enable_onnxruntime = "onnxruntime" in args.engines
    enable_tensorflow = "tensorflow" in args.engines

    if enable_torch2 and version.parse(torch.__version__) < version.parse("2.0.0"):
        logger.error(f"PyTorch version must be >=2.0.0 and you are using {torch.__version__}")
        return

    config_modifier = ConfigModifier(args.force_num_layers)

    results = []

    for num_threads in args.num_threads:
        torch.set_num_threads(num_threads)
        logger.debug(torch.__config__.parallel_info())
        if enable_torch or enable_torch2 or enable_torchscript:
            if args.input_counts != [1]:
                logger.warning("--input_counts is not implemented for torch or torchscript engine.")

            if enable_torchscript:
                results += run_pytorch(
                    args.use_gpu,
                    args.models,
                    args.model_class,
                    config_modifier,
                    args.precision,
                    num_threads,
                    args.batch_sizes,
                    args.sequence_lengths,
                    args.test_times,
                    True,
                    False,
                    args.cache_dir,
                    args.verbose,
                )

            if enable_torch:
                results += run_pytorch(
                    args.use_gpu,
                    args.models,
                    args.model_class,
                    config_modifier,
                    args.precision,
                    num_threads,
                    args.batch_sizes,
                    args.sequence_lengths,
                    args.test_times,
                    False,
                    False,
                    args.cache_dir,
                    args.verbose,
                )

            if enable_torch2:
                results += run_pytorch(
                    args.use_gpu,
                    args.models,
                    args.model_class,
                    config_modifier,
                    args.precision,
                    num_threads,
                    args.batch_sizes,
                    args.sequence_lengths,
                    args.test_times,
                    False,
                    True,
                    args.cache_dir,
                    args.verbose,
                )

        if enable_tensorflow:
            results += run_tensorflow(
                args.use_gpu,
                args.models,
                args.model_class,
                config_modifier,
                args.precision,
                num_threads,
                args.batch_sizes,
                args.sequence_lengths,
                args.test_times,
                args.cache_dir,
                args.verbose,
            )

        model_fusion_statistics = {}
        if enable_onnxruntime:
            try:
                use_raw_attention_mask = not args.use_mask_index
                results += run_onnxruntime(
                    args.use_gpu,
                    args.provider,
                    args.models,
                    args.model_class,
                    config_modifier,
                    args.precision,
                    num_threads,
                    args.batch_sizes,
                    args.sequence_lengths,
                    args.test_times,
                    args.input_counts,
                    args.optimizer_info,
                    args.validate_onnx,
                    args.cache_dir,
                    args.onnx_dir,
                    args.verbose,
                    args.overwrite,
                    args.disable_ort_io_binding,
                    use_raw_attention_mask,
                    model_fusion_statistics,
                    args.model_source,
                    args.enable_arm64_bfloat16_fastmath_mlas_gemm,
                    args,
                )
            except Exception:
                logger.exception("Exception")

    time_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if model_fusion_statistics:
        csv_filename = args.fusion_csv or f"benchmark_fusion_{time_stamp}.csv"
        output_fusion_statistics(model_fusion_statistics, csv_filename)

    if len(results) == 0:
        if args.batch_sizes != [0]:
            logger.warning("No any result available.")
        return

    csv_filename = args.detail_csv or f"benchmark_detail_{time_stamp}.csv"
    output_details(results, csv_filename)

    csv_filename = args.result_csv or f"benchmark_summary_{time_stamp}.csv"
    output_summary(results, csv_filename, args)


def main():
    args = parse_arguments()

    if args.test_times == 0:
        args.test_times = max(1, int(1000 / args.samples))

    if args.average_sequence_length <= 0:
        args.average_sequence_length = args.sequence_length

    manager = multiprocessing.Manager()
    perf_results = manager.dict()

    batch_size_set = set(args.batch_size)
    if not (min(batch_size_set) >= 1 and max(batch_size_set) <= 128):
        raise Exception("batch_size not in range [1, 128]")

    model_setting = ModelSetting(
        args.model,
        args.input_ids_name,
        args.segment_ids_name,
        args.input_mask_name,
        args.opt_level,
        args.input_tuning_results,
        args.output_tuning_results,
        args.mask_type,
    )

    for batch_size in batch_size_set:
        test_setting = TestSetting(
            batch_size,
            args.sequence_length,
            args.samples,
            args.test_times,
            args.use_gpu,
            args.use_io_binding,
            args.provider,
            args.intra_op_num_threads,
            args.seed,
            args.verbose,
            args.log_severity,
            args.average_sequence_length,
            args.random_sequence_length,
        )

        print("test setting", test_setting)
        run_performance(model_setting, test_setting, perf_results)

    # Sort the results so that the first one has smallest latency.
    sorted_results = sorted(perf_results.items(), reverse=False, key=lambda x: x[1])

    summary_file = os.path.join(
        Path(args.model).parent,
        "perf_results_{}_B{}_S{}_{}.txt".format(
            "GPU" if args.use_gpu else "CPU",
            "-".join([str(x) for x in sorted(batch_size_set)]),
            args.sequence_length,
            datetime.now().strftime("%Y%m%d-%H%M%S"),
        ),
    )
    with open(summary_file, "w+", newline="") as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter="\t", lineterminator="\n")
        headers = None
        for key, perf_result in sorted_results:
            params = key.split(",")
            if headers is None:
                headers = [
                    "Latency(ms)",
                    "Latency_P50",
                    "Latency_P75",
                    "Latency_P90",
                    "Latency_P95",
                    "Latency_P99",
                    "Throughput(QPS)",
                ]
                headers.extend([x.split("=")[0] for x in params])
                tsv_writer.writerow(headers)

            values = [format(x, ".2f") for x in perf_result]
            values.extend([x.split("=")[1] for x in params])
            tsv_writer.writerow(values)

    print("Test summary is saved to", summary_file)


def main():
    args = parse_arguments()

    if args.average_sequence_length <= 0:
        args.average_sequence_length = args.sequence_length

    output_dir = args.output_dir
    if output_dir is None:
        # Default output directory is a sub-directory under the directory of model.
        p = Path(args.model)
        output_dir = os.path.join(p.parent, f"batch_{args.batch_size}_seq_{args.sequence_length}")

    if output_dir is not None:
        # create the output directory if not existed
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
    else:
        print("Directory existed. test data files will be overwritten.")

    create_and_save_test_data(
        args.model,
        output_dir,
        args.batch_size,
        args.sequence_length,
        args.samples,
        args.seed,
        args.verbose,
        args.input_ids_name,
        args.segment_ids_name,
        args.input_mask_name,
        args.only_input_tensors,
        args.average_sequence_length,
        args.random_sequence_length,
        args.mask_type,
    )

    print("Test data is saved to directory:", output_dir)


def main():
    args = parse_arguments()

    if args.output_dir is not None:
        # create the output directory if not existed
        path = Path(args.output_dir)
        path.mkdir(parents=True, exist_ok=True)

    run_test(
        args.baseline_model,
        args.optimized_model,
        args.output_dir,
        args.batch_size,
        args.sequence_length,
        args.use_gpu,
        args.samples,
        args.seed,
        args.verbose,
        args.rtol,
        args.atol,
        args.input_ids,
        args.segment_ids,
        args.input_mask,
        args.mask_type,
    )


def main(argv: list[str] | None = None, sentences: list[str] | None = None):
    """Main entry function

    Args:
        argv (Optional[List[str]], optional): _description_. Defaults to None.
        sentences (Optional[List[str]], optional): input text. Defaults to None.

    Raises:
        ValueError: Path does not exist: --encoder_decoder_init_onnx
        ValueError: Path does not exist: --decoder_onnx
        ValueError: --decoder_onnx and --encoder_decoder_init_onnx are not used together for T5

    Returns:
        Union[Dict[str, Any], None]: A dictionary with string with metric name, and value can be integer or string.
    """

    args = parse_arguments(argv)
    setup_logger(args.verbose)

    if args.model_type in ["t5", "mt5"]:
        if args.encoder_decoder_init_onnx and not os.path.exists(args.encoder_decoder_init_onnx):
            raise ValueError(f"Path does not exist: --encoder_decoder_init_onnx {args.encoder_decoder_init_onnx}")
        if args.decoder_onnx and not os.path.exists(args.decoder_onnx):
            raise ValueError(f"Path does not exist: --decoder_onnx {args.decoder_onnx}")
        if (args.encoder_decoder_init_onnx and not args.decoder_onnx) or (
            args.decoder_onnx and not args.encoder_decoder_init_onnx
        ):
            raise ValueError("--decoder_onnx shall use together with --encoder_decoder_init_onnx")

    is_greedy = args.num_beams == 1 and args.num_return_sequences == 1

    if args.model_type == "gpt2" and is_greedy:
        if args.top_p > 0.0 and args.top_p < 1.0:
            convert_generation_model(args, GenerationType.SAMPLING)
            logger.info(
                "The test for gpt2_sampling onnx model is limited to non-custom model with small top_p(e.g <=0.01) value. The result should be the same as gpt2 greedy search."
            )
            if args.top_p > 0.01 or args.custom or args.seed:
                return
        else:
            convert_generation_model(args, GenerationType.GREEDYSEARCH)
    else:
        convert_generation_model(args)

    logger.info("start testing model...")
    if args.model_type in ["t5", "mt5"]:
        result = test_t5_model(args, sentences=sentences)
    else:
        result = test_gpt_model(args, sentences=sentences, is_greedy=is_greedy)

    if result:
        if args.use_external_data_format:
            logger.info(f"Output files: {args.output}, {args.output}.data")
        else:
            logger.info(f"Output file: {args.output}")

    return result


def main():
    args = _parse_arguments()

    _setup_logger(args.verbose)

    logger.debug(f"arguments:{args}")

    if os.path.realpath(args.input) == os.path.realpath(args.output):
        logger.warning("Specified the same input and output path. Note that this may overwrite the original model")

    model = load_model(args.input)
    packing_mode = PackingMode(OnnxModel(model))
    packing_mode.convert()
    packing_mode.model.save_model_to_file(args.output, use_external_data_format=args.use_external_data_format)


def main():
    args = _parse_arguments()

    _setup_logger(args.verbose)

    logger.debug(f"arguments:{args}")

    if os.path.realpath(args.input) == os.path.realpath(args.output):
        logger.warning("Specified the same input and output path. Note that this may overwrite the original model")

    optimization_options = FusionOptions.parse(args)

    optimizer = optimize_model(
        args.input,
        args.model_type,
        args.num_heads,
        args.hidden_size,
        opt_level=args.opt_level,
        optimization_options=optimization_options,
        use_gpu=args.use_gpu,
        provider=args.provider,
        only_onnxruntime=args.only_onnxruntime,
    )

    if args.float16:
        optimizer.convert_float_to_float16(keep_io_types=True)

    if args.input_int32:
        optimizer.change_graph_inputs_to_int32()

    # Print the operator statistics might help end user.
    optimizer.get_operator_statistics()

    fused_op_count = optimizer.get_fused_operator_statistics()
    if "bert" in args.model_type and optimizer.is_fully_optimized(fused_op_count):
        logger.info("The model has been fully optimized.")
    else:
        logger.info("The model has been optimized.")

    if args.convert_to_packing_mode:
        if args.model_type == "bert":
            optimizer.convert_to_packing_mode(not args.disable_symbolic_shape_infer)
        else:
            logger.warning("Packing mode only supports BERT like models")

    optimizer.save_model_to_file(args.output, args.use_external_data_format, convert_attribute=args.convert_attribute)


def main():
    args = parse_arguments()
    setup_logging(args.verbose)

    output_names = None if args.output_names is None else args.output_names.split(";")

    model = ModelProto()
    with open(args.input, "rb") as input_file:
        model.ParseFromString(input_file.read())
    onnx_model = OnnxModel(model)

    optimizer = BertOnnxModelShapeOptimizer(onnx_model)

    optimizer.optimize(
        args.output,
        args.input_ids,
        args.segment_ids,
        args.input_mask,
        args.enable_shape_opt,
        args.enable_reshape_opt,
        output_names,
        args.batch_size,
        args.sequence_length,
        args.verbose,
    )


def main():
    args = parse_arguments()
    print(args)

    for name in ["onnxruntime-gpu", "onnxruntime", "onnx", "torch", "transformers", "optimum", "datasets", "evaluate"]:
        package_version = get_package_version(name)
        if package_version:
            print(f"{name} version", package_version)

    pretrained_model_name = args.model_name
    if args.onnx and not os.path.exists(args.onnx):
        raise RuntimeError(f"Onnx model path does not exist: {args.onnx}")

    disable_fused_attention = os.environ.get("ORT_DISABLE_FUSED_ATTENTION", "0") == "1"

    all_results = []
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
    for sequence_length in args.sequence_lengths:
        tokenizer.model_max_length = sequence_length
        tokenizer.doc_stride = min(sequence_length // 2, 128)
        if args.onnx is None:
            print("Exporting onnx model. It might take a few minutes...")
        start_time = time.time()
        ort_model, onnx_path = load_onnx_model(pretrained_model_name, args.onnx, args.provider, args.use_io_binding)
        latency = time.time() - start_time
        print(f"Onnx model exported or loaded in {latency:.1f} seconds")

        print(ort_model.config)
        if sequence_length > ort_model.config.max_position_embeddings:
            raise RuntimeError("sequence length should not be larger than {ort_model.config.max_position_embeddings}")

        qa_pipeline = pipeline(
            "question-answering", model=ort_model, tokenizer=tokenizer, question_first=True, batch_size=args.batch_size
        )

        task_evaluator = evaluator("question-answering")
        print("Loading dataset...")
        start_time = time.time()
        squad_dataset = load_dataset("squad", split=f"validation[:{args.total}]" if args.total > 0 else "validation")
        latency = time.time() - start_time
        print(f"Dataset loaded in {latency:.1f} seconds")

        print("Evaluating squad_v2 with ORT. It might take a few minutes...")
        start_time = time.time()
        result = task_evaluator.compute(
            model_or_pipeline=qa_pipeline,
            data=squad_dataset,
            metric="squad_v2",
            squad_v2_format=True,
        )
        latency = time.time() - start_time
        print(f"Evaluation done in {latency:.1f} seconds")

        result["provider"] = args.provider
        result["disable_fused_attention"] = disable_fused_attention
        result["pretrained_model_name"] = pretrained_model_name
        result["onnx_path"] = onnx_path
        result["batch_size"] = args.batch_size
        result["sequence_length"] = sequence_length
        result["use_io_binding"] = args.use_io_binding
        print(result)

        all_results.append(result)

    output_details(all_results, "detail.csv")

    for metric_name in ["f1", "exact", "samples_per_second"]:
        output_summary(all_results, f"{metric_name}.csv", metric_name)


def main(args):
    if version.parse(transformers_version) < version.parse(
        "3.1.0"
    ):  # past_key_values name does not exist in 3.0.2 or older
        raise RuntimeError("This tool requires transformers 3.1.0 or later.")

    logger.info(f"Arguments:{args}")
    if args.precision == Precision.FLOAT16:
        assert args.optimize_onnx and args.use_gpu, "fp16 requires --optimize_onnx --use_gpu"

    if args.precision == Precision.INT8:
        assert not args.use_gpu, "quantization only supports CPU"

    if args.stage == 1:
        assert args.past_sequence_lengths == [0], "past_sequence_lengths shall be 0 for stage==1 (init decoder)"

    torch.set_num_threads(psutil.cpu_count(logical=True) if args.thread_num <= 0 else args.thread_num)
    print(torch.__config__.parallel_info())

    cache_dir = args.cache_dir
    output_dir = args.onnx_dir
    prepare_environment(cache_dir, output_dir, args.use_gpu)

    model_class = MODEL_CLASSES[args.model_class][0]
    gpt2helper = Gpt2Helper
    config = AutoConfig.from_pretrained(args.model_name_or_path, torchscript=args.torchscript, cache_dir=cache_dir)
    model = model_class.from_pretrained(args.model_name_or_path, config=config, cache_dir=cache_dir)

    # This script does not support float16 for PyTorch.
    # if args.float16:
    #    model.half()

    device = torch.device("cuda:0" if args.use_gpu else "cpu")
    model.to(device)
    use_external_data_format = config.n_layer > 24  # TODO: find a way to check model size > 2GB
    onnx_model_paths = gpt2helper.get_onnx_paths(
        output_dir,
        args.model_name_or_path,
        args.model_class,
        has_past=True,
        new_folder=use_external_data_format,
    )

    onnx_model_path = onnx_model_paths["raw"]
    use_padding = MODEL_CLASSES[args.model_class][2]
    gpt2helper.export_onnx(
        model,
        device,
        onnx_model_path,
        args.verbose,
        use_external_data_format,
        has_position_ids=use_padding,
        has_attention_mask=use_padding,
    )

    if args.optimize_onnx or args.precision != Precision.FLOAT32:
        onnx_model_path = onnx_model_paths[str(args.precision) if args.precision != Precision.INT8 else "fp32"]
        gpt2helper.optimize_onnx(
            onnx_model_paths["raw"],
            onnx_model_path,
            args.precision == Precision.FLOAT16,
            model.config.num_attention_heads,
            model.config.hidden_size,
            use_external_data_format,
            auto_mixed_precision=True,
            stage=args.stage,
        )

        if args.precision == Precision.INT8:
            logger.info("quantizing model...")
            QuantizeHelper.quantize_onnx_model(onnx_model_path, onnx_model_paths["int8"], use_external_data_format)
            model = QuantizeHelper.quantize_torch_model(model)
            logger.info("finished quantizing model")
            onnx_model_path = onnx_model_paths["int8"]

    if args.torchscript:
        model = gpt2helper.torchscript(
            model,
            config,
            device,
            has_position_ids=use_padding,
            has_attention_mask=use_padding,
        )

    session = create_onnxruntime_session(
        onnx_model_path,
        args.use_gpu,
        enable_all_optimization=False,
        num_threads=args.thread_num,
        verbose=args.verbose,
    )
    if session is None:
        return

    # Allocate output buffers for IO Binding
    max_output_shapes = gpt2helper.get_output_shapes(
        max(args.batch_sizes),
        max(args.past_sequence_lengths),
        max(args.sequence_lengths),
        config,
        args.model_class,
    )
    output_buffers = gpt2helper.get_output_buffers(max_output_shapes, device, args.precision == Precision.FLOAT16)

    csv_filename = args.result_csv or "benchmark_result_{}.csv".format(datetime.now().strftime("%Y%m%d-%H%M%S"))
    with open(csv_filename, mode="a", newline="") as csv_file:
        column_names = [
            "model_name",
            "model_class",
            "stage",
            "environment_variables",
            "gpu",
            "precision",
            "optimizer",
            "torchscript",
            "batch_size",
            "sequence_length",
            "past_sequence_length",
            "disable_io_binding",
            "torch_latency",
            "onnxruntime_latency",
        ]
        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        csv_writer.writeheader()

        for batch_size in args.batch_sizes:
            for sequence_length in args.sequence_lengths:
                for past_sequence_length in args.past_sequence_lengths:
                    assert batch_size > 0 and sequence_length > 0 and past_sequence_length >= 0
                    logger.debug(
                        "Running test for batch_size=%d sequence_length=%d past_sequence_length=%d ...",
                        batch_size,
                        sequence_length,
                        past_sequence_length,
                    )

                    dummy_inputs = gpt2helper.get_dummy_inputs(
                        batch_size,
                        past_sequence_length,
                        sequence_length,
                        config.num_attention_heads,
                        config.hidden_size,
                        config.n_layer,
                        config.vocab_size,
                        device,
                        float16=(args.precision == Precision.FLOAT16),
                        has_position_ids=use_padding,
                        has_attention_mask=use_padding,
                    )
                    output_shapes = gpt2helper.get_output_shapes(
                        batch_size,
                        past_sequence_length,
                        sequence_length,
                        config,
                        args.model_class,
                    )

                    try:
                        if args.validate_onnx or args.output_torch_latency:
                            outputs, torch_latency = gpt2helper.pytorch_inference(model, dummy_inputs, args.test_times)

                            # Dump Torch output shape
                            for i, value in enumerate(outputs):
                                if isinstance(value, tuple):
                                    logger.debug(
                                        f"torch output {i} is tuple of size {len(value)}, shape {value[0].shape}"
                                    )
                                else:
                                    logger.debug(f"torch output {i} shape {value.shape}")
                        else:
                            outputs = None
                            torch_latency = None

                        if args.disable_io_binding:
                            ort_outputs, ort_latency = gpt2helper.onnxruntime_inference(
                                session, dummy_inputs, args.test_times
                            )
                        else:
                            ort_outputs, ort_latency = gpt2helper.onnxruntime_inference_with_binded_io(
                                session,
                                dummy_inputs,
                                output_buffers,
                                output_shapes,
                                args.test_times,
                                return_numpy=False,
                                include_copy_output_latency=args.include_copy_output_latency,
                            )

                        if args.validate_onnx:
                            copy_outputs = ort_outputs
                            if not args.disable_io_binding:
                                # Results of IO binding might be in GPU. Copy outputs to CPU for comparison.
                                copy_outputs = []
                                for output in ort_outputs:
                                    copy_outputs.append(output.cpu().numpy())

                            if gpt2helper.compare_outputs(
                                outputs,
                                copy_outputs,
                                model_class=args.model_class,
                                rtol=DEFAULT_TOLERANCE[args.precision],
                                atol=DEFAULT_TOLERANCE[args.precision],
                            ):
                                logger.info(
                                    f"Pytorch and ONNX Runtime outputs are all close (tolerance={DEFAULT_TOLERANCE[args.precision]})."
                                )

                        logger.info(
                            "batch_size=%d, sequence_length=%d, past_sequence_length=%d, onnxruntime_latency=%.2f %s %s",
                            batch_size,
                            sequence_length,
                            past_sequence_length,
                            ort_latency,
                            "(disable_io_binding)" if args.disable_io_binding else "",
                            ", torch_latency={torch_latency}" if torch_latency else "",
                        )

                        row = {
                            "model_name": args.model_name_or_path,
                            "model_class": args.model_class,
                            "stage": args.stage,
                            "environment_variables": get_ort_environment_variables(),
                            "gpu": args.use_gpu,
                            "precision": args.precision,
                            "optimizer": args.optimize_onnx,
                            "torchscript": args.torchscript,
                            "batch_size": batch_size,
                            "sequence_length": sequence_length,
                            "past_sequence_length": past_sequence_length,
                            "disable_io_binding": args.disable_io_binding,
                            "torch_latency": f"{torch_latency:.2f}" if torch_latency else "None",
                            "onnxruntime_latency": f"{ort_latency:.2f}",
                        }
                        csv_writer.writerow(row)
                    except Exception:
                        logger.error("Exception", exc_info=True)  # noqa: G201
                        return None

    logger.info(f"Results are saved to file {csv_filename}")
    return csv_filename


def main(argv=None, experiment_name: str = "", run_id: str = "0", csv_filename: str = "gpt2_parity_results.csv"):
    warnings.warn(
        "This example is deprecated. Use the Olive recipe instead: "
        "https://github.com/microsoft/olive-recipes/tree/main",
        DeprecationWarning,
        stacklevel=2,
    )

    result = {}
    if version.parse(transformers_version) < version.parse(
        "3.1.0"
    ):  # past_key_values name does not exist in 3.0.2 or older
        raise RuntimeError("This tool requires transformers 3.1.0 or later.")

    args = parse_arguments(argv)
    setup_logger(args.verbose)

    if not experiment_name:
        experiment_name = " ".join(argv if argv else sys.argv[1:])

    if args.tolerance == 0:
        args.tolerance = DEFAULT_TOLERANCE[args.precision]

    logger.info(f"Arguments:{args}")

    cache_dir = args.cache_dir
    output_dir = args.output if not args.output.endswith(".onnx") else os.path.dirname(args.output)
    prepare_environment(cache_dir, output_dir, args.use_gpu)

    if args.precision != Precision.FLOAT32:
        assert args.optimize_onnx, "fp16/int8 requires --optimize_onnx"

    if args.precision == Precision.FLOAT16:
        assert args.use_gpu, "fp16 requires --use_gpu"

    if args.precision == Precision.INT8:
        assert not args.use_gpu, "quantization only supports CPU"

    model_class = MODEL_CLASSES[args.model_class][0]
    use_padding = MODEL_CLASSES[args.model_class][2]

    gpt2helper = Gpt2Helper
    config = AutoConfig.from_pretrained(args.model_name_or_path, cache_dir=cache_dir)
    model = model_class.from_pretrained(args.model_name_or_path, config=config, cache_dir=cache_dir)

    device = torch.device("cuda:0" if args.use_gpu else "cpu")
    model.eval().to(device)

    if (not args.use_external_data_format) and (config.n_layer > 24):
        logger.info("Try --use_external_data_format when model size > 2GB")

    onnx_model_paths = gpt2helper.get_onnx_paths(
        output_dir,
        args.model_name_or_path,
        args.model_class,
        new_folder=(args.precision == Precision.INT8),
        remove_existing=["fp32", "fp16", "int8"],
    )  # Do not remove raw model to save time in parity test

    raw_onnx_model = onnx_model_paths["raw"]

    int_data_type = torch.int64 if args.use_int64_inputs else torch.int32

    if os.path.exists(raw_onnx_model) and not args.overwrite:
        logger.warning(f"Skip exporting ONNX model since it existed: {raw_onnx_model}")
    else:
        logger.info(f"Exporting ONNX model to {raw_onnx_model}")
        gpt2helper.export_onnx(
            model,
            device,
            raw_onnx_model,
            args.verbose,
            args.use_external_data_format,
            has_position_ids=use_padding,
            has_attention_mask=use_padding,
            input_ids_dtype=int_data_type,
            position_ids_dtype=int_data_type,
            attention_mask_dtype=int_data_type,
        )

    fp16_params = {"keep_io_types": args.keep_io_types}
    if args.io_block_list:
        fp16_params["keep_io_types"] = args.io_block_list
    if args.node_block_list:
        fp16_params["node_block_list"] = args.node_block_list
    if args.op_block_list:
        fp16_params["op_block_list"] = args.op_block_list
    if args.force_fp16_initializers:
        fp16_params["force_fp16_initializers"] = args.force_fp16_initializers

    is_io_float16 = args.precision == Precision.FLOAT16 and not args.keep_io_types

    optimized_ops = ""
    all_ops = ""
    if args.optimize_onnx or args.precision != Precision.FLOAT32:
        output_path = onnx_model_paths[str(args.precision) if args.precision != Precision.INT8 else "fp32"]

        logger.info(f"Optimizing model to {output_path}")
        m = gpt2helper.optimize_onnx(
            raw_onnx_model,
            output_path,
            args.precision == Precision.FLOAT16,
            model.config.num_attention_heads,
            model.config.hidden_size,
            args.use_external_data_format,
            auto_mixed_precision=args.auto_mixed_precision,
            stage=args.stage,
            **fp16_params,
        )

        nodes = m.nodes()
        op_list = {node.op_type for node in nodes}
        all_ops = ",".join(op_list)

        # print optimized operators
        optimized_op_counter = m.get_fused_operator_statistics()
        if optimized_op_counter:
            optimized_ops = ",".join([key for key in optimized_op_counter if optimized_op_counter[key] > 0])
    else:
        output_path = raw_onnx_model

    if args.precision == Precision.INT8:
        logger.info("quantizing model...")
        QuantizeHelper.quantize_onnx_model(output_path, onnx_model_paths["int8"], args.use_external_data_format)
        model = QuantizeHelper.quantize_torch_model(model)
        logger.info("finished quantizing model")
        output_path = onnx_model_paths["int8"]

    if args.output.endswith(".onnx") and output_path != args.output and not args.use_external_data_format:
        shutil.move(output_path, args.output)
        output_path = args.output

    logger.info(f"Output path: {output_path}")
    model_size_in_MB = int(get_onnx_model_size(output_path, args.use_external_data_format) / 1024 / 1024)  # noqa: N806

    provider = args.provider
    session = create_onnxruntime_session(
        output_path, args.use_gpu, provider, enable_all_optimization=True, verbose=args.verbose
    )
    if args.model_class == "GPT2LMHeadModel" and session is not None:
        parity_result = gpt2helper.test_parity(
            session,
            model,
            device,
            is_io_float16,
            rtol=args.tolerance,
            atol=args.tolerance,
            model_class=args.model_class,
            has_position_ids=use_padding,
            has_attention_mask=use_padding,
            input_ids_dtype=int_data_type,
            position_ids_dtype=int_data_type,
            attention_mask_dtype=int_data_type,
            test_cases_per_run=args.test_cases,
            total_runs=args.test_runs,
            stage=args.stage,
            verbose=args.verbose,
        )

        # An example configuration for testing performance
        batch_size = 8
        sequence_length = 32 if args.stage == 1 else 1
        past_sequence_length = 0 if args.stage == 1 else 32

        latency = gpt2helper.test_performance(
            session,
            model,
            device,
            is_io_float16,
            total_runs=100,
            use_io_binding=True,
            model_class=args.model_class,
            has_position_ids=use_padding,
            has_attention_mask=use_padding,
            input_ids_dtype=int_data_type,
            position_ids_dtype=int_data_type,
            attention_mask_dtype=int_data_type,
            batch_size=batch_size,
            sequence_length=sequence_length,
            past_sequence_length=past_sequence_length,
        )

        if args.precision == Precision.FLOAT16:
            logger.info(f"fp16 conversion parameters:{fp16_params}")

        # Write results to file
        latency_name = get_latency_name(batch_size, sequence_length, past_sequence_length)
        csv_file_existed = os.path.exists(csv_filename)
        with open(csv_filename, mode="a", newline="") as csv_file:
            column_names = [
                "experiment",
                "run_id",
                "model_name",
                "model_class",
                "stage",
                "gpu",
                "precision",
                "optimizer",
                "test_cases",
                "runs",
                "keep_io_types",
                "io_block_list",
                "op_block_list",
                "node_block_list",
                "force_fp16_initializers",
                "auto_mixed_precision",
                "optimized_operators",
                "operators",
                "environment_variables",
                "onnxruntime",
                latency_name,
                "top1_match_rate",
                "onnx_size_in_MB",
                "diff_50_percentile",
                "diff_90_percentile",
                "diff_95_percentile",
                "diff_99_percentile",
                "diff_pass_rate",
                "nan_rate",
                "top1_match_rate_per_run",
            ]
            csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
            if not csv_file_existed:
                csv_writer.writeheader()
            row = {
                "experiment": experiment_name,
                "run_id": run_id,
                "model_name": args.model_name_or_path,
                "model_class": args.model_class,
                "stage": args.stage,
                "gpu": args.use_gpu,
                "precision": args.precision,
                "optimizer": args.optimize_onnx,
                "test_cases": args.test_cases,
                "runs": args.test_runs,
                "keep_io_types": args.keep_io_types,
                "io_block_list": args.io_block_list,
                "op_block_list": args.op_block_list,
                "node_block_list": args.node_block_list,
                "force_fp16_initializers": args.force_fp16_initializers,
                "auto_mixed_precision": args.auto_mixed_precision,
                "optimized_operators": optimized_ops,
                "operators": all_ops,
                "environment_variables": get_ort_environment_variables(),
                "onnxruntime": ort_version,
                latency_name: f"{latency:.2f}",
                "diff_50_percentile": parity_result["max_diff_percentile_50"],
                "diff_90_percentile": parity_result["max_diff_percentile_90"],
                "diff_95_percentile": parity_result["max_diff_percentile_95"],
                "diff_99_percentile": parity_result["max_diff_percentile_99"],
                "diff_pass_rate": parity_result["diff_pass_rate"],
                "nan_rate": parity_result["nan_rate"],
                "top1_match_rate": parity_result["top1_match_rate"],
                "top1_match_rate_per_run": parity_result["top1_match_rate_per_run"],
                "onnx_size_in_MB": f"{model_size_in_MB}",
            }
            logger.info(f"result: {row}")
            result.update(row)
            csv_writer.writerow(row)

    if args.input_test_file:
        test_inputs = []
        # Each line of test file is a JSON string like:
        # {"input_ids": [[14698, 257, 1310, 13688, 319, 326]]}
        with open(args.input_test_file) as read_f:
            for _, line in enumerate(read_f):
                line = line.rstrip()  # noqa: PLW2901
                data = json.loads(line)
                input_ids = torch.from_numpy(numpy.asarray(data["input_ids"], dtype=numpy.int64)).to(device)

                if use_padding:
                    if "attention_mask" in data:
                        numpy_float = numpy.float16 if is_io_float16 else numpy.float32
                        attention_mask = torch.from_numpy(numpy.asarray(data["attention_mask"], dtype=numpy_float)).to(
                            device
                        )
                    else:
                        padding = -1
                        attention_mask = (input_ids != padding).type(torch.float16 if is_io_float16 else torch.float32)
                        input_ids.masked_fill_(input_ids == padding, 0)

                    if "position_ids" in data:
                        position_ids = torch.from_numpy(numpy.asarray(data["position_ids"], dtype=numpy.int64)).to(
                            device
                        )
                    else:
                        position_ids = attention_mask.long().cumsum(-1) - 1
                        position_ids.masked_fill_(position_ids < 0, 0)

                    inputs = {
                        "input_ids": input_ids.to(int_data_type),
                        "position_ids": position_ids.to(int_data_type),
                        "attention_mask": attention_mask.to(int_data_type),
                    }
                else:
                    inputs = {"input_ids": input_ids.to(int_data_type)}

                test_inputs.append(inputs)

        Gpt2Tester.test_generation(
            session,
            model,
            device,
            test_inputs,
            precision=args.precision,
            model_class=args.model_class,
            top_k=20,
            top_k_no_order=True,
            max_steps=24,
            max_inputs=0,
            verbose=args.verbose,
            save_test_data=3,
            save_test_data_dir=Path(output_path).parent,
        )

    logger.info(f"Done. Output model: {output_path}")
    return result


def main():
    rank = get_rank()
    world_size = get_size()

    args = get_args(rank)
    setup_logger(args.verbose)
    logger.info(args.__dict__)
    torch.backends.cudnn.benchmark = True

    args.rank = rank
    args.world_size = world_size
    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name, cache_dir=args.cache_dir, use_auth_token=args.auth, trust_remote_code=args.auth
    )
    config = AutoConfig.from_pretrained(
        args.model_name, cache_dir=args.cache_dir, use_auth_token=args.auth, trust_remote_code=args.auth
    )
    target_device = f"cuda:{args.rank}" if args.device != "cpu" else args.device
    use_fp16 = args.precision == "fp16"

    setattr(args, "tokenizer", tokenizer)  # noqa: B010
    setattr(args, "config", config)  # noqa: B010
    setattr(args, "target_device", target_device)  # noqa: B010
    setattr(args, "use_fp16", use_fp16)  # noqa: B010

    # Get model and model info
    model = get_model(args)
    ort_model_inputs_len = get_ort_model_inputs_len(args, model)

    # Check if past_present_share_buffer can be enabled (only for FP16 models with GQA)
    if args.benchmark_type in {"ort-convert-to-onnx", "ort-msft"}:
        onnx_model = onnx.load_model(args.ort_model_path.format(args.rank), load_external_data=False)
        gqa_nodes = list(filter(lambda node: node.op_type == "GroupQueryAttention", onnx_model.graph.node))

        use_buffer_share = use_fp16 and len(gqa_nodes) > 0 and args.device != "cpu"
        setattr(args, "use_buffer_share", use_buffer_share)  # noqa: B010
    else:
        setattr(args, "use_buffer_share", False)  # noqa: B010

    # Measure prompt cost (init_inputs) and generated token cost (iter_inputs)
    for batch_size, sequence_length in itertools.product(args.batch_sizes, args.sequence_lengths):
        if args.rank == 0:
            logger.info(f"\nBatch size = {batch_size} and sequence length = {sequence_length}...")
        setattr(args, "batch_size", int(batch_size))  # noqa: B010
        setattr(args, "sequence_length", int(sequence_length))  # noqa: B010

        init_inputs, iter_inputs = get_inputs(args, ort_model_inputs_len)
        run_inference(args, init_inputs, iter_inputs, model)


def main():
    args = get_args()
    setup_logger(args.verbose)
    logger.info(args.__dict__)
    torch.backends.cudnn.benchmark = True

    all_results = []
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.device_id)

    # Benchmark PyTorch without torch.compile
    if args.hf_pt_eager:
        benchmark_cmd = [
            "python",
            "-m",
            "models.llama.benchmark",
            "--benchmark-type",
            "hf-pt-eager",
            "--model-name",
            args.model_name,
            "--precision",
            args.precision,
            "--batch-sizes",
            args.batch_sizes,
            "--sequence-lengths",
            args.sequence_lengths,
            "--device",
            args.device,
            "--warmup-runs",
            str(args.warmup_runs),
            "--num-runs",
            str(args.num_runs),
            "--log-folder",
            args.log_folder,
            "--cache-dir",
            args.cache_dir,
            "--auth",
        ]
        logger.info("Benchmark PyTorch without torch.compile")
        results = benchmark(args, benchmark_cmd, "pytorch-eager")
        all_results.extend(results)

    # Benchmark PyTorch with torch.compile
    if args.hf_pt_compile:
        benchmark_cmd = [
            "python",
            "-m",
            "models.llama.benchmark",
            "--benchmark-type",
            "hf-pt-compile",
            "--model-name",
            args.model_name,
            "--precision",
            args.precision,
            "--batch-sizes",
            args.batch_sizes,
            "--sequence-lengths",
            args.sequence_lengths,
            "--device",
            args.device,
            "--warmup-runs",
            str(args.warmup_runs),
            "--num-runs",
            str(args.num_runs),
            "--log-folder",
            args.log_folder,
            "--cache-dir",
            args.cache_dir,
            "--auth",
        ]
        logger.info("Benchmark PyTorch with torch.compile")
        results = benchmark(args, benchmark_cmd, "pytorch-compile")
        all_results.extend(results)

    # Benchmark Optimum + ONNX Runtime
    if args.hf_ort_dir_path:
        benchmark_cmd = [
            "python",
            "-m",
            "models.llama.benchmark",
            "--benchmark-type",
            "hf-ort",
            "--hf-ort-dir-path",
            args.hf_ort_dir_path,
            "--model-name",
            args.model_name,
            "--precision",
            args.precision,
            "--batch-sizes",
            args.batch_sizes,
            "--sequence-lengths",
            args.sequence_lengths,
            "--device",
            args.device,
            "--warmup-runs",
            str(args.warmup_runs),
            "--num-runs",
            str(args.num_runs),
            "--log-folder",
            args.log_folder,
            "--cache-dir",
            args.cache_dir,
            "--auth",
        ]
        logger.info("Benchmark Optimum + ONNX Runtime")
        results = benchmark(args, benchmark_cmd, "optimum-ort")
        all_results.extend(results)

    # Benchmark Microsoft model in ONNX Runtime
    if args.ort_msft_model_path:
        benchmark_cmd = [
            "python",
            "-m",
            "models.llama.benchmark",
            "--benchmark-type",
            "ort-msft",
            "--ort-model-path",
            args.ort_msft_model_path,
            "--model-name",
            args.model_name,
            "--precision",
            args.precision,
            "--batch-sizes",
            args.batch_sizes,
            "--sequence-lengths",
            args.sequence_lengths,
            "--device",
            args.device,
            "--warmup-runs",
            str(args.warmup_runs),
            "--num-runs",
            str(args.num_runs),
            "--log-folder",
            args.log_folder,
            "--cache-dir",
            args.cache_dir,
        ]
        logger.info("Benchmark Microsoft model in ONNX Runtime")
        results = benchmark(args, benchmark_cmd, "ort-msft")
        all_results.extend(results)

    # Benchmark convert_to_onnx model in ONNX Runtime
    if args.ort_convert_to_onnx_model_path:
        benchmark_cmd = [
            "python",
            "-m",
            "models.llama.benchmark",
            "--benchmark-type",
            "ort-convert-to-onnx",
            "--ort-model-path",
            args.ort_convert_to_onnx_model_path,
            "--model-name",
            args.model_name,
            "--precision",
            args.precision,
            "--batch-sizes",
            args.batch_sizes,
            "--sequence-lengths",
            args.sequence_lengths,
            "--device",
            args.device,
            "--warmup-runs",
            str(args.warmup_runs),
            "--num-runs",
            str(args.num_runs),
            "--log-folder",
            args.log_folder,
            "--cache-dir",
            args.cache_dir,
        ]
        logger.info("Benchmark convert_to_onnx model in ONNX Runtime")
        results = benchmark(args, benchmark_cmd, "onnxruntime")
        all_results.extend(results)

    csv_file = f"{args.model_size}_{args.precision}_{datetime.datetime.now():%Y-%m-%d_%H:%M:%S}.csv"
    save_results(all_results, os.path.join(args.log_folder, csv_file))


def main():
    args = get_args()
    setup_logger(False)
    logger.info(args.__dict__)

    # Get prompts and prompt sizes
    size_to_prompt = None
    with open(args.prompts_file) as f:
        size_to_prompt = json.load(f, object_hook=lambda d: {int(k): v for k, v in d.items()})

    # Get config, tokenizer, and model
    config = AutoConfig.from_pretrained(
        args.hf_dir_path if args.hf_dir_path != "" else args.model_name,
        cache_dir=args.cache_dir,
        use_auth_token=args.auth,
        trust_remote_code=args.trust,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        args.hf_dir_path if args.hf_dir_path != "" else args.model_name,
        cache_dir=args.cache_dir,
        use_auth_token=args.auth,
        trust_remote_code=args.trust,
    )
    model = get_model(args)

    all_csv_metrics = []
    for batch_size, prompt_length in itertools.product(args.batch_sizes, args.prompt_lengths):
        batch_size, prompt_length = int(batch_size), int(prompt_length)  # noqa: PLW2901
        logger.info(f"Running batch size = {batch_size}, prompt length = {prompt_length}")
        clear_cache()
        max_length = prompt_length + args.generation_length

        if prompt_length not in size_to_prompt:
            raise NotImplementedError(
                textwrap.dedent(
                    f"""
                                A prompt of size {prompt_length} was not found in '{args.prompts_file}'. There are a couple of solutions to fix this.
                                1) You can change one of the keys in '{args.prompts_file}' to be {prompt_length}.
                                    If {prompt_length} < actual prompt's length, the benchmark E2E tool will repeat the first word in the prompt until {prompt_length} = actual prompt's length.
                                    If {prompt_length} > actual prompt's length, the benchmark E2E tool will automatically trim the actual prompt's length so that {prompt_length} = actual prompt's length.
                                2) You can add a new key-value entry in '{args.prompts_file}' of the form '{prompt_length}': 'your prompt goes here'.
                """
                )
            )
        prompt = [size_to_prompt[prompt_length]] * batch_size
        csv_metrics = [batch_size, prompt_length]

        try:
            # Measure prompt processing
            logger.info("Measuring prompt processing...")
            inputs, outputs = prepare_model_for_inference(args, model, config, tokenizer, prompt_length, prompt)
            accelerator_prompt_latency_s, outputs = run_inference(args, model, args.num_runs, inputs, outputs)

            # Calculate prompt metrics
            accelerator_prompt_latency_ms = accelerator_prompt_latency_s * 1000
            accelerator_prompt_thrpt = batch_size * (prompt_length / accelerator_prompt_latency_s)
            logger.info(f"Average Latency of Prompt Processing: {accelerator_prompt_latency_ms} ms")
            logger.info(
                f"Average Throughput of Prompt Processing: {batch_size * (prompt_length / accelerator_prompt_latency_s)} tps"
            )
            csv_metrics.extend([accelerator_prompt_latency_ms, accelerator_prompt_thrpt])

            # Measure token generation
            logger.info("Measuring token generation...")
            clear_cache()
            inputs, outputs = prepare_model_for_inference(args, model, config, tokenizer, prompt_length, prompt)

            all_token_ids = inputs["input_ids"].clone()
            current_length = all_token_ids.shape[-1]
            num_heads = config.num_key_value_heads
            head_size = (
                config.head_dim if hasattr(config, "head_dim") else config.hidden_size // config.num_attention_heads
            )

            has_eos = torch.zeros(batch_size, device=args.target_device, dtype=torch.bool)

            # 0th entry will have prompt accelerator time, 1st entry onwards will have token generation accelerator time
            accelerator_times = []
            sampling_times = []  # cost to sample after each model run

            wall_clock_start_time = time.perf_counter()
            while current_length <= max_length:
                # Run inference
                accelerator_time_latency_s, outputs = run_inference(args, model, 1, inputs, outputs)
                accelerator_times.append(accelerator_time_latency_s)

                # Sample with argmax (greedy search)
                sampling_start_time = time.perf_counter()
                if outputs["logits"].shape[1] > 1:
                    prompt_end_indices = inputs["attention_mask"].sum(1) - 1
                    idxs = (
                        prompt_end_indices.unsqueeze(dim=1)
                        .repeat(1, config.vocab_size)
                        .view(batch_size, 1, config.vocab_size)
                    )
                    next_token_logits = torch.gather(outputs["logits"], 1, idxs).squeeze()
                else:
                    next_token_logits = outputs["logits"][:, -1, :]
                next_tokens = torch.argmax(next_token_logits, dim=-1)

                # Check if we previously reached EOS token id or if generated token id is EOS token id
                has_eos = has_eos | next_tokens == tokenizer.eos_token_id

                # Determine which new tokens to add to list of all token ids
                # Add EOS token ids for batch entries that ended early (ragged batching scenario where some batch entries ended early and some haven't)
                tokens_to_add = next_tokens.masked_fill(has_eos, tokenizer.eos_token_id).reshape([batch_size, 1])
                sampling_end_time = time.perf_counter()
                sampling_times.append(sampling_end_time - sampling_start_time)

                all_token_ids = torch.cat([all_token_ids, tokens_to_add], dim=-1)
                current_length += 1

                # Update inputs for next inference run
                inputs["input_ids"] = tokens_to_add
                inputs["attention_mask"] = torch.cat(
                    [inputs["attention_mask"], (~has_eos).to(torch.int64).reshape(batch_size, 1)], 1
                )
                if "position_ids" in inputs:
                    inputs["position_ids"] = torch.max(inputs["position_ids"], dim=1)[0].reshape(batch_size, 1) + 1

                # Set logits to zeros for next inference run and re-use memory buffer
                if outputs["logits"].shape[1] != 1:
                    outputs["logits"] = outputs["logits"][:, :1, :].contiguous()
                outputs["logits"].zero_()

                # Update KV caches for next inference run
                if args.engine == "pt":
                    # Update KV caches for PyTorch
                    inputs["past_key_values"] = outputs["past_key_values"]
                elif not args.use_buffer_share:
                    # Update KV caches for ONNX Runtime if buffer sharing is not used
                    for i in range(config.num_hidden_layers):
                        inputs[f"past_key_values.{i}.key"] = outputs[f"present.{i}.key"]
                        inputs[f"past_key_values.{i}.value"] = outputs[f"present.{i}.value"]

                    new_sequence_length = inputs["attention_mask"].shape[1]
                    for i in range(config.num_hidden_layers):
                        present_key = torch.zeros(
                            batch_size,
                            num_heads,
                            new_sequence_length,
                            head_size,
                            device=args.target_device,
                            dtype=args.torch_dtype,
                        )
                        present_value = torch.zeros(
                            batch_size,
                            num_heads,
                            new_sequence_length,
                            head_size,
                            device=args.target_device,
                            dtype=args.torch_dtype,
                        )
                        outputs.update(
                            {
                                f"present.{i}.key": present_key.contiguous(),
                                f"present.{i}.value": present_value.contiguous(),
                            }
                        )

            wall_clock_end_time = time.perf_counter()

            # Filter out any anomaly accelerator times (e.g. for `torch.compile`)
            accelerator_times.pop(0)  # Remove prompt processing time
            if args.anomaly_filtering:
                anomaly_threshold_factor = 10
                min_time_s = min(accelerator_times)
                orig_size = len(accelerator_times)
                accelerator_times = list(
                    filter(lambda acc_time: acc_time < anomaly_threshold_factor * min_time_s, accelerator_times)
                )
                new_size = len(accelerator_times)
                logger.info(
                    f"Filtered out {orig_size - new_size} anomaly accelerator times that are {anomaly_threshold_factor}x greater than {min_time_s * 1000} ms..."
                )

            #######################################################
            # Calculate sampling and first token generated metrics
            #######################################################

            # Calculate sampling metrics
            avg_sampling_latency_s = sum(sampling_times) / len(sampling_times)
            avg_sampling_latency_ms = avg_sampling_latency_s * 1000
            avg_sampling_thrpt = batch_size * (1 / avg_sampling_latency_s)
            logger.info(f"Average Latency of Sampling: {avg_sampling_latency_ms} ms")
            logger.info(f"Average Throughput of Sampling: {avg_sampling_thrpt} tps")

            # Calculate first token generated metrics
            first_token_latency_s = accelerator_times[0]
            first_token_latency_ms = first_token_latency_s * 1000
            first_token_thrpt = batch_size * (1 / first_token_latency_s)
            logger.info(f"Latency of First Token Generated: {first_token_latency_ms} ms")
            logger.info(f"Throughput of First Token Generated: {first_token_thrpt} tps")

            ####################################################
            # Calculate first `halfway` token generated metrics
            ####################################################

            halfway = args.generation_length // 2
            halfway_token_latency_s = sum(accelerator_times[:halfway]) / len(accelerator_times[:halfway])
            halfway_token_latency_ms = halfway_token_latency_s * 1000
            halfway_token_thrpt = batch_size * (1 / halfway_token_latency_s)
            logger.info(f"Average Latency of First {halfway} Tokens Generated: {halfway_token_latency_ms} ms")
            logger.info(f"Average Throughput of First {halfway} Tokens Generated: {halfway_token_thrpt} tps")

            #########################################
            # Calculate all tokens generated metrics
            #########################################

            all_token_latency_s = sum(accelerator_times) / len(accelerator_times)
            all_token_latency_ms = all_token_latency_s * 1000
            all_token_thrpt = batch_size * (1 / all_token_latency_s)
            logger.info(
                f"Average Latency of First {args.generation_length} Tokens Generated: {all_token_latency_ms} ms"
            )
            logger.info(f"Average Throughput of First {args.generation_length} Tokens Generated: {all_token_thrpt} tps")

            ###############################
            # Calculate wall clock metrics
            ###############################

            wall_clock_latency_s = wall_clock_end_time - wall_clock_start_time
            wall_clock_thrpt = batch_size * ((prompt_length + args.generation_length) / wall_clock_latency_s)
            logger.info(f"Wall-Clock Latency: {wall_clock_latency_s} s")
            logger.info(
                f"Wall-Clock Throughput: {batch_size * ((prompt_length + args.generation_length) / wall_clock_latency_s)} tps"
            )

            # Add metrics to CSV
            logger.info("Adding results to CSV")
            csv_metrics.extend(
                [
                    avg_sampling_latency_ms,
                    avg_sampling_thrpt,
                    first_token_latency_ms,
                    first_token_thrpt,
                    halfway_token_latency_ms,
                    halfway_token_thrpt,
                    all_token_latency_ms,
                    all_token_thrpt,
                    wall_clock_latency_s,
                    wall_clock_thrpt,
                ]
            )
            all_csv_metrics.append(csv_metrics)

        except Exception as e:
            logger.info(f"Could not benchmark at batch size = {batch_size}, prompt length = {prompt_length} - {e}")

    filename = f"benchmark_{args.engine}_e2e_{datetime.datetime.now():%Y-%m-%d_%H:%M:%S}.csv"
    save_results(all_csv_metrics, filename, args.generation_length)


def main():
    warnings.warn(
        "This example is deprecated. Use the Olive recipe instead: "
        "https://github.com/microsoft/olive-recipes/tree/main",
        DeprecationWarning,
        stacklevel=2,
    )
    if version.parse(torch.__version__) < version.parse("2.2.0"):
        logger.error(f"Detected PyTorch version {torch.__version__}. Please upgrade and use v2.2.0 or newer.")
        return

    args = get_args()
    setup_logger(args.verbose)
    prepare_environment(args.input, args.output, args.execution_provider != "cpu")
    if args.reexport:
        remove_existing_files(args.output)
    logger.info(f"Arguments: {args}")

    world_size = get_size()
    rank = get_rank()
    args.world_size = world_size

    # Load model and config
    use_auth_token = args.input == os.path.join(".")
    setattr(args, "use_auth_token", use_auth_token)  # noqa: B010

    original_model_name = args.model_name
    setattr(args, "original_model_name", original_model_name)  # noqa: B010
    args.model_name = args.model_name.split("/")[-1]

    setattr(args, "device_name", "cpu" if args.execution_provider == "cpu" else f"cuda:{rank}")  # noqa: B010
    setattr(args, "device", torch.device(args.device_name))  # noqa: B010

    location = args.original_model_name if use_auth_token else args.input

    if args.optimize_optimum:
        config = AutoConfig.from_pretrained(args.original_model_name, cache_dir=args.cache_dir)
        optimize_optimum(config, args)
        return

    # Use CUDA for LLaMA-2-70B to speed up export and CPU for other models
    l_config, llama = setup_torch_model(
        args, location, use_auth_token, device=args.device if args.model_name == "Llama-2-70b-hf" else None
    )

    assert l_config.num_attention_heads % world_size == 0 and l_config.num_key_value_heads % world_size == 0

    barrier()
    for i in range(world_size):
        if i == rank:
            # Set model paths for FP32 model
            decoder_model_fp32_path = os.path.join(
                args.output, f"rank_{rank}_{args.model_name}_decoder_model_fp32.onnx"
            )
            decoder_with_past_model_fp32_path = os.path.join(
                args.output, f"rank_{rank}_{args.model_name}_decoder_with_past_model_fp32.onnx"
            )
            decoder_merged_model_fp32_path = os.path.join(
                args.output, f"rank_{rank}_{args.model_name}_decoder_merged_model_fp32.onnx"
            )
            old_paths = [decoder_model_fp32_path, decoder_with_past_model_fp32_path, decoder_merged_model_fp32_path]

            missing_separate_exports = (
                args.no_merged
                and not os.path.exists(decoder_model_fp32_path)
                and not os.path.exists(decoder_with_past_model_fp32_path)
            )
            missing_merged_export = not args.no_merged and not os.path.exists(decoder_merged_model_fp32_path)

            # Export to ONNX
            if missing_separate_exports or missing_merged_export:
                if args.use_dynamo_export:
                    logger.warning("Please ensure you have installed PyTorch, ONNX, and ONNX Script as follows.")
                    logger.warning("Step 1 - PyTorch nightly: https://pytorch.org/get-started/locally/")
                    logger.warning("Step 2 - ONNX weekly: https://pypi.org/project/onnx-weekly/")
                    logger.warning(
                        "Step 3 - ONNX Script from source: https://github.com/microsoft/onnxscript#installing-onnx-script"
                    )
                    logger.warning(
                        "Note: After you install ONNX weekly, omit `onnx` when running the first line for installing ONNX Script. This is because you already installed `onnx-weekly` in the previous step."
                    )
                    run_dynamo_export(args, l_config, llama)
                elif args.no_merged:
                    run_torchscript_separate_export(args, l_config, llama, rank, world_size)
                else:
                    run_torchscript_merged_export(args, l_config, llama, rank, world_size)
            del llama  # Delete LLaMA model from memory since it will be loaded again during parity check

            # Set model paths to store FP32 optimized model
            decoder_model_fp32_opt_path = os.path.join(
                args.output, f"rank_{rank}_{args.model_name}_decoder_model_fp32_opt.onnx"
            )
            decoder_with_past_model_fp32_opt_path = os.path.join(
                args.output, f"rank_{rank}_{args.model_name}_decoder_with_past_model_fp32_opt.onnx"
            )
            decoder_merged_model_fp32_opt_path = os.path.join(
                args.output, f"rank_{rank}_{args.model_name}_decoder_merged_model_fp32_opt.onnx"
            )
            new_paths = [
                decoder_model_fp32_opt_path,
                decoder_with_past_model_fp32_opt_path,
                decoder_merged_model_fp32_opt_path,
            ]

            # Run the optimizer script.
            logger.info("Optimizing models...")
            for orig_path, opt_path in zip(old_paths, new_paths, strict=False):
                if os.path.exists(orig_path):
                    optimize_export(args, l_config, input_path=orig_path, output_path=opt_path, world_size=world_size)

            # Re-assign default FP32 model paths as their optimized versions
            decoder_model_fp32_path = decoder_model_fp32_opt_path
            decoder_with_past_model_fp32_path = decoder_with_past_model_fp32_opt_path
            decoder_merged_model_fp32_path = decoder_merged_model_fp32_opt_path
            old_paths = [decoder_model_fp32_path, decoder_with_past_model_fp32_path, decoder_merged_model_fp32_path]

            logger.info(
                f"The {args.model_name} ONNX model has been successfully optimized with the ORT transformer optimizer script!"
            )

            # Change precision of exported models from FP32
            if args.precision == Precision.FLOAT16:
                new_paths = convert_to_float16(args, old_paths, rank)

            elif args.precision == Precision.INT8:
                decoder_model_int8_path = os.path.join(
                    args.output, f"rank_{rank}_{args.model_name}_decoder_model_int8.onnx"
                )
                decoder_with_past_model_int8_path = os.path.join(
                    args.output, f"rank_{rank}_{args.model_name}_decoder_with_past_model_int8.onnx"
                )
                decoder_merged_model_int8_path = os.path.join(
                    args.output, f"rank_{rank}_{args.model_name}_decoder_merged_model_int8.onnx"
                )
                new_paths = [decoder_model_int8_path, decoder_with_past_model_int8_path, decoder_merged_model_int8_path]

                if args.quantization_method == "smooth_quant":
                    if not args.no_merged:
                        logger.error("SmoothQuant must be used on separately exported models")
                    else:
                        logger.info(
                            f"Quantizing {decoder_model_fp32_path} and {decoder_with_past_model_fp32_path} to int8"
                        )
                        smooth_quant(args, old_paths[0], old_paths[1], new_paths[0], new_paths[1])

                elif args.quantization_method == "quantize_dynamic":
                    logger.warning(
                        "The `quantize_dynamic` method is deprecated in favor of `smooth_quant` instead. Precision loss may be high with `quantize_dynamic`."
                    )

                    logger.info("Quantizing to int8...")
                    for fp32_path, int8_path in zip(old_paths, new_paths, strict=False):
                        if os.path.exists(fp32_path):
                            ort_quantization.quantize_dynamic(
                                fp32_path,
                                int8_path,
                                op_types_to_quantize=(
                                    ["MatMul", "Gemm", "Gather"]
                                    if args.quantize_embedding_layer
                                    else ["MatMul", "Gemm"]
                                ),
                                per_channel=args.quantize_per_channel,
                                reduce_range=args.quantize_reduce_range,
                                use_external_data_format=True,
                                extra_options={"MatMulConstBOnly": True},
                            )
                            logger.info(
                                f"The ONNX model at {fp32_path} has been quantized to int8 and saved at {int8_path}!"
                            )
                            remove_existing_model(decoder_model_fp32_path)

                    logger.info(f"The {args.model_name} ONNX model has been successfully quantized to int8!")

                else:
                    raise Exception(f"Could not recognize {args.quantization_method} as a quantization method")

            elif args.precision == Precision.INT4:
                if args.execution_provider != "cpu":
                    old_paths = convert_to_float16(args, old_paths, rank)

                decoder_model_int4_path = os.path.join(
                    args.output, f"rank_{rank}_{args.model_name}_decoder_model_int4.onnx"
                )
                decoder_with_past_model_int4_path = os.path.join(
                    args.output, f"rank_{rank}_{args.model_name}_decoder_with_past_model_int4.onnx"
                )
                decoder_merged_model_int4_path = os.path.join(
                    args.output, f"rank_{rank}_{args.model_name}_decoder_merged_model_int4.onnx"
                )
                new_paths = [decoder_model_int4_path, decoder_with_past_model_int4_path, decoder_merged_model_int4_path]

                for fp_path, int4_path in zip(old_paths, new_paths, strict=False):
                    if os.path.exists(fp_path):
                        model = onnx.load_model(fp_path, load_external_data=True)
                        quant = MatMulNBitsQuantizer(
                            model=model,
                            bits=args.bits,
                            block_size=args.block_size,
                            is_symmetric=True,
                            accuracy_level=args.int4_accuracy_level,
                            nodes_to_exclude=[],
                        )
                        quant.process()
                        quant.model.save_model_to_file(int4_path, use_external_data_format=True)
                        del model
                        del quant
                        logger.info(f"The ONNX model at {fp_path} has been quantized to int4 and saved at {int4_path}!")
                        remove_existing_model(fp_path)
        barrier()

    logger.info("Verifying parity on all ONNX models created")

    # Use FP32 precision for FP32, INT8, INT4 CPU models, use FP16 precision for FP16 and INT4 GPU models
    args.precision = (
        "fp32"
        if args.precision in {Precision.INT8, Precision.FLOAT32}
        or (args.precision == Precision.INT4 and args.execution_provider == "cpu")
        else "fp16"
    )

    # Verify parity on all saved ONNX models
    for filename in os.listdir(args.output):
        if (
            ".data" in filename
            or ".onnx" not in filename
            or args.precision not in filename
            or f"rank_{rank}" not in filename
        ):
            continue

        parity_cmd = [
            "-m",
            original_model_name,
            "-o",
            os.path.join(args.output, filename),
            "-ep",
            args.execution_provider,
            "--precision",
            args.precision,
            "--cache_dir",
            args.cache_dir,
            "--torch_model_directory",
            args.input,
        ]
        if args.small_gpu:
            parity_cmd.append("--small_gpu")
        if "with_past" in filename:
            parity_cmd.append("--use_past_kv")
        if "merged" in filename:
            parity_cmd.append("--merged")

        try:
            logger.info(f"check parity with cmd: {parity_cmd}")
            parity_check(parity_cmd)
        except Exception as e:
            logger.exception(f"An error occurred while verifying parity: {e}")
            sys.exit(-1)


def main(argv: list[str] = []):  # noqa: B006
    args = get_args(argv)
    setup_logger(args.verbose)
    logger.info(f"Arguments: {args}")
    rank = get_rank()

    # Load model and config
    setattr(args, "use_fp16", args.precision == "fp16")  # noqa: B010
    args.rank = rank
    setattr(args, "device_name", "cpu" if args.execution_provider == "cpu" else f"cuda:{rank}")  # noqa: B010
    setattr(args, "device", torch.device(args.device_name))  # noqa: B010
    use_auth_token = args.torch_model_directory == os.path.join(".")
    location = args.model_name if use_auth_token else args.torch_model_directory

    kv_cache_ortvalues = {}
    if not args.merged:
        verify_parity(args, location, use_auth_token, kv_cache_ortvalues)
    else:
        config = llama = None
        if not args.small_gpu:
            config, llama = setup_torch_model(
                args,
                location,
                use_auth_token,
                torch_dtype=(torch.float16 if args.use_fp16 else torch.float32),
                device=args.device,
            )

        # Verify prompt processing in merged model (decoder_model.onnx)
        args.use_past_kv = False
        kv_cache_ortvalues = verify_parity(
            args, location, use_auth_token, kv_cache_ortvalues, pytorch_model=llama, config=config
        )

        # Verify token generation in merged model (decoder_with_past_model.onnx)
        args.use_past_kv = True
        verify_parity(args, location, use_auth_token, kv_cache_ortvalues, pytorch_model=llama, config=config)


def main():
    torch.multiprocessing.set_start_method("spawn")

    args = parse_arguments()

    benchmark_helper.setup_logger(args.verbose)

    if len(sys.argv) > 1:
        test_results = launch_test(args)
        time_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        csv_filename = f"benchmark_detail_{time_stamp}.csv"
        output_details(test_results, csv_filename)
        return

    gpu_list = benchmark_helper.get_gpu_info()
    logger.info("GPU info: %s", gpu_list)
    fp16_batch_sizes = [16, 8, 4, 2, 1]
    fp32_batch_sizes = [4, 2, 1]
    if gpu_list and gpu_list[0]["total"] >= 32 * 1024 * 1024 * 1024:  # 32 GB
        fp16_batch_sizes = [64, 32, 16, 8, 4, 2, 1]
        fp32_batch_sizes = [16, 8, 4, 2, 1]

    gpu_name = re.sub(r"(?u)[^-\w.]", "_", gpu_list[0]["name"]) if gpu_list else "gpu"
    is_baseline = os.environ.get("ORT_LONGFORMER_BASELINE", "0") == "1"
    experiment_name = f"longformer_base_{gpu_name}" + ("_baseline" if is_baseline else "")
    logger.info(
        f"experiment_name={experiment_name}, fp16_batch_sizes={fp16_batch_sizes}, fp32_batch_sizes={fp32_batch_sizes}"
    )

    total_runs = 1
    all_results = []
    for _ in range(total_runs):
        for batch_size in fp16_batch_sizes:
            fp16_results = run_experiments(use_fp16=True, batch_size=batch_size, is_baseline=is_baseline)
            output_details(fp16_results, "longformer_base_fp16.csv")
            all_results += fp16_results
    for metric_name in ["average_latency_ms", "QPS", "memory", "diff_90_percentile"]:
        output_summary(all_results, f"{experiment_name}_{metric_name}.csv", metric_name)

    all_results = []
    for _ in range(total_runs):
        for batch_size in fp32_batch_sizes:
            fp32_results = run_experiments(use_fp16=False, batch_size=batch_size, is_baseline=is_baseline)
            output_details(fp32_results, "longformer_base_fp32.csv")
            all_results += fp32_results
    for metric_name in ["average_latency_ms", "QPS", "memory", "diff_90_percentile"]:
        output_summary(all_results, f"{experiment_name}_{metric_name}.csv", metric_name)


def main(args):
    model_name = args.model
    onnx_model_path = model_name + ".onnx"

    global weight_bias_format  # noqa: PLW0603
    weight_bias_format = 0 if args.no_merge_qkv else 1

    model = LongformerModel.from_pretrained(PRETRAINED_LONGFORMER_MODELS[model_name])

    export_longformer(model, onnx_model_path, args.export_padding)

    if args.optimize_onnx or args.precision != "fp32":
        fp32_model_path = model_name + f"_f{weight_bias_format}" + "_fp32.onnx"
        fp16_model_path = model_name + f"_f{weight_bias_format}" + "_fp16.onnx" if args.precision == "fp16" else None
        optimize_longformer(onnx_model_path, fp32_model_path, fp16_model_path)


def main():
    args = parse_arguments()

    output_dir = args.output_dir
    if output_dir is None:
        # Default output directory is a sub-directory under the directory of model.
        output_dir = os.path.join(
            Path(args.model).parent,
            f"b{args.batch_size}_s{args.sequence_length}_g{args.global_tokens}",
        )

    if output_dir is not None:
        # create the output directory if not existed
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
    else:
        print("Directory existed. test data files will be overwritten.")

    if args.average_sequence_length <= 0:
        args.average_sequence_length = args.sequence_length

    create_longformer_test_data(
        args.model,
        output_dir,
        args.batch_size,
        args.sequence_length,
        args.samples,
        args.seed,
        args.verbose,
        args.input_ids_name,
        args.input_mask_name,
        args.global_mask_name,
        args.global_tokens,
        args.average_sequence_length,
    )

    print("Test data is saved to directory:", output_dir)


def main():
    warnings.warn(
        "This example is deprecated. Use the Olive recipe instead: "
        "https://github.com/microsoft/olive-recipes/tree/main",
        DeprecationWarning,
        stacklevel=2,
    )
    args = parse_arguments()

    device = torch.device("cuda", args.device_id) if torch.cuda.is_available() else torch.device("cpu")

    converter = ConvertPhi2ToONNX(device, cache_dir=args.cache_dir)
    converter.set_quantization_params(args.block_size, args.int4_accuracy_level)

    output_dir = args.output_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    original_onnx_path = os.path.join(output_dir, "phi2_original.onnx")

    if not args.skip_export:
        if not os.path.exists(original_onnx_path) or args.overwrite:
            converter.dynamo_export(original_onnx_path)

    model_type_to_args = {
        "fp32_cpu": (
            AttentionOpType.MultiHeadAttention,
            Precision.FLOAT32,
            os.path.join(output_dir, "phi2_decoder_fp32_cpu.onnx"),
        ),
        "int4_cpu": (
            AttentionOpType.MultiHeadAttention,
            Precision.INT4,
            os.path.join(output_dir, "phi2_decoder_int4_cpu.onnx"),
        ),
        "fp32_gpu": (
            AttentionOpType.Attention,
            Precision.FLOAT32,
            os.path.join(output_dir, "phi2_decoder_fp32_gpu.onnx"),
        ),
        "fp16_gpu": (
            AttentionOpType.Attention,
            Precision.FLOAT16,
            os.path.join(output_dir, "phi2_decoder_fp16_gpu.onnx"),
        ),
        "int4_gpu": (AttentionOpType.Attention, Precision.INT4, os.path.join(output_dir, "phi2_decoder_int4_gpu.onnx")),
        "fp16_gpu_sm8x": (
            AttentionOpType.GroupQueryAttention,
            Precision.FLOAT16,
            os.path.join(output_dir, "phi2_decoder_fp16_gpu_sm8x.onnx"),
        ),
        "int4_gpu_sm8x": (
            AttentionOpType.GroupQueryAttention,
            Precision.INT4,
            os.path.join(output_dir, "phi2_decoder_int4_gpu_sm8x.onnx"),
        ),
        "fp16_vllm": (
            AttentionOpType.PagedAttention,
            Precision.FLOAT16,
            os.path.join(output_dir, "phi2_decoder_fp16_vllm.onnx"),
        ),
        "int4_vllm": (
            AttentionOpType.PagedAttention,
            Precision.INT4,
            os.path.join(output_dir, "phi2_decoder_int4_vllm.onnx"),
        ),
    }

    if not args.skip_export:
        from multiprocessing import Process  # noqa: PLC0415

        def run_optimize_phi2_onnx(
            converter: ConvertPhi2ToONNX,
            original_onnx_path: str,
            attention_type: AttentionOpType,
            precision: Precision,
            optimized_onnx_path: str,
        ):
            converter.init_attn_type_and_precision(attention_type, precision)
            converter.optimize_phi2_onnx(original_onnx_path, optimized_onnx_path)
            if args.use_cuda_graph:
                assert args.fp16_gpu_sm8x or args.int4_gpu_sm8x
                converter.convert_to_use_cuda_graph(optimized_onnx_path, optimized_onnx_path)

        processes = []
        if args.fp32_cpu:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx, args=(converter, original_onnx_path, *model_type_to_args["fp32_cpu"])
                )
            )

        if args.int4_cpu:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx, args=(converter, original_onnx_path, *model_type_to_args["int4_cpu"])
                )
            )

        if args.fp32_gpu:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx, args=(converter, original_onnx_path, *model_type_to_args["fp32_gpu"])
                )
            )

        if args.fp16_gpu:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx, args=(converter, original_onnx_path, *model_type_to_args["fp16_gpu"])
                )
            )

        if args.int4_gpu:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx, args=(converter, original_onnx_path, *model_type_to_args["int4_gpu"])
                )
            )

        if args.fp16_gpu_sm8x:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx,
                    args=(converter, original_onnx_path, *model_type_to_args["fp16_gpu_sm8x"]),
                )
            )

        if args.int4_gpu_sm8x:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx,
                    args=(converter, original_onnx_path, *model_type_to_args["int4_gpu_sm8x"]),
                )
            )

        if args.fp16_vllm:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx,
                    args=(converter, original_onnx_path, *model_type_to_args["fp16_vllm"]),
                )
            )

        if args.int4_vllm:
            processes.append(
                Process(
                    target=run_optimize_phi2_onnx,
                    args=(converter, original_onnx_path, *model_type_to_args["int4_vllm"]),
                )
            )

        [p.start() for p in processes]
        [p.join() for p in processes]

    if args.run_example or args.run_benchmark:
        from inference_example import run_phi2  # noqa: PLC0415

        if args.fp16_gpu_sm8x:
            logging.info("Running fp16_gpu_sm8x example...")
            run_phi2(
                onnx_model_path=model_type_to_args["fp16_gpu_sm8x"][2],
                use_buffer_share=True,
                device_id=args.device_id,
                use_step=True,
                use_cuda_graph=args.use_cuda_graph,
                run_benchmark=args.run_benchmark,
            )
        if args.int4_gpu_sm8x:
            logging.info("Running int4_gpu_sm8x example...")
            run_phi2(
                onnx_model_path=model_type_to_args["int4_gpu_sm8x"][2],
                use_buffer_share=True,
                device_id=args.device_id,
                use_step=True,
                use_cuda_graph=args.use_cuda_graph,
                run_benchmark=args.run_benchmark,
            )
        if args.fp32_gpu:
            logging.info("Running fp32_gpu example...")
            run_phi2(
                onnx_model_path=model_type_to_args["fp32_gpu"][2],
                use_buffer_share=False,
                device_id=args.device_id,
                packed_kv=True,
                use_fp16=False,
                run_benchmark=args.run_benchmark,
            )
        if args.fp16_gpu:
            logging.info("Running fp16_gpu example...")
            run_phi2(
                onnx_model_path=model_type_to_args["fp16_gpu"][2],
                use_buffer_share=False,
                device_id=args.device_id,
                packed_kv=True,
                run_benchmark=args.run_benchmark,
            )
        if args.int4_gpu:
            logging.info("Running int4_gpu example...")
            run_phi2(
                onnx_model_path=model_type_to_args["int4_gpu"][2],
                use_buffer_share=False,
                device_id=args.device_id,
                packed_kv=True,
                run_benchmark=args.run_benchmark,
            )
        if args.fp32_cpu or args.int4_cpu or args.fp16_vllm or args.int4_vllm:
            raise NotImplementedError("CPU/vllm inference example is not implemented yet.")


def main():
    args = parse_arguments()

    sam2_model = load_sam2_model(args.sam2_dir, args.model_type, device="cpu")

    pathlib.Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    for component in args.components:
        onnx_model_path = sam2_onnx_path(args.output_dir, args.model_type, component, args.multimask_output)
        if component == "image_encoder":
            if args.overwrite or not os.path.exists(onnx_model_path):
                export_image_encoder_onnx(
                    sam2_model, onnx_model_path, args.dynamic_batch_axes, args.verbose, args.dynamo
                )
                test_image_encoder_onnx(sam2_model, onnx_model_path, dynamic_batch_axes=args.dynamic_batch_axes)

        elif component == "mask_decoder":
            if args.overwrite or not os.path.exists(onnx_model_path):
                export_mask_decoder_onnx(
                    sam2_model,
                    onnx_model_path,
                    args.multimask_output,
                    not args.disable_dynamic_multimask_via_stability,
                    args.verbose,
                )
                test_mask_decoder_onnx(
                    sam2_model,
                    onnx_model_path,
                    args.multimask_output,
                    not args.disable_dynamic_multimask_via_stability,
                )
        elif component == "prompt_encoder":
            if args.overwrite or not os.path.exists(onnx_model_path):
                export_prompt_encoder_onnx(sam2_model, onnx_model_path)
                test_prompt_encoder_onnx(sam2_model, onnx_model_path)
        else:
            assert component == "image_decoder"
            if args.overwrite or not os.path.exists(onnx_model_path):
                export_decoder_onnx(sam2_model, onnx_model_path, args.multimask_output)
                test_decoder_onnx(sam2_model, onnx_model_path, args.multimask_output)

    suffix = ""
    convert_to_fp16 = args.dtype == "fp16"
    if args.optimize:
        suffix = f"_{args.dtype}_" + ("gpu" if args.use_gpu else "cpu")
        for component in args.components:
            onnx_model_path = sam2_onnx_path(args.output_dir, args.model_type, component, args.multimask_output)
            optimized_model_path = sam2_onnx_path(
                args.output_dir, args.model_type, component, args.multimask_output, suffix
            )
            optimize_sam2_model(onnx_model_path, optimized_model_path, convert_to_fp16, args.use_gpu)

    if args.demo:
        # Export required ONNX models for demo if not already exported.
        image_encoder_onnx_path = sam2_onnx_path(
            args.output_dir, args.model_type, "image_encoder", args.multimask_output
        )
        if not os.path.exists(image_encoder_onnx_path):
            export_image_encoder_onnx(sam2_model, image_encoder_onnx_path, args.dynamic_batch_axes, args.verbose)

        image_decoder_onnx_path = sam2_onnx_path(args.output_dir, args.model_type, "image_decoder", False)
        if not os.path.exists(image_decoder_onnx_path):
            export_decoder_onnx(sam2_model, image_decoder_onnx_path, False)

        image_decoder_multi_onnx_path = sam2_onnx_path(args.output_dir, args.model_type, "image_decoder", True)
        if not os.path.exists(image_decoder_multi_onnx_path):
            export_decoder_onnx(sam2_model, image_decoder_multi_onnx_path, True)

        dtype = torch.float32 if args.dtype == "fp32" else torch.float16
        if suffix:
            optimized_image_encoder_onnx_path = image_encoder_onnx_path.replace(".onnx", f"{suffix}.onnx")
            if not os.path.exists(optimized_image_encoder_onnx_path):
                optimize_sam2_model(
                    image_encoder_onnx_path, optimized_image_encoder_onnx_path, convert_to_fp16, args.use_gpu
                )

            optimized_image_decoder_onnx_path = image_decoder_onnx_path.replace(".onnx", f"{suffix}.onnx")
            if not os.path.exists(optimized_image_decoder_onnx_path):
                optimize_sam2_model(
                    image_decoder_onnx_path, optimized_image_decoder_onnx_path, convert_to_fp16, args.use_gpu
                )

            optimized_image_decoder_multi_onnx_path = image_decoder_multi_onnx_path.replace(".onnx", f"{suffix}.onnx")
            if not os.path.exists(optimized_image_decoder_multi_onnx_path):
                optimize_sam2_model(
                    image_decoder_multi_onnx_path,
                    optimized_image_decoder_multi_onnx_path,
                    convert_to_fp16,
                    args.use_gpu,
                )

            # Use optimized models to run demo.
            image_encoder_onnx_path = optimized_image_encoder_onnx_path
            image_decoder_onnx_path = optimized_image_decoder_onnx_path
            image_decoder_multi_onnx_path = optimized_image_decoder_multi_onnx_path

        ort_image_files = run_demo(
            args.sam2_dir,
            args.model_type,
            engine="ort",
            dtype=dtype,
            image_encoder_onnx_path=image_encoder_onnx_path,
            image_decoder_onnx_path=image_decoder_onnx_path,
            image_decoder_multi_onnx_path=image_decoder_multi_onnx_path,
            use_gpu=args.use_gpu,
        )
        print("demo output files for ONNX Runtime:", ort_image_files)

        # Get results from torch engine to compare.
        torch_image_files = run_demo(args.sam2_dir, args.model_type, engine="torch", dtype=dtype, use_gpu=args.use_gpu)
        print("demo output files for PyTorch:", torch_image_files)

        show_all_images(ort_image_files, torch_image_files, suffix)
        print(f"Combined demo output: sam2_demo{suffix}.png")


def main():
    args = parse_arguments()
    print(args)

    if args.engine == "onnxruntime":
        if args.version in ["2.1"]:
            # Set a flag to avoid overflow in attention, which causes black image output in SD 2.1 model.
            # The environment variables shall be set before the first run of Attention or MultiHeadAttention operator.
            os.environ["ORT_DISABLE_TRT_FLASH_ATTENTION"] = "1"

        from packaging import version  # noqa: PLC0415

        from onnxruntime import __version__ as ort_version  # noqa: PLC0415

        if version.parse(ort_version) == version.parse("1.16.0"):
            # ORT 1.16 has a bug that might trigger Attention RuntimeError when latest fusion script is applied on clip model.
            # The walkaround is to enable fused causal attention, or disable Attention fusion for clip model.
            os.environ["ORT_ENABLE_FUSED_CAUSAL_ATTENTION"] = "1"

        if args.enable_cuda_graph:
            if not (args.engine == "onnxruntime" and args.provider in ["cuda", "tensorrt"] and args.pipeline is None):
                raise ValueError("The stable diffusion pipeline does not support CUDA graph.")

            if version.parse(ort_version) < version.parse("1.16"):
                raise ValueError("CUDA graph requires ONNX Runtime 1.16 or later")

    logging.basicConfig(format="%(funcName)20s: %(message)s", level=logging.INFO, force=True)

    memory_monitor_type = "cuda"

    start_memory = measure_gpu_memory(memory_monitor_type, None)
    print("GPU memory used before loading models:", start_memory)

    sd_model = SD_MODELS[args.version]
    provider = PROVIDERS[args.provider]
    if args.engine == "onnxruntime" and args.provider == "tensorrt":
        if "xl" in args.version:
            print("Testing Txt2ImgXLPipeline with static input shape. Backend is ORT TensorRT EP.")
            result = run_ort_trt_xl(
                work_dir=args.work_dir,
                version=args.version,
                batch_size=args.batch_size,
                disable_safety_checker=True,
                height=args.height,
                width=args.width,
                steps=args.steps,
                num_prompts=args.num_prompts,
                batch_count=args.batch_count,
                start_memory=start_memory,
                memory_monitor_type=memory_monitor_type,
                max_batch_size=args.max_trt_batch_size,
                nvtx_profile=False,
                use_cuda_graph=args.enable_cuda_graph,
                skip_warmup=args.skip_warmup,
            )
        else:
            print("Testing Txt2ImgPipeline with static input shape. Backend is ORT TensorRT EP.")
            result = run_ort_trt_static(
                work_dir=args.work_dir,
                version=args.version,
                batch_size=args.batch_size,
                disable_safety_checker=not args.enable_safety_checker,
                height=args.height,
                width=args.width,
                steps=args.steps,
                num_prompts=args.num_prompts,
                batch_count=args.batch_count,
                start_memory=start_memory,
                memory_monitor_type=memory_monitor_type,
                max_batch_size=args.max_trt_batch_size,
                nvtx_profile=False,
                use_cuda_graph=args.enable_cuda_graph,
                skip_warmup=args.skip_warmup,
            )
    elif args.engine == "optimum" and provider == "CUDAExecutionProvider":
        if "xl" in args.version:
            os.environ["ORT_ENABLE_FUSED_CAUSAL_ATTENTION"] = "1"

        result = run_optimum_ort(
            model_name=sd_model,
            directory=args.pipeline,
            provider=provider,
            batch_size=args.batch_size,
            disable_safety_checker=not args.enable_safety_checker,
            height=args.height,
            width=args.width,
            steps=args.steps,
            num_prompts=args.num_prompts,
            batch_count=args.batch_count,
            start_memory=start_memory,
            memory_monitor_type=memory_monitor_type,
            use_io_binding=args.use_io_binding,
            skip_warmup=args.skip_warmup,
        )
    elif args.engine == "onnxruntime":
        assert args.pipeline and os.path.isdir(args.pipeline), (
            "--pipeline should be specified for the directory of ONNX models"
        )
        print(f"Testing diffusers StableDiffusionPipeline with {provider} provider and tuning={args.tuning}")
        result = run_ort(
            model_name=sd_model,
            directory=args.pipeline,
            provider=provider,
            batch_size=args.batch_size,
            disable_safety_checker=not args.enable_safety_checker,
            height=args.height,
            width=args.width,
            steps=args.steps,
            num_prompts=args.num_prompts,
            batch_count=args.batch_count,
            start_memory=start_memory,
            memory_monitor_type=memory_monitor_type,
            tuning=args.tuning,
            skip_warmup=args.skip_warmup,
        )
    elif args.engine == "tensorrt" and "xl" in args.version:
        print("Testing Txt2ImgXLPipeline with static input shape. Backend is TensorRT.")
        result = run_tensorrt_static_xl(
            work_dir=args.work_dir,
            version=args.version,
            batch_size=args.batch_size,
            disable_safety_checker=True,
            height=args.height,
            width=args.width,
            steps=args.steps,
            num_prompts=args.num_prompts,
            batch_count=args.batch_count,
            start_memory=start_memory,
            memory_monitor_type=memory_monitor_type,
            max_batch_size=args.max_trt_batch_size,
            nvtx_profile=False,
            use_cuda_graph=args.enable_cuda_graph,
            skip_warmup=args.skip_warmup,
        )
    elif args.engine == "tensorrt":
        print("Testing Txt2ImgPipeline with static input shape. Backend is TensorRT.")
        result = run_tensorrt_static(
            work_dir=args.work_dir,
            version=args.version,
            model_name=sd_model,
            batch_size=args.batch_size,
            disable_safety_checker=True,
            height=args.height,
            width=args.width,
            steps=args.steps,
            num_prompts=args.num_prompts,
            batch_count=args.batch_count,
            start_memory=start_memory,
            memory_monitor_type=memory_monitor_type,
            max_batch_size=args.max_trt_batch_size,
            nvtx_profile=False,
            use_cuda_graph=args.enable_cuda_graph,
            skip_warmup=args.skip_warmup,
        )
    else:
        print(
            f"Testing Txt2ImgPipeline with dynamic input shape. Backend is PyTorch: compile={args.enable_torch_compile}, xformers={args.use_xformers}."
        )
        result = run_torch(
            model_name=sd_model,
            batch_size=args.batch_size,
            disable_safety_checker=not args.enable_safety_checker,
            enable_torch_compile=args.enable_torch_compile,
            use_xformers=args.use_xformers,
            height=args.height,
            width=args.width,
            steps=args.steps,
            num_prompts=args.num_prompts,
            batch_count=args.batch_count,
            start_memory=start_memory,
            memory_monitor_type=memory_monitor_type,
            skip_warmup=args.skip_warmup,
        )

    print(result)

    with open("benchmark_result.csv", mode="a", newline="") as csv_file:
        column_names = [
            "model_name",
            "directory",
            "engine",
            "version",
            "provider",
            "disable_safety_checker",
            "height",
            "width",
            "steps",
            "batch_size",
            "batch_count",
            "num_prompts",
            "average_latency",
            "median_latency",
            "first_run_memory_MB",
            "second_run_memory_MB",
            "enable_cuda_graph",
        ]
        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        csv_writer.writeheader()
        csv_writer.writerow(result)

    # Show loaded DLLs when steps == 1 for debugging purpose.
    if args.steps == 1:
        print_loaded_libraries(args.provider in ["cuda", "tensorrt"])


def main():
    args = arguments()

    with torch.no_grad():
        if args.engine == "ort_cuda":
            pipeline = load_ort_cuda_pipeline(
                args.name,
                args.engine,
                use_control_net=args.use_control_net,
                enable_cuda_graph=args.enable_cuda_graph,
                work_dir=args.work_dir,
            )
        else:
            pipeline = load_pipeline(
                args.name,
                args.engine,
                use_control_net=args.use_control_net,
                use_nhwc=args.use_nhwc,
                enable_cuda_graph=args.enable_cuda_graph,
            )

        canny_image = get_canny_image()

        if args.engine == "ort_cuda":
            images, latency_list = test_ort_cuda(
                pipeline,
                args.batch_size,
                args.steps,
                control_image=canny_image,
                warmup_runs=args.warmup_runs,
                verbose=args.verbose,
            )
        elif args.engine == "stable_fast":
            from sfast.utils.compute_precision import low_compute_precision  # noqa: PLC0415

            with low_compute_precision():
                images, latency_list = test(
                    pipeline,
                    args.batch_size,
                    args.steps,
                    control_image=canny_image,
                    warmup_runs=args.warmup_runs,
                    verbose=args.verbose,
                )
        else:
            images, latency_list = test(
                pipeline,
                args.batch_size,
                args.steps,
                control_image=canny_image,
                warmup_runs=args.warmup_runs,
                verbose=args.verbose,
            )

        # Save the first output image to inspect the result.
        if images:
            images[0].save(
                f"{args.engine}_{args.name.replace('/', '_')}_{args.batch_size}_{args.steps}_c{int(args.use_control_net)}.png"
            )

        result = {
            "engine": args.engine,
            "batch_size": args.batch_size,
            "steps": args.steps,
            "control_net": args.use_control_net,
            "nhwc": args.use_nhwc,
            "enable_cuda_graph": args.enable_cuda_graph,
            "average_latency_in_ms": mean(latency_list) * 1000,
        }
        print(result)


def main(args):
    controlnet_images, controlnet_scale = process_controlnet_arguments(args)

    pipeline, refiner = load_pipelines(args)
    assert refiner is None

    prompt, negative_prompt = repeat_prompt(args)
    batch_size = len(prompt)
    pipeline.load_resources(args.height, args.width, batch_size)

    def run_inference(warmup=False):
        return pipeline.run(
            prompt,
            negative_prompt,
            args.height,
            args.width,
            denoising_steps=args.denoising_steps,
            guidance=args.guidance,
            seed=args.seed,
            controlnet_images=controlnet_images,
            controlnet_scales=controlnet_scale,
            show_latency=not warmup,
            output_type="pil",
            deterministic=args.deterministic,
        )

    if not args.disable_cuda_graph:
        # inference once to get cuda graph
        _, _ = run_inference(warmup=True)

    print("[I] Warming up ..")
    for _ in range(args.num_warmup_runs):
        _, _ = run_inference(warmup=True)

    print("[I] Running StableDiffusion pipeline")
    if args.nvtx_profile:
        cudart.cudaProfilerStart()
    images, perf_data = run_inference(warmup=False)
    if args.nvtx_profile:
        cudart.cudaProfilerStop()

    metadata = get_metadata(args, False)
    metadata.update(pipeline.metadata())
    if perf_data:
        metadata.update(perf_data)
    metadata["images"] = len(images)
    print(metadata)
    pipeline.save_images(images, prompt, negative_prompt, metadata)

    pipeline.teardown()


def main(args):
    no_prompt = isinstance(args.prompt, list) and len(args.prompt) == 1 and not args.prompt[0]
    if no_prompt:
        if args.version == "xl-turbo":
            run_turbo_demo(args)
        else:
            run_dynamic_shape_demo(args)
    else:
        run_demo(args)


def main(argv: list[str] | None = None):
    warnings.warn(
        "This example is deprecated. Use the Olive recipe instead: "
        "https://github.com/microsoft/olive-recipes/tree/main",
        DeprecationWarning,
        stacklevel=2,
    )
    args = parse_arguments(argv)

    logger.info("Arguments: %s", str(args))

    # Return op counters for testing purpose.
    return optimize_stable_diffusion_pipeline(
        args.input, args.output, args.overwrite, args.use_external_data_format, args.float16, args.inspect, args
    )


def main():
    args = parse_arguments()

    setup_logger(args.verbose)

    logger.info(f"Arguments:{args}")

    cache_dir = args.cache_dir
    output_dir = args.output if not args.output.endswith(".onnx") else os.path.dirname(args.output)
    prepare_environment(cache_dir, output_dir, args.use_gpu)

    if args.precision != Precision.FLOAT32.value:
        assert args.optimize_onnx, "fp16/int8 requires --optimize_onnx"

    if args.precision == Precision.FLOAT16.value:
        assert args.use_gpu, "fp16 requires --use_gpu"

    output_paths = export_onnx_models(
        args.model_name_or_path,
        cache_dir,
        output_dir,
        args.use_gpu,
        args.use_external_data_format,
        args.optimize_onnx,
        args.precision,
        args.verbose,
        args.use_decoder_start_token,
        args.overwrite,
        args.disable_auto_mixed_precision,
        not args.use_int64_inputs,
        args.model_type,
        encoder_decoder_init=args.encoder_decoder_init,
        force_fp16_io=args.force_fp16_io,
    )

    logger.info(f"Done! Outputs: {output_paths}")


def main():
    args = parse_args()
    setup_logger(args.verbose)
    logger.info(args.__dict__)
    torch.backends.cudnn.benchmark = True

    config = WhisperConfig.from_pretrained(args.model_name)
    processor = WhisperProcessor.from_pretrained(args.model_name)
    target_device = f"cuda:{args.device_id}" if args.device != "cpu" else args.device
    use_fp16 = args.precision == "fp16" or (args.precision in {"int8", "int4"} and args.device != "cpu")

    setattr(args, "processor", processor)  # noqa: B010
    setattr(args, "target_device", target_device)  # noqa: B010
    setattr(args, "use_fp16", use_fp16)  # noqa: B010
    setattr(args, "has_audio_stream", False)  # noqa: B010
    setattr(args, "eos_token_id", config.eos_token_id)  # noqa: B010

    logger.info(f"Forced decoder prompt ids: {args.decoder_input_ids}")

    # Measure cost to transcribe audio
    model = get_model(args)
    if args.benchmark_type == "ort":
        # Check for optional inputs that could have been added during export
        ort_model_inputs = {model_input.name for model_input in model.get_inputs()}
        args.has_audio_stream = "audio_stream" in ort_model_inputs
        setattr(args, "has_decoder_input_ids", "decoder_input_ids" in ort_model_inputs)  # noqa: B010
        setattr(args, "has_logits_processor", "logits_processor" in ort_model_inputs)  # noqa: B010
        setattr(args, "has_temperature", "temperature" in ort_model_inputs)  # noqa: B010

        if args.decoder_input_ids == []:
            args.decoder_input_ids = [config.decoder_start_token_id]

    inputs = get_inputs(args)
    run_inference(args, inputs, model)


def main():
    args = get_args()
    setup_logger(args.verbose)
    logger.info(args.__dict__)
    torch.backends.cudnn.benchmark = True

    config = WhisperConfig.from_pretrained(args.model_name)
    processor = WhisperProcessor.from_pretrained(args.model_name)

    # Calculate forced decoder input ids
    hf_forced_decoder_ids = processor.get_decoder_prompt_ids(language=args.language, task=args.task)
    ort_forced_decoder_ids = [config.decoder_start_token_id] + [token_id[1] for token_id in hf_forced_decoder_ids]
    hf_decoder_input_ids_cmd = (
        ["--decoder-input-ids", str(hf_forced_decoder_ids)] if args.language and args.task else []
    )
    ort_decoder_input_ids_cmd = (
        ["--decoder-input-ids", str(ort_forced_decoder_ids)] if args.language and args.task else []
    )
    ort_tune_cmd = ["--tune"] if args.tune else []

    all_results = []
    for audio_file in os.listdir(args.audio_path):
        audio_path = os.path.join(args.audio_path, audio_file)
        try:
            duration = librosa.get_duration(path=audio_path)
        except Exception as e:
            duration = -1
            logger.warning(f"An error occurred while trying to calculate the audio duration: {e}", exc_info=True)
            logger.warning(
                f"If you get an error that says:\n\tsoundfile.LibsndfileError: Error opening '{audio_file}': File contains data in an unknown format.\nyou may not have installed `ffmpeg` in addition to installing `librosa`."
            )
        logger.info(f"Testing {audio_path}...")

        # Benchmark PyTorch without torch.compile
        if args.hf_pt_eager:
            benchmark_cmd = [  # noqa: RUF005
                "python",
                "-m",
                "models.whisper.benchmark",
                "--audio-path",
                audio_path,
                "--benchmark-type",
                "hf-pt-eager",
                "--model-name",
                args.model_name,
                "--precision",
                args.precision,
                "--device",
                args.device,
                "--device-id",
                str(args.device_id),
                "--warmup-runs",
                str(args.warmup_runs),
                "--num-runs",
                str(args.num_runs),
                "--log-folder",
                args.log_folder,
            ] + hf_decoder_input_ids_cmd
            logger.info("Benchmark PyTorch without torch.compile")
            results = benchmark(args, benchmark_cmd, "pytorch-eager", audio_file, duration)
            all_results.extend(results)

        # Benchmark PyTorch with torch.compile
        if args.hf_pt_compile:
            benchmark_cmd = [  # noqa: RUF005
                "python",
                "-m",
                "models.whisper.benchmark",
                "--audio-path",
                audio_path,
                "--benchmark-type",
                "hf-pt-compile",
                "--model-name",
                args.model_name,
                "--precision",
                args.precision,
                "--device",
                args.device,
                "--device-id",
                str(args.device_id),
                "--warmup-runs",
                str(args.warmup_runs),
                "--num-runs",
                str(args.num_runs),
                "--log-folder",
                args.log_folder,
            ] + hf_decoder_input_ids_cmd
            logger.info("Benchmark PyTorch with torch.compile")
            results = benchmark(args, benchmark_cmd, "pytorch-compile", audio_file, duration)
            all_results.extend(results)

        # Benchmark Optimum + ONNX Runtime
        if args.hf_ort_dir_path:
            benchmark_cmd = [  # noqa: RUF005
                "python",
                "-m",
                "models.whisper.benchmark",
                "--audio-path",
                audio_path,
                "--benchmark-type",
                "hf-ort",
                "--hf-ort-dir-path",
                args.hf_ort_dir_path,
                "--model-name",
                args.model_name,
                "--precision",
                args.precision,
                "--device",
                args.device,
                "--device-id",
                str(args.device_id),
                "--warmup-runs",
                str(args.warmup_runs),
                "--num-runs",
                str(args.num_runs),
                "--log-folder",
                args.log_folder,
            ] + hf_decoder_input_ids_cmd
            logger.info("Benchmark Optimum + ONNX Runtime")
            results = benchmark(args, benchmark_cmd, "optimum-ort", audio_file, duration)
            all_results.extend(results)

        # Benchmark ONNX Runtime
        if args.ort_model_path:
            benchmark_cmd = (
                [  # noqa: RUF005
                    "python",
                    "-m",
                    "models.whisper.benchmark",
                    "--audio-path",
                    audio_path,
                    "--benchmark-type",
                    "ort",
                    "--ort-model-path",
                    args.ort_model_path,
                    "--model-name",
                    args.model_name,
                    "--precision",
                    args.precision,
                    "--device",
                    args.device,
                    "--device-id",
                    str(args.device_id),
                    "--warmup-runs",
                    str(args.warmup_runs),
                    "--num-runs",
                    str(args.num_runs),
                    "--log-folder",
                    args.log_folder,
                ]
                + ort_decoder_input_ids_cmd
                + ort_tune_cmd
            )
            logger.info("Benchmark ONNX Runtime")
            results = benchmark(args, benchmark_cmd, "onnxruntime", audio_file, duration)
            all_results.extend(results)

    csv_file = f"{args.model_size}-{args.precision}_{datetime.datetime.now():%Y-%m-%d_%H:%M:%S}.csv"
    save_results(all_results, os.path.join(args.log_folder, csv_file))


def main(argv=None):
    warnings.warn(
        "This example is deprecated. Use the Olive recipe instead: "
        "https://github.com/microsoft/olive-recipes/tree/main",
        DeprecationWarning,
        stacklevel=2,
    )
    args = parse_arguments(argv)

    setup_logger(args.verbose)

    logger.info(f"Arguments:{args}")

    cache_dir = args.cache_dir
    output_dir = args.output if not args.output.endswith(".onnx") else os.path.dirname(args.output)
    prepare_environment(cache_dir, output_dir, args.use_gpu)

    if args.precision == Precision.FLOAT16:
        assert args.use_gpu, "fp16 requires --use_gpu"

    output_paths = export_onnx_models(
        args.model_name_or_path,
        args.model_impl,
        cache_dir,
        output_dir,
        args.use_gpu,
        args.use_external_data_format,
        args.optimize_onnx,
        args.precision,
        args.verbose,
        args.use_forced_decoder_ids,
        not args.separate_encoder_and_decoder_init,
        args.no_beam_search_op,
        args.use_decoder_masked_mha,
        args.output_cross_qk,
        args.overwrite,
        not args.use_int64_inputs,
        args.accuracy_level,
        args.quantize_symmetric,
        args.provider,
        args.quant_method,
    )

    max_diff = 0
    if not args.no_beam_search_op:
        logger.info("Chaining model ... :")
        args.beam_model_output_dir = WhisperHelper.get_onnx_path(
            output_dir,
            args.model_name_or_path,
            suffix="_beamsearch",
            new_folder=False,
        )
        for path in output_paths:
            if "encoder_decoder" in path or "encoder" in path:
                args.encoder_path = path
            elif "decoder" in path:
                args.decoder_path = path
        chain_model(args)
        output_paths.append(args.beam_model_output_dir)

        # Check chained model
        ort_session = create_onnxruntime_session(
            args.beam_model_output_dir,
            use_gpu=args.use_gpu,
            provider=args.provider,
        )
        device = torch.device("cuda" if args.use_gpu else "cpu")

        # Wrap parity check in try-except to allow export to continue in case this produces an error
        try:
            with torch.no_grad():
                # Verify batched decoding with prompts for OpenAI implementation
                if args.model_impl == "openai" and args.use_forced_decoder_ids:
                    max_diff = WhisperHelper.verify_onnx(
                        args.model_name_or_path, cache_dir, ort_session, device, batch_size=2, prompt_mode=True
                    )
                else:
                    max_diff = WhisperHelper.verify_onnx(args.model_name_or_path, cache_dir, ort_session, device)
            if max_diff > 1e-4:
                logger.warning("PyTorch and ONNX Runtime results are NOT close")
            else:
                logger.info("PyTorch and ONNX Runtime results are close")
        except Exception as e:
            logger.warning(
                f"An error occurred while trying to verify parity between PyTorch and ONNX Runtime: {e}", exc_info=True
            )

        # Remove extra ONNX models saved in output directory
        for _file in os.listdir(output_dir):
            if "_beamsearch" not in _file and "_jump_times" not in _file:
                path = os.path.join(output_dir, _file)
                os.remove(path)
                if path in output_paths:
                    output_paths.remove(path)

    else:
        # Create ancillary JSON files for ONNX Runtime GenAI and/or Hugging Face's Optimum
        WhisperHelper.save_processing(
            args.model_name_or_path,
            args.provider,
            args.separate_encoder_and_decoder_init,
            args.use_decoder_masked_mha,
            args.output_cross_qk,
            next(iter(filter(lambda path: "encoder" in path, output_paths))),
            next(iter(filter(lambda path: "decoder" in path, output_paths))),
            output_dir,
            cache_dir,
        )

    logger.info(f"Done! Outputs: {output_paths}")
    return max_diff


def main():
    parser = ArgumentParser(
        "Insert Cast, Transpose nodes into Onnx model to make it aligned with QNN generated context binary."
    )
    parser.add_argument("-m", "--onnx_model", help="Required. Path to Onnx model file.", required=True, type=str)
    parser.add_argument(
        "-q", "--qnn_json", help="Required. Path to Qnn converted model_net.json file.", required=True, type=str
    )
    args = parser.parse_args()

    # Parse Qnn model_net.json file to get the graph input output information
    qnn_input_output_tensor_dic = {}
    parse_qnn_json_file(args.qnn_json, qnn_input_output_tensor_dic)

    model = onnx.load(args.onnx_model)

    nodes_to_add = []
    # Tranch the tensor name change to update the consumer nodes
    graph_input_output_name_dic = {}
    for graph_input in model.graph.input:
        if graph_input.name in qnn_input_output_tensor_dic:
            input_name_fater_node_insert = graph_input.name
            qnn_input_tensor = qnn_input_output_tensor_dic[graph_input.name]
            # Insert Cast node if Onnx input and Qnn input has different data type
            if graph_input.type.tensor_type.elem_type != qnn_input_tensor.onnx_data_type:
                # Insert Cast node
                cast_input_name = input_name_fater_node_insert
                cast_output_name = cast_input_name + "_qnn_cast"
                input_cast_node = helper.make_node(
                    "Cast",
                    name=cast_output_name,
                    inputs=[cast_input_name],
                    outputs=[cast_output_name],
                    to=graph_input.type.tensor_type.elem_type,
                )
                # Change input data type to Qnn input data type
                graph_input.type.tensor_type.elem_type = qnn_input_tensor.onnx_data_type
                nodes_to_add.extend([input_cast_node])
                input_name_fater_node_insert = cast_output_name
                graph_input_output_name_dic[graph_input.name] = cast_output_name

            if not compare_onnx_shape_with_qnn_shape(graph_input.type.tensor_type.shape.dim, qnn_input_tensor.dim):
                # Add Transpose node (channel last to channel first)
                transpose_perm = gen_to_channel_first_perm(len(graph_input.type.tensor_type.shape.dim))
                transpose_input_name = input_name_fater_node_insert
                transpose_output_name = transpose_input_name + "_qnn_trans"
                input_transpose_node = helper.make_node(
                    "Transpose",
                    name=transpose_output_name,
                    inputs=[transpose_input_name],
                    outputs=[transpose_output_name],
                    perm=transpose_perm,
                )
                nodes_to_add.extend([input_transpose_node])
                graph_input_output_name_dic[graph_input.name] = transpose_output_name

                # Change input shape to Qnn input shape
                for i in range(len(graph_input.type.tensor_type.shape.dim)):
                    graph_input.type.tensor_type.shape.dim[i].dim_value = qnn_input_tensor.dim[i]
        else:
            raise AssertionError("Error: Onnx model input: " + graph_input.name + " not exist from QNN model input.")

    for graph_output in model.graph.output:
        if graph_output.name in qnn_input_output_tensor_dic:
            output_name_after_node_insert = graph_output.name
            # Insert Cast node if Onnx input and Qnn input has idfferent data type
            qnn_output_tensor = qnn_input_output_tensor_dic[graph_output.name]
            if graph_output.type.tensor_type.elem_type != qnn_output_tensor.onnx_data_type:
                # Insert Cast node
                cast_output_name = output_name_after_node_insert
                cast_input_name = cast_output_name + "_qnn_cast"
                output_cast_node = helper.make_node(
                    "Cast",
                    name=cast_input_name,
                    inputs=[cast_input_name],
                    outputs=[cast_output_name],
                    to=qnn_output_tensor.onnx_data_type,
                )
                # Change output data type to Onn output data type
                graph_output.type.tensor_type.elem_type = qnn_output_tensor.onnx_data_type
                nodes_to_add.extend([output_cast_node])
                output_name_after_node_insert = cast_input_name
                graph_input_output_name_dic[graph_output.name] = cast_input_name

            if not compare_onnx_shape_with_qnn_shape(graph_output.type.tensor_type.shape.dim, qnn_output_tensor.dim):
                # Add Transpose node (channel first to channel last)
                transpose_perm = gen_to_channel_last_perm(len(graph_output.type.tensor_type.shape.dim))
                transpose_output_name = output_name_after_node_insert
                transpose_input_name = transpose_output_name + "_qnn_trans"
                output_transpose_node = helper.make_node(
                    "Transpose",
                    name=transpose_input_name,
                    inputs=[transpose_input_name],
                    outputs=[transpose_output_name],
                    perm=transpose_perm,
                )
                nodes_to_add.extend([output_transpose_node])
                graph_input_output_name_dic[graph_output.name] = transpose_input_name

                # Change output shape to Qnn output shape
                for i in range(len(graph_output.type.tensor_type.shape.dim)):
                    graph_output.type.tensor_type.shape.dim[i].dim_value = qnn_input_output_tensor_dic[
                        graph_output.name
                    ].dim[i]
        else:
            raise AssertionError("Error: Onnx model output: " + graph_output.name + " not exist from QNN model output.")

    for node in model.graph.node:
        for node_input_index, node_input in enumerate(node.input):
            # update consumer node for graph inputs to connect to inserted node
            if node_input in graph_input_output_name_dic:
                node.input[node_input_index] = graph_input_output_name_dic[node_input]

        for node_output_index, node_output in enumerate(node.output):
            # update producer node for graph outputs to connect to inserted node
            if node_output in graph_input_output_name_dic:
                node.output[node_output_index] = graph_input_output_name_dic[node_output]

    model.graph.node.extend(nodes_to_add)
    graph_topological_sort(model.graph)

    # Add extra parameter all_tensors_to_one_file=False, size_threshold=5000 if the model exceeds protobuf 2GB limit e.g below
    # onnx.save(model, args.onnx_model.replace(".onnx", "_add_trans.onnx"), all_tensors_to_one_file=False, size_threshold=5000)
    onnx.save(model, args.onnx_model.replace(".onnx", "_add_trans.onnx"))


def main():
    parser = ArgumentParser("Generate Onnx model which includes the QNN context binary.")
    parser.add_argument("-b", "--qnn_bin", help="Required. Path to Qnn context binary file.", required=True, type=str)
    parser.add_argument(
        "-q", "--qnn_json", help="Required. Path to Qnn converted model_net.json file.", required=True, type=str
    )
    parser.add_argument(
        "--disable_embed_mode",
        action="store_true",
        default=False,
        help="Set embed_mode=1 which mean embed Qnn context binary into the onnx model. Otherwise, set context binary file path in the onnx model",
    )
    parser.add_argument(
        "--quantized_IO",
        action="store_true",
        default=False,
        help="QNN converted context binary use quantized data as graph inputs and outputs. Will keep it if quantized_IO=True, otherwise, will insert Q and DQ nodes accordingly to make the graph inputs & outputs as float32 data type.",
    )
    args = parser.parse_args()

    # Parse Qnn model_net.json file to get the graph input output information

    with open(args.qnn_json) as qnn_json_file:
        qnn_json_obj = json.load(qnn_json_file)
        if "graph" in qnn_json_obj and "tensors" in qnn_json_obj["graph"]:
            print("This json file is from Qnn converter")
            qnn_input_tensor_dic = {}
            qnn_output_tensor_dic = {}
            parse_qnn_converter_json_file(qnn_json_obj, qnn_input_tensor_dic, qnn_output_tensor_dic)

            generate_wrapper_onnx_file(
                "QnnContext",
                args.qnn_json.replace(".json", "_qnn_ctx.onnx"),
                qnn_input_tensor_dic,
                qnn_output_tensor_dic,
                args.disable_embed_mode,
                args.qnn_bin,
                args.quantized_IO,
            )
        elif "info" in qnn_json_obj and "graphs" in qnn_json_obj["info"]:
            print("This json file is extracted from QNN context binary file")
            qnn_version = qnn_json_obj["info"]["buildId"]
            for qnn_graph in qnn_json_obj["info"]["graphs"]:
                qnn_input_tensor_dic = {}
                qnn_output_tensor_dic = {}
                graph_name = parse_qnn_graph(qnn_graph, qnn_input_tensor_dic, qnn_output_tensor_dic)

                ctx_file_name = graph_name + "_qnn_ctx.onnx"
                if not args.quantized_IO:
                    ctx_file_name = ctx_file_name.replace(".onnx", "_fp32_io.onnx")

                generate_wrapper_onnx_file(
                    graph_name,
                    ctx_file_name,
                    qnn_input_tensor_dic,
                    qnn_output_tensor_dic,
                    args.disable_embed_mode,
                    args.qnn_bin,
                    args.quantized_IO,
                    qnn_version,
                )
        else:
            print("json file unrecoginized.")


def main():
    if '-c' in sys.argv[1:]:
        run_compile()
    else:
        run_main(sys.argv[1:])


def main(argv: list[str]) -> None:
    # Set recursion limit and GC thresholds consistent with mypy/main.py
    sys.setrecursionlimit(RECURSION_LIMIT)
    if platform.python_implementation() == "CPython":
        gc.set_threshold(200 * 1000, 30, 30)

    args = parser.parse_args(argv)

    # This mimics how daemon receives the options. Note we need to postpone
    # processing error codes after plugins are loaded, because plugins can add
    # custom error codes.
    with open(args.options_data, "rb") as f:
        buf = ReadBuffer(f.read())
    options_dict = read_json(buf)
    disable_error_code = options_dict.pop("disable_error_code", [])
    enable_error_code = options_dict.pop("enable_error_code", [])
    options = Options().apply_changes(options_dict)

    status_file = args.status_file
    server = IPCServer(CONNECTION_NAME, WORKER_CONNECTION_TIMEOUT)

    try:
        with open(status_file, "w") as f:
            json.dump({"pid": os.getpid(), "connection_name": server.connection_name}, f)
            f.write("\n")
    except Exception as exc:
        print(f"Error writing status file {status_file}:", exc)
        raise

    fscache = FileSystemCache()
    fscache.set_package_root(options.package_root)
    cached_read = fscache.read
    error_formatter = None if options.output is None else OUTPUT_CHOICES.get(options.output)
    errors = Errors(
        options,
        read_source=lambda path: read_py_file(path, cached_read),
        error_formatter=error_formatter,
    )

    ctx = ServerContext(options, disable_error_code, enable_error_code, errors, fscache)
    try:
        with server:
            serve(server, ctx)
    except (OSError, IPCException) as exc:
        if options.verbosity >= 1:
            print("Error communicating with coordinator:", exc)
    except Exception as exc:
        report_internal_error(exc, errors.file, 0, errors, options)
    finally:
        server.cleanup()

    if options.fast_exit:
        # Exit fast if allowed, since coordinator is waiting on us.
        util.hard_exit(0)


def main(argv: list[str]) -> None:
    """The code is top-down."""
    check_python_version("dmypy")

    # set recursion limit consistent with mypy/main.py
    sys.setrecursionlimit(RECURSION_LIMIT)

    args = parser.parse_args(argv)
    if not args.action:
        parser.print_usage()
    else:
        try:
            args.action(args)
        except BadStatus as err:
            fail(err.args[0])
        except Exception:
            # We do this explicitly to avoid exceptions percolating up
            # through mypy.api invocations
            traceback.print_exc()
            sys.exit(2)


def main(_):
  print(_CONFIG.value)


def main(_):
  print(_CONFIG.value)


def main(_):
  print(_CONFIG.value)


def main(_):
  # Config is already loaded in FLAGS.my_config due to the logic hidden
  # in app.run().
  config = _CONFIG.value

  print_section('Printing config.')
  print(config)

  # Config is of our type ConfigDict.
  print('Type of the config {}'.format(type(config)))

  # By default it is locked, thus you cannot add new fields.
  # This prevents you from misspelling your attribute name.
  print_section('Locking.')
  print('config.is_locked={}'.format(config.is_locked))
  try:
    config.object.new_field = -3
  except AttributeError as e:
    print(e)

  # There is also "did you mean" feature!
  try:
    config.object.floet = -3.
  except AttributeError as e:
    print(e)

  # However if you want to modify it you can always unlock.
  print_section('Unlocking.')
  with config.unlocked():
    config.object.new_field = -3
    print('config.object.new_field={}'.format(config.object.new_field))

  # By default config is also type-safe, so you cannot change the type of any
  # field.
  print_section('Type safety.')
  try:
    config.float = 'jerry'
  except TypeError as e:
    print(e)
  config.float = -1.2
  print('config.float={}'.format(config.float))

  # NoneType is ignored by type safety and can both override and be overridden.
  config.float = None
  config.float = -1.2

  # You can temporarly turn type safety off.
  with config.ignore_type():
    config.float = 'tom'
    print('config.float={}'.format(config.float))
    config.float = 2.3
    print('config.float={}'.format(config.float))

  # You can use ConfigDict as a regular dict in many typical use-cases:
  # Iteration over fields:
  print_section('Iteration over fields.')
  for field in config:
    print('config has field "{}"'.format(field))

  # Checking if it contains a particular field using the "in" command.
  print_section('Checking for a particular field.')
  for field in ('float', 'non_existing'):
    if field in config:
      print('"{}" is in config'.format(field))
    else:
      print('"{}" is not in config'.format(field))

  # Using ** unrolling to pass the config to a function as named arguments.
  print_section('Unpacking with **')
  print(hello_function(**config))

  # You can even load a dictionary (notice it is not ConfigDict anymore) from
  # a yaml string representation of ConfigDict.
  # Note: __repr__ (not __str__) is the recommended representation, as it
  # preserves FieldReferences and placeholders.
  print_section('Loading dictionary from string representation.')
  dictionary = yaml.load(repr(config), yaml.UnsafeLoader)
  print('dict["object_reference"]["dict"]["dict"]["float"]={}'.format(
      dictionary['object_reference']['dict']['dict']['float']))


def main(_):
  cfg = config_dict.ConfigDict()
  cfg.float_field = 12.6
  cfg.integer_field = 123
  cfg.another_integer_field = 234
  cfg.nested = config_dict.ConfigDict()
  cfg.nested.string_field = 'tom'

  print(cfg.integer_field)  # Prints 123.
  print(cfg['integer_field'])  # Prints 123 as well.

  try:
    cfg.integer_field = 'tom'  # Raises TypeError as this field is an integer.
  except TypeError as e:
    print(e)

  cfg.float_field = 12  # Works: `int` types can be assigned to `float`.
  cfg.nested.string_field = u'bob'  # `String` fields can store Unicode strings.

  print(cfg)


def main(_):

  inner_dict = {'list': [1, 2], 'tuple': (1, 2, [3, 4], (5, 6))}
  example_dict = {
      'string': 'tom',
      'int': 2,
      'list': [1, 2],
      'set': {1, 2},
      'tuple': (1, 2),
      'ref': config_dict.FieldReference({'int': 0}),
      'inner_dict_1': inner_dict,
      'inner_dict_2': inner_dict
  }

  print_section('Initializing on dictionary.')
  # ConfigDict can be initialized on example_dict
  example_cd = config_dict.ConfigDict(example_dict)

  # Dictionary fields are also converted to ConfigDict
  print(type(example_cd.inner_dict_1))

  # And the reference structure is preserved
  print(id(example_cd.inner_dict_1) == id(example_cd.inner_dict_2))

  print_section('Initializing on ConfigDict.')

  # ConfigDict can also be initialized on a ConfigDict
  example_cd_cd = config_dict.ConfigDict(example_cd)

  # Yielding the same result:
  print(example_cd == example_cd_cd)

  # Note that the memory addresses are different
  print(id(example_cd) == id(example_cd_cd))

  # The memory addresses of the attributes are not the same because of the
  # FieldReference, which gets removed on the second initialization
  list_to_ids = lambda x: [id(element) for element in x]
  print(
      set(list_to_ids(list(example_cd.values()))) == set(
          list_to_ids(list(example_cd_cd.values()))))

  print_section('Initializing on self-referencing dictionary.')

  # Initialization works on a self-referencing dict
  self_ref_dict = copy.deepcopy(example_dict)
  self_ref_dict['self'] = self_ref_dict
  self_ref_cd = config_dict.ConfigDict(self_ref_dict)

  # And the reference structure is replicated
  print(id(self_ref_cd) == id(self_ref_cd.self))

  print_section('Unexpected initialization behavior.')

  # ConfigDict initialization doesn't look inside lists, so doesn't convert a
  # dict in a list to ConfigDict
  dict_in_list_in_dict = {'list': [{'troublemaker': 0}]}
  dict_in_list_in_dict_cd = config_dict.ConfigDict(dict_in_list_in_dict)
  print(type(dict_in_list_in_dict_cd.list[0]))

  # This can cause the reference structure to not be replicated
  referred_dict = {'key': 'value'}
  bad_reference = {'referred_dict': referred_dict, 'list': [referred_dict]}
  bad_reference_cd = config_dict.ConfigDict(bad_reference)
  print(id(bad_reference_cd.referred_dict) == id(bad_reference_cd.list[0]))


def main(_):
  cfg = config_dict.ConfigDict()
  cfg.integer_field = 123

  # Locking prohibits the addition and deletion of new fields but allows
  # modification of existing values. Locking happens automatically during
  # loading through flags.
  cfg.lock()
  try:
    cfg.intagar_field = 124  # Raises AttributeError and suggests valid field.
  except AttributeError as e:
    print(e)
  cfg.integer_field = -123  # Works fine.

  with cfg.unlocked():
    cfg.intagar_field = 1555  # Works fine too.

  print(cfg)


def main(_):
  placeholder = config_dict.FieldReference(0)
  cfg = config_dict.ConfigDict()
  cfg.placeholder = placeholder
  cfg.optional = config_dict.FieldReference(0, field_type=int)
  cfg.nested = config_dict.ConfigDict()
  cfg.nested.placeholder = placeholder

  try:
    cfg.optional = 'tom'  # Raises Type error as this field is an integer.
  except TypeError as e:
    print(e)

  cfg.optional = 1555  # Works fine.
  cfg.placeholder = 1  # Changes the value of both placeholder and
  # nested.placeholder fields.

  # Note that the indirection provided by FieldReferences will be lost if
  # accessed through a ConfigDict:
  placeholder = config_dict.FieldReference(0)
  cfg.field1 = placeholder
  cfg.field2 = placeholder  # This field will be tied to cfg.field1.
  cfg.field3 = cfg.field1  # This will just be an int field initialized to 0.

  print(cfg)


def main(argv=()):
  del argv  # Unused.
  lazy_computation()
  lazy_configdict()
  change_lazy_computation()
  create_cycle()
  lazy_configdict_advanced()


def main(_):
  print_section('Attribute Types.')
  cfg = config_dict.ConfigDict()
  cfg.int = 1
  cfg.list = [1, 2, 3]
  cfg.tuple = (1, 2, 3)
  cfg.set = {1, 2, 3}
  cfg.frozenset = frozenset({1, 2, 3})
  cfg.dict = {
      'nested_int': 4,
      'nested_list': [4, 5, 6],
      'nested_tuple': ([4], 5, 6),
  }

  print('Types of cfg fields:')
  print('list: ', type(cfg.list))  # List
  print('set: ', type(cfg.set))  # Set
  print('nested_list: ', type(cfg.dict.nested_list))  # List
  print('nested_tuple[0]: ', type(cfg.dict.nested_tuple[0]))  # List

  frozen_cfg = config_dict.FrozenConfigDict(cfg)
  print('\nTypes of FrozenConfigDict(cfg) fields:')
  print('list: ', type(frozen_cfg.list))  # Tuple
  print('set: ', type(frozen_cfg.set))  # Frozenset
  print('nested_list: ', type(frozen_cfg.dict.nested_list))  # Tuple
  print('nested_tuple[0]: ', type(frozen_cfg.dict.nested_tuple[0]))  # Tuple

  cfg_from_frozen = config_dict.ConfigDict(frozen_cfg)
  print('\nTypes of ConfigDict(FrozenConfigDict(cfg)) fields:')
  print('list: ', type(cfg_from_frozen.list))  # List
  print('set: ', type(cfg_from_frozen.set))  # Set
  print('nested_list: ', type(cfg_from_frozen.dict.nested_list))  # List
  print('nested_tuple[0]: ', type(cfg_from_frozen.dict.nested_tuple[0]))  # List

  print('\nCan use FrozenConfigDict.as_configdict() to convert to ConfigDict:')
  print(cfg_from_frozen == frozen_cfg.as_configdict())  # True

  print_section('Immutability.')
  try:
    frozen_cfg.new_field = 1  # Raises AttributeError because of immutability.
  except AttributeError as e:
    print(e)

  print_section('"==" and eq_as_configdict().')
  # FrozenConfigDict.__eq__() is not type-invariant with respect to ConfigDict
  print(frozen_cfg == cfg)  # False
  # FrozenConfigDict.eq_as_configdict() is type-invariant with respect to
  # ConfigDict
  print(frozen_cfg.eq_as_configdict(cfg))  # True
  # .eq_as_congfigdict() is also a method of ConfigDict
  print(cfg.eq_as_configdict(frozen_cfg))  # True


def main(args: Sequence[str] | None = None) -> int:
    namespace = parse_args(args)
    if namespace.filenames:
        convert(namespace.filenames)
    elif namespace.stdin:
        convert_stdin()
    else:
        interactive()
    return 0


def main():
    """Main entry point."""
    passed, total, failures = run_eval()

    # Exit with error code if too many failures
    pass_rate = passed / total
    if pass_rate < 0.80:
        print(f"\n❌ EVAL FAILED: Pass rate {pass_rate:.1%} is below 80% threshold")
        sys.exit(1)
    elif pass_rate < 0.90:
        print(f"\n⚠️  EVAL WARNING: Pass rate {pass_rate:.1%} is below 90%")
        sys.exit(0)
    else:
        print(f"\n✅ EVAL PASSED: Pass rate {pass_rate:.1%}")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Add audio to a Werewolf game replay.")
    parser.add_argument("-i", "--input_path", type=str, required=True, help="Path to replay JSON.")
    parser.add_argument("-o", "--output_dir", type=str, help="Output directory.")
    parser.add_argument("-c", "--config_path", type=str,
                        default=os.path.join(os.path.dirname(__file__), "configs/audio/standard.yaml"))
    parser.add_argument("--debug-audio", action="store_true", help="Generate debug audio only.")
    parser.add_argument("--serve", action="store_true", help="Start Vite server.")
    parser.add_argument("--voice", choices=["chirp", "gemini"], default="gemini",
                        help="Voice model to use (chirp/gemini)")
    parser.add_argument("--prompt_path", type=str,
                        default=os.path.join(os.path.dirname(__file__), "configs/audio/theatrical_prompt.txt"))
    parser.add_argument("--cache_path", type=str, help="LLM cache file path.")
    parser.add_argument("--enable_llm_enhancement", action="store_true",
                        help="Enable LLM enhancement (theatrical rewrites).")
    parser.add_argument("--disable_llm_enhancement", action="store_true",
                        help="Disable LLM enhancement (theatrical rewrites).")

    args = parser.parse_args()

    # Determine LLM status
    # Default to False if not specified, unless enable flag is set.
    # But wait, logic below says disable_llm = args.disable...
    # Let's keep existing logic structure but fixing the args for voice.

    disable_llm = args.disable_llm_enhancement
    if args.enable_llm_enhancement:
        disable_llm = False

    # Defaults
    if not args.output_dir:
        args.output_dir = "werewolf_replay_audio"
    if not args.cache_path:
        args.cache_path = os.path.join(args.output_dir, "llm_cache.json")

    os.makedirs(args.output_dir, exist_ok=True)
    setup_logger(output_dir=args.output_dir, base_name="add_audio")
    load_env_modules()

    # Config
    try:
        config = AudioConfig(args.config_path)
    except FileNotFoundError as e:
        logger.error(str(e))
        return

    # Replay
    if not os.path.exists(args.input_path):
        logger.error(f"Replay not found: {args.input_path}")
        return
    with open(args.input_path, "r", encoding="utf-8") as f:
        replay_data = json.load(f)

    # Components
    gemini_key = os.getenv("GEMINI_API_KEY")
    enhancer = LLMEnhancer(gemini_key, args.prompt_path, args.cache_path, not args.enable_llm_enhancement)

    if args.voice == "chirp":
        tts = VertexTTSGenerator(config.get_vertex_model(), regions=config.vertex_ai_regions)
    else:
        tts = GeminiTTSGenerator(gemini_key, regions=config.vertex_ai_regions)

    manager = AudioManager(config, enhancer, tts, args.output_dir)

    if args.debug_audio:
        manager.generate_debug_audio()
    else:
        manager.process_replay(replay_data)
        enhancer.save_cache()

    if args.serve:
        vis_dir = os.path.join(os.path.dirname(__file__), "../visualizer/default")
        audio_map_path = os.path.join(args.output_dir, "audio_map.json")
        VisualizerServer.start(vis_dir, args.input_path, audio_map_path)


def main():
    parser = argparse.ArgumentParser(description="Batch process audio generation and upload.")
    parser.add_argument("replay_dir", help="Directory containing .json replay files")
    parser.add_argument("--workers", type=int, default=2, help="Number of concurrent workers (Limited for display)")
    parser.add_argument("--keep-temp", action="store_true", help="Keep temporary audio files after upload")
    parser.add_argument("--log-file", type=str, default="batch_errors.log", help="Path to error log file")
    
    # Args expected by add_audio (defaults matching add_audio.py)
    parser.add_argument("-c", "--config_path", type=str,
                        default=os.path.join(script_dir, "configs/audio/standard.yaml"))
    parser.add_argument("--voice", type=str, default="gemini", choices=["chirp", "gemini"])
    parser.add_argument("--prompt_path", type=str,
                        default=os.path.join(script_dir, "configs/audio/theatrical_prompt.txt"))
    parser.add_argument("--cache_path", type=str, help="LLM cache file path.")
    parser.add_argument("--enable_llm_enhancement", action="store_true", help="Enable LLM enhancement (theatrical rewrites).")
    
    args = parser.parse_args()

    # Defaults
    if not args.cache_path:
        # We assume a shared cache for batch? Or per file?
        # Ideally shared cache if we want to save API calls across identical phrases (unlikely in different games).
        # Let's just use a default path in current dir.
        args.cache_path = "llm_cache.json"

    # Setup Logging
    logging.basicConfig(
        filename=args.log_file,
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w' # Overwrite log file on new run
    )
    logger = logging.getLogger()

    all_files = glob.glob(os.path.join(args.replay_dir, "*.json"))
    # Filter for numeric IDs only (e.g. 74222013.json) to avoid processing summaries or other artifacts
    replay_files = [
        f for f in all_files 
        if os.path.basename(f).replace(".json", "").isdigit()
    ]
    if not replay_files:
        print(f"No json files found in {args.replay_dir}")
        return

    # Configuration
    bucket_base = "gs://kaggle-static/episode-assets/werewolf/episodes"
    
    print(f"Found {len(replay_files)} replays.")
    print(f"Processing with {args.workers} workers...")
    
    # IMPORTANT: 50 workers with progress bars might exceed terminal height.
    # We warn the user if workers > 20.
    if args.workers > 20:
        print("WARNING: High worker count might cause visual glitches with progress bars.")

    success_count = 0
    errors = []

    # ThreadPool Executor
    # We assign a static position index to each worker?
    # No, workers pick up tasks. We need to assign a slot (0..workers-1) to each running task.
    # We can use a Semaphore-guarded list of available slots.
    
    slot_lock = threading.Lock()
    # Initialize in reverse so pop() gives 0, 1, 2...
    available_slots = list(range(args.workers - 1, -1, -1))
    
    def get_slot():
        with slot_lock:
            return available_slots.pop()
            
    def release_slot(s):
        with slot_lock:
            available_slots.append(s)

    def worker_wrapper(file_path):
        slot = get_slot()
        try:
            return process_single_episode_direct(
                file_path, bucket_base, args.config_path, 
                args.voice, args.prompt_path, args.cache_path, 
                args.enable_llm_enhancement, args.keep_temp, 
                position=slot
            )
        finally:
            release_slot(slot)

    # Main Progress Bar (Overall)
    # position=args.workers to place it below all worker bars?
    # Or position=0 and shift workers down?
    # Let's put overall at position=0.
    # Workers at 1..N.
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_file = {
            executor.submit(worker_wrapper, f): f 
            for f in replay_files
        }
        
        # position=0 is the main bar
        with tqdm(total=len(replay_files), desc="Total Progress", position=0, leave=True) as pbar:
            for future in as_completed(future_to_file):
                is_success, msg = future.result()
                if is_success:
                    success_count += 1
                else:
                    errors.append(msg)
                    logger.error(msg)
                    # We print errors to tqdm.write to avoid breaking layout, hopefully.
                    # tqdm.write(f"Error: {msg}") 
                    # If we use tqdm.write with many active bars, it might shift them. 
                    # Better to only log to file?
                    # User asked for error logs in file.
                pbar.update(1)

    print(f"\n\n\nCompleted. Success: {success_count}, Failed: {len(errors)}") # Newlines to clear bars
    
    if errors:
        print(f"\nErrors have been written to {args.log_file}")
        print("Check the log file for details.")


def main():
    parser = argparse.ArgumentParser(description="Measure LLM cost for the Werewolf game.")
    parser.add_argument(
        "-c",
        "--config_path",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "configs/run/comprehensive.yaml"),
        help="Path to the base YAML configuration file.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="cost_measurement",
        help="Output directory for logs, replays, and results.",
    )
    parser.add_argument(
        "-m",
        "--model_name",
        type=str,
        default=DEFAULT_MODEL,
        choices=LLM_MODEL_NAMES,
        help="LiteLLM model name to use for all agents.",
    )
    parser.add_argument("-d", "--disable_debug_mode", action="store_true", help="Disable debug mode.")

    args = parser.parse_args()

    # Create a unique subdirectory for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_output_dir = os.path.join(args.output_dir, f"run_{timestamp}")
    os.makedirs(run_output_dir, exist_ok=True)

    log_filename = f"measure_cost_{timestamp}"
    setup_logger(output_dir=run_output_dir, base_name=log_filename)
    logger.info(f"Starting cost measurement script. Results will be saved in: {run_output_dir}")

    # Load base game configuration
    with open(args.config_path, "r") as f:
        base_config = yaml.safe_load(f).get("game_config", {})

    max_turns_to_test = [8, 12, 16, 20, 24]
    runs_per_setting = 3
    results = {
        str(t): {"total_cost": [], "total_tokens": [], "total_prompt_tokens": [], "total_completion_tokens": []}
        for t in max_turns_to_test
    }
    all_trajectories = {
        "total_tokens": {str(t): [] for t in max_turns_to_test},
        "reasoning_tokens": {str(t): [] for t in max_turns_to_test},
        "text_tokens": {str(t): [] for t in max_turns_to_test},
    }

    for turns in max_turns_to_test:
        logger.info(f"--- Starting runs for max_turns = {turns} ---")
        for run in range(runs_per_setting):
            base_name = f"game_turns_{turns}_run_{run + 1}"
            logger.info(f"Starting {base_name}...")

            game_config, agent_harnesses = setup_game_config(turns, base_config, args.model_name)

            try:
                final_env = run_werewolf(
                    output_dir=run_output_dir,
                    base_name=base_name,
                    config=game_config,
                    agents=agent_harnesses,
                    debug=not args.disable_debug_mode,
                )

                # Extract cost summary
                cost_summary_dict = final_env.info.get("GAME_END", {}).get("cost_summary", {})
                if cost_summary_dict:
                    cost_summary = CostSummary(**cost_summary_dict)
                    results[str(turns)]["total_cost"].append(cost_summary.total_cost)
                    results[str(turns)]["total_tokens"].append(cost_summary.total_tokens)
                    results[str(turns)]["total_prompt_tokens"].append(cost_summary.total_prompt_tokens)
                    results[str(turns)]["total_completion_tokens"].append(cost_summary.total_completion_tokens)
                    logger.info(f"Finished {base_name}. Total Cost: ${cost_summary.total_cost:.4f}")

                    for agent_summary in cost_summary.cost_per_agent:
                        if agent_summary.data and agent_summary.data.usage_history:
                            usage_history_dicts = [usage.model_dump() for usage in agent_summary.data.usage_history]

                            total_tokens_traj = [usage.get("total_tokens", 0) or 0 for usage in usage_history_dicts]
                            all_trajectories["total_tokens"][str(turns)].append(total_tokens_traj)

                            reasoning_tokens_traj = [
                                usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0) or 0
                                for usage in usage_history_dicts
                            ]
                            all_trajectories["reasoning_tokens"][str(turns)].append(reasoning_tokens_traj)

                            text_tokens_traj = [
                                (u.get("completion_tokens", 0) or 0)
                                - (u.get("completion_tokens_details", {}).get("reasoning_tokens", 0) or 0)
                                for u in usage_history_dicts
                            ]
                            all_trajectories["text_tokens"][str(turns)].append(text_tokens_traj)
                else:
                    logger.error(f"Could not find cost summary for {base_name}.")

            except Exception as e:
                logger.error(f"An error occurred during {base_name}: {e}", exc_info=True)

    # Calculate mean and standard deviation
    summary_data = {}
    for turns, metrics in results.items():
        summary_data[turns] = {}
        for metric, values in metrics.items():
            if values:
                summary_data[turns][metric] = {"mean": np.mean(values), "std": np.std(values), "raw_values": values}
            else:
                summary_data[turns][metric] = {"mean": 0, "std": 0, "raw_values": []}

    # Save summary to JSON
    summary_filename = os.path.join(run_output_dir, "cost_analysis_summary.json")
    with open(summary_filename, "w") as f:
        json.dump(summary_data, f, indent=4)
    logger.info(f"Saved summary results to {summary_filename}")

    # Plot results
    plot_results(summary_data, run_output_dir)
    plot_token_trajectories(all_trajectories, run_output_dir)

    logger.info("--- Cost measurement script finished ---")


def main():
    parser = argparse.ArgumentParser(
        description="Load data from a measure_cost.py output directory and generate token trajectory plots."
    )
    parser.add_argument(
        "-i",
        "--input_dir",
        type=str,
        required=True,
        help="Path to the output directory of a previous measure_cost.py run.",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        logger.error(f"Input directory not found: {args.input_dir}")
        return

    logger.info(f"Loading data from: {args.input_dir}")

    all_trajectories = {"total_tokens": {}, "reasoning_tokens": {}, "text_tokens": {}}

    # Find all game replay JSON files
    game_files = glob.glob(os.path.join(args.input_dir, "game_*_run_*.json"))
    if not game_files:
        logger.error(f"No game replay files (game_*_run_*.json) found in {args.input_dir}.")
        return

    logger.info(f"Found {len(game_files)} game replay files to process.")

    for game_file in game_files:
        # Extract max_turns from filename
        match = re.search(r"game_turns_(\d+)_run_", os.path.basename(game_file))
        if not match:
            logger.warning(f"Could not parse max_turns from filename: {game_file}. Skipping.")
            continue
        turns = match.group(1)

        with open(game_file, "r") as f:
            game_data = json.load(f)

        cost_summary_dict = game_data.get("info", {}).get("GAME_END", {}).get("cost_summary")
        if not cost_summary_dict:
            logger.warning(f"No cost_summary found in {game_file}. Skipping.")
            continue

        cost_summary = CostSummary(**cost_summary_dict)

        for agent_summary in cost_summary.cost_per_agent:
            if agent_summary.data and agent_summary.data.usage_history:
                usage_history_dicts = [usage.model_dump() for usage in agent_summary.data.usage_history]

                total_tokens_traj = [usage.get("total_tokens", 0) or 0 for usage in usage_history_dicts]
                all_trajectories["total_tokens"].setdefault(turns, []).append(total_tokens_traj)

                reasoning_tokens_traj = [
                    usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0) or 0
                    for usage in usage_history_dicts
                ]
                all_trajectories["reasoning_tokens"].setdefault(turns, []).append(reasoning_tokens_traj)

                text_tokens_traj = [
                    (u.get("completion_tokens", 0) or 0)
                    - (u.get("completion_tokens_details", {}).get("reasoning_tokens", 0) or 0)
                    for u in usage_history_dicts
                ]
                all_trajectories["text_tokens"].setdefault(turns, []).append(text_tokens_traj)

    logger.info("Finished processing all files. Generating plots...")
    plot_token_trajectories(all_trajectories, args.input_dir)
    logger.info(f"--- Script finished. Plots saved in {args.input_dir} ---")


def main():
    """
    Rerenders a Werewolf game replay HTML file from an existing game record JSON.
    This is useful for updating the replay viewer to the latest version without
    rerunning the entire game simulation.
    """
    parser = argparse.ArgumentParser(
        description="Rerender a Werewolf game HTML replay from a JSON game record.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input_json",
        type=str,
        required=True,
        help="Path to the input game record JSON file (e.g., werewolf_game.json).",
    )
    parser.add_argument(
        "-o", "--output_html", type=str, required=True, help="Path to write the newly rendered HTML output file."
    )
    args = parser.parse_args()

    logging.info(f"Loading game record from: {args.input_json}")
    if not os.path.exists(args.input_json):
        logging.error(f"Error: Input file not found at {args.input_json}")
        return

    try:
        with open(args.input_json, "r", encoding="utf-8") as f:
            replay_data = json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Error: Failed to decode JSON from {args.input_json}. The file might be corrupted.")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the file: {e}")
        return

    logging.info("Successfully loaded game data. Initializing Kaggle environment...")

    # The environment name should be stored in the replay, but we default to 'werewolf'
    env_name = replay_data.get("name", "werewolf")
    if env_name != "werewolf":
        logging.warning(f"Game record is for '{env_name}', but we are rendering with the 'werewolf' environment.")

    try:
        # Recreate the environment state from the replay file
        env = make(
            "werewolf",
            configuration=replay_data.get("configuration"),
            steps=replay_data.get("steps", []),
            info=replay_data.get("info", {}),
        )
        logging.info("Environment initialized. Rendering new HTML...")

        # Render the HTML. This will use the werewolf.js file included in the
        # installed kaggle_environments package.
        html_content = env.render(mode="html")

        output_dir = os.path.dirname(args.output_html)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(args.output_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        logging.info(f"Successfully rerendered HTML to: {args.output_html}")

    except Exception as e:
        logging.error(f"An error occurred during environment creation or rendering: {e}")
        logging.error(
            "Please ensure the 'kaggle_environments' package is correctly installed and the JSON file is valid."
        )


def main():
    parser = argparse.ArgumentParser(description="Run a single Werewolf game.")
    parser.add_argument(
        "-c",
        "--config_path",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "configs/run/run_config.yaml"),
        help="Path to the YAML configuration file.",
    )
    parser.add_argument(
        "-o", "--output_dir", type=str, default="werewolf_run", help="Output directory for the log and replay file."
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument(
        "-r", "--random_agents", action="store_true", help="Use random agents for all players for fast testing."
    )
    parser.add_argument(
        "-a", "--append_timestamp_to_dir", action="store_true", help="Append a timestamp to the output directory."
    )
    parser.add_argument(
        "-s", "--shuffle_roles", action="store_true", help="If provided, shuffle the roles provided in the config."
    )

    args = parser.parse_args()

    # Create a unique subdirectory for this run
    run_output_dir = append_timestamp_to_dir(args.output_dir, append=args.append_timestamp_to_dir)

    os.makedirs(run_output_dir, exist_ok=True)

    base_name = "werewolf_game"
    setup_logger(output_dir=run_output_dir, base_name=base_name)

    log_git_hash()

    # Load game configuration
    with open(args.config_path, "r") as f:
        config = yaml.safe_load(f)
        game_config = config.get("game_config", {})

    # shuffle roles
    if args.shuffle_roles:
        role_and_params = [(agent["role"], agent.get("role_params", {})) for agent in game_config["agents"]]
        random.shuffle(role_and_params)
        for agent, (new_role, new_role_params) in zip(game_config["agents"], role_and_params):
            agent["role"] = new_role
            agent["role_params"] = new_role_params

    # Extract agent harnesses from the config and register the agents
    agents_ = [agent.get("agent_id", "random") for agent in game_config.get("agents", [])]
    agent_dict = {}
    for agent_name in agents_:
        if agent_name.startswith("llm/"):
            model_name = agent_name.lstrip("llm/")
            agent_dict[agent_name] = AgentFactoryWrapper(
                LLMWerewolfAgent, model_name=model_name, system_prompt=LLM_SYSTEM_PROMPT
            )
    register_agents(agent_dict)

    if args.random_agents:
        logger.info("Using random agents for all players.")
        agents_ = ["random"] * len(agents_)

    logger.info(f"Starting Werewolf game run. Output will be saved to: {run_output_dir}")
    with LogExecutionTime(logger_obj=logger, task_str="single game"):
        run_werewolf(
            output_dir=run_output_dir, base_name=base_name, config=game_config, agents=agents_, debug=args.debug
        )
    logger.info(f"Game finished. Replay and log saved in: {run_output_dir}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(script_dir, "configs", "run", "run_config.yaml")

    parser = argparse.ArgumentParser(
        description="Run a block-design experiment for the Werewolf game, "
        "where each block is a complete role rotation amongst the players."
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        help="Output directory for game replays and logs.",
        default="werewolf_block_experiment",
    )
    parser.add_argument(
        "-c", "--config", type=str, default=default_config_path, help="Path to the base configuration YAML file."
    )
    parser.add_argument(
        "-b",
        "--num_blocks",
        type=int,
        default=10,
        help="Number of blocks to run. Each block is a complete role rotation.",
    )
    parser.add_argument(
        "-r", "--use_random_agents", action="store_true", help="Use random agents for all players for fast testing."
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode for the game environment. "
        "Note that you can use debug mode to enable intra game sequential execution.",
    )
    parser.add_argument("-p", "--parallel", action="store_true", help="Run games in parallel using multiple processes.")
    parser.add_argument(
        "-n", "--num_processes", type=int, default=None, help="Number of processes for parallel execution."
    )
    parser.add_argument(
        "-a", "--append_timestamp_to_dir", action="store_true", help="Append a timestamp to the output directory."
    )
    parser.add_argument(
        "-s",
        "--shuffle_player_ids",
        action="store_true",
        help="Shuffle player ids for each game to account for name bias.",
    )

    args = parser.parse_args()

    output_dir = append_timestamp_to_dir(args.output_dir, append=args.append_timestamp_to_dir)

    os.makedirs(output_dir, exist_ok=True)

    setup_logger(output_dir, "run_block")

    config = load_config(args.config)

    num_players = len(config.get("game_config", {}).get("agents", []))
    if args.num_processes is None:
        num_processes = multiprocessing.cpu_count() * 0.9
        if not args.debug:
            num_processes /= num_players
        num_processes = max(1, math.floor(num_processes))
    else:
        num_processes = args.num_processes

    logger.info("Starting experiment with the following settings:")
    logger.info(f"Output Directory: {output_dir}")
    logger.info(f"Number of Blocks: {args.num_blocks}")
    logger.info(f"Parallel Execution: {args.parallel}")
    if args.parallel:
        logger.info(f"Number of Processes: {num_processes}")
    logger.info(f"Debug Mode: {args.debug}")
    logger.info(f"Use Random Agents: {args.use_random_agents}")
    logger.info(f"Shuffle Player IDs: {args.shuffle_player_ids}")

    with LogExecutionTime(logger_obj=logger, task_str="block experiment"):
        run_experiment(
            output_dir=output_dir,
            num_blocks=args.num_blocks,
            config=config,
            use_random_agents=args.use_random_agents,
            debug=args.debug,
            parallel=args.parallel,
            num_processes=num_processes,
            shuffle_player_ids=args.shuffle_player_ids,
        )
    logger.info("Experiment finished successfully.")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(script_dir, "configs", "run", "run_config.yaml")

    parser = argparse.ArgumentParser(description="Run a pairwise matrix tournament for the Werewolf game.")
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        help="Output directory for game replays and logs.",
        default="werewolf_pairwise_matrix",
    )
    parser.add_argument(
        "-c", "--config", type=str, default=default_config_path, help="Path to the base configuration YAML file."
    )
    parser.add_argument(
        "-t",
        "--num_tournaments",
        type=int,
        default=1,
        help="Number of tournaments to run. Each tournament is a full N*N matrix of games.",
    )
    parser.add_argument(
        "-r", "--use_random_agents", action="store_true", help="Use random agents for all players for fast testing."
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode for the game environment. Forces sequential execution.",
    )
    parser.add_argument("-p", "--parallel", action="store_true", help="Run games in parallel using multiple processes.")
    parser.add_argument(
        "-n", "--num_processes", type=int, default=None, help="Number of processes for parallel execution."
    )
    parser.add_argument(
        "-a", "--append_timestamp_to_dir", action="store_true", help="Append a timestamp to the output directory."
    )

    args = parser.parse_args()

    output_dir = append_timestamp_to_dir(args.output_dir, append=args.append_timestamp_to_dir)

    os.makedirs(output_dir, exist_ok=True)

    setup_logger(output_dir, "run_pairwise_matrix")

    config = load_config(args.config)

    if args.num_processes is None:
        num_processes = max(1, math.floor(multiprocessing.cpu_count() * 0.8))
    else:
        num_processes = args.num_processes

    logger.info("Starting tournament with the following settings:")
    logger.info(f"Output Directory: {output_dir}")
    logger.info(f"Number of Tournaments: {args.num_tournaments}")
    logger.info(f"Parallel Execution: {args.parallel}")
    if args.parallel:
        logger.info(f"Number of Processes: {num_processes}")
    logger.info(f"Debug Mode: {args.debug}")
    logger.info(f"Use Random Agents: {args.use_random_agents}")

    with LogExecutionTime(logger_obj=logger, task_str="pairwise matrix tournament"):
        run_tournament(
            output_dir=output_dir,
            num_tournaments=args.num_tournaments,
            config=config,
            use_random_agents=args.use_random_agents,
            debug=args.debug,
            parallel=args.parallel,
            num_processes=num_processes,
        )
    logger.info("Tournament finished successfully.")


def main():
    """Main function to orchestrate the sampling and running of games."""
    args = parse_arguments()
    run_output_dir = setup_environment(args)

    agent_pool = load_agent_pool(args.agent_pool_configs)
    if not agent_pool:
        logger.error("Agent pool is empty. Please check your agent pool config files.")
        return

    with open(args.base_game_config, "r") as f:
        base_config = yaml.safe_load(f)
        game_config_template = base_config.get("game_config", {})

    game_tasks = generate_game_tasks(args, run_output_dir, agent_pool, game_config_template)

    if game_tasks:
        run_games(args, game_tasks)
        logger.info(f"All games finished. Results saved in: {run_output_dir}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(script_dir, "configs", "run", "roundrobin_discussion_small.yaml")

    parser = argparse.ArgumentParser(description="Run N self-play Werewolf games based on a configuration file.")
    parser.add_argument(
        "-c", "--config_path", type=str, default=default_config_path, help="Path to the YAML configuration file."
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="werewolf_self_play",
        help="Output directory for the log and replay files.",
    )
    parser.add_argument(
        "-m",
        "--model_name",
        type=str,
        default="gemini/gemini-2.5-flash",
        help="The model name by litellm for self play.",
    )
    parser.add_argument(
        "-t",
        "--thumbnail",
        type=str,
        default="https://storage.googleapis.com/kaggle-static/game-arena/werewolf/thumbnails/gemini.png",
        help="The thumbnail image url.",
    )
    parser.add_argument("-n", "--num_games", type=int, default=1, help="Number of self-play games to run.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument(
        "-r", "--random_agents", action="store_true", help="Use random agents for all players for fast testing."
    )
    parser.add_argument(
        "-a", "--append_timestamp_to_dir", action="store_true", help="Append a timestamp to the output directory."
    )
    parser.add_argument(
        "-s", "--shuffle_roles", action="store_true", help="If provided, shuffle the roles for each game."
    )
    parser.add_argument("-p", "--parallel", action="store_true", help="Run games in parallel using multiple processes.")
    parser.add_argument("--num_processes", type=int, default=None, help="Number of processes for parallel execution.")

    args = parser.parse_args()

    run_output_dir = append_timestamp_to_dir(args.output_dir, append=args.append_timestamp_to_dir)
    os.makedirs(run_output_dir, exist_ok=True)
    setup_logger(output_dir=run_output_dir, base_name="self_play")

    with open(args.config_path, "r") as f:
        config = yaml.safe_load(f)

    num_processes = args.num_processes
    if args.parallel and num_processes is None:
        # Default to 4x the number of CPUs for I/O bound tasks
        num_processes = multiprocessing.cpu_count() * 4

    logger.info("Starting self-play with the following settings:")
    logger.info(f"Model Name: {args.model_name}")
    logger.info(f"Thumbnail: {args.thumbnail}")
    logger.info(f"Output Directory: {run_output_dir}")
    logger.info(f"Number of Games: {args.num_games}")
    logger.info(f"Config Path: {args.config_path}")
    logger.info(f"Parallel Execution: {args.parallel}")
    if args.parallel:
        logger.info(f"Number of Processes: {num_processes}")
    logger.info(f"Debug Mode: {args.debug}")
    logger.info(f"Use Random Agents: {args.random_agents}")
    logger.info(f"Shuffle Roles: {args.shuffle_roles}")

    with LogExecutionTime(logger_obj=logger, task_str=f"{args.num_games} self-play games"):
        run_self_play_games(
            model_name=args.model_name,
            thumbnail=args.thumbnail,
            output_dir=run_output_dir,
            num_games=args.num_games,
            config=config,
            use_random_agents=args.random_agents,
            debug=args.debug,
            parallel=args.parallel,
            num_processes=num_processes,
            shuffle_roles=args.shuffle_roles,
        )

    logger.info("Self-play run finished successfully.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Summarize Werewolf Game")
    parser.add_argument("-i", "--input_path", required=True, help="Path to the game replay JSON")
    parser.add_argument("-o", "--output_dir", help="Directory to save outputs (defaults to input file's directory)")
    parser.add_argument("--model", default="gemini-3-pro-preview", help="Gemini Model ID")
    parser.add_argument("--dry-run", action="store_true", help="Generate transcript only, do not call LLM")
    parser.add_argument("--max-retries", type=int, default=10, help="Max retries for API quota errors")
    args = parser.parse_args()

    json_path = args.input_path
    model_id = args.model
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = os.path.dirname(os.path.abspath(json_path))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(json_path))[0]
    transcript_path = os.path.join(output_dir, f"{base_name}_transcript.txt")
    summary_path = os.path.join(output_dir, f"{base_name}_summary.json")

    print(f"Reading game log from: {json_path}")
    transcript, turn_count = extract_game_transcript(json_path)
    
    if len(transcript) < 100:
        print("Transcript is too short or empty. Something went wrong with extraction.")
        print(transcript)
        sys.exit(1)
        
    print(f"Transcript length: {len(transcript)} characters.")
    
    # Always save transcript
    with open(transcript_path, "w") as f:
        f.write(transcript)
    print(f"Transcript saved to: {transcript_path}")

    if args.dry_run:
        return

    print(f"Sending to Gemini ({model_id})...")
    
    analysis = summarize_with_gemini(transcript, model_id, max_retries=args.max_retries)
    
    if analysis:
        analysis.total_turns = turn_count
        # Save structured JSON
        with open(summary_path, "w") as f:
             f.write(analysis.model_dump_json(indent=2))
        print(f"Summary saved to: {summary_path}")

        print("\n" + "="*50)
        print(f"GAME SUMMARY: {analysis.title}")
        print("="*50)
        print(f"\n{analysis.narrative_summary}\n")
        
        print(f"Winner: {analysis.winner_team}")
        print(f"MVP: {analysis.mvp_player} - {analysis.mvp_reasoning}")
        print(f"Best Play: {analysis.best_play}")
        print(f"Biggest Mistake: {analysis.biggest_mistake}")
        
        print("\n" + "-"*30)
        print("ENTERTAINMENT METRICS")
        print("-"*30)
        print(f"Score: {analysis.entertainment_metrics.excitement_score}/10 ({analysis.entertainment_metrics.outcome_type})")
        print("Dramatic Moments:")
        for moment in analysis.entertainment_metrics.dramatic_moments:
            print(f"- {moment}")

        print("\n" + "-"*30)
        print("PLAYER STATS")
        print("-"*30)
        
        for stat in analysis.player_stats:
            print(f"\n{stat.display_name} ({stat.role})")
            print(f"  Persuasion: {stat.persuasion}/10 | Deception: {stat.deception}/10")
            print(f"  Aggression: {stat.aggression}/10 | Analysis:  {stat.analysis}/10")

        print("\n" + "-"*30)
        print("PLAYER HIGHLIGHTS")
        print("-"*30)
        
        for player in analysis.player_highlights:
            print(f"\nPlayer: {player.player_name} ({player.role})")
            print(f"Summary: {player.summary}")
            print(f"Key Move: {player.key_move}")
            
    else:
        print("Failed to generate analysis.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-moves", type=int, default=10)
    parser.add_argument(
        "--model",
        default=os.environ.get("MODEL_NAME", "gemini-2.5-flash"),
    )
    args = parser.parse_args()

    if "GEMINI_API_KEY" not in os.environ:
        sys.exit("GEMINI_API_KEY must be set in the environment.")

    os.environ["MODEL_NAME"] = args.model
    os.environ.setdefault("MODEL_PROXY_KEY", "unused")
    os.environ.setdefault("MODEL_PROXY_URL", "dummy_url")

    open_spiel_env._register_game_envs(["connect_four"])
    env = make("open_spiel_connect_four", debug=True)
    env.reset()
    _wrap_litellm_with_logging()

    agent_fn = create_agent_fn(_C4Harness())

    moves_played = 0
    last_action_string = None
    while moves_played < args.num_moves:
        is_setup_step = len(env.steps) == 1
        submissions = []
        for s in env.state:
            if s["status"] == "ACTIVE":
                result = agent_fn(s["observation"], {})
                if result.get("submission") is not None:
                    last_action_string = result.get("actionString")
                submissions.append(result)
            else:
                submissions.append({"submission": -1})

        if is_setup_step:
            print("\n========== Setup step ==========")
            print(f">>> Submissions: {submissions}")
        else:
            moves_played += 1
            print(f"\n========== Move {moves_played}: {last_action_string or '?'} ==========")

        env.step(submissions)
        if env.done:
            print("\nGame finished.")
            break

    print("\n========== Final board ==========")
    print(env.state[0]["observation"].get("observationString", "(no observation)"))
    print("\n========== Results ==========")
    for i, s in enumerate(env.state):
        print(f"Agent {i}: status={s['status']}, reward={s['reward']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-moves", type=int, default=5)
    parser.add_argument("--board-size", type=int, default=9)
    parser.add_argument("--komi", type=float, default=7.5)
    parser.add_argument(
        "--model", default=os.environ.get("MODEL_NAME", "gemini-2.5-flash")
    )
    args = parser.parse_args()

    if "GEMINI_API_KEY" not in os.environ:
        sys.exit("GEMINI_API_KEY must be set in the environment.")

    os.environ["MODEL_NAME"] = args.model
    os.environ.setdefault("MODEL_PROXY_KEY", "unused")
    os.environ.setdefault("MODEL_PROXY_URL", "dummy_url")

    open_spiel_env._register_game_envs(["go"])
    env = make(
        "open_spiel_go",
        {
            "openSpielGameParameters": {
                "board_size": args.board_size,
                "komi": args.komi,
            }
        },
        debug=True,
    )
    env.reset()
    _wrap_litellm_with_logging()

    agent_fn = create_agent_fn(_GoHarness())

    moves_played = 0
    last_action_string = None
    while moves_played < args.num_moves:
        is_setup_step = len(env.steps) == 1
        submissions = []
        for s in env.state:
            if s["status"] == "ACTIVE":
                result = agent_fn(s["observation"], {})
                if result.get("submission") is not None:
                    last_action_string = result.get("actionString")
                submissions.append(result)
            else:
                submissions.append({"submission": -1})

        if is_setup_step:
            print("\n========== Setup step ==========")
            print(f">>> Submissions: {submissions}")
        else:
            moves_played += 1
            print(f"\n========== Move {moves_played}: {last_action_string or '?'} ==========")

        env.step(submissions)
        if env.done:
            print("\nGame finished.")
            break

    print("\n========== Final board ==========")
    print(env.state[0]["observation"].get("observationString", "(no observation)"))


def main() -> None:
    args = parse_args()
    if args.output.exists() and not args.force:
        raise FileExistsError(f"{args.output} already exists. Pass --force to overwrite.")

    if not args.skip_verify:
        confirm_chance_action_range(args.deck_size)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as outfile:
        for preset in generate_presets(
            seed=args.seed,
            num_presets=args.num_presets,
            num_hands=args.num_hands,
            cards_per_hand=args.cards_per_hand,
            deck_size=args.deck_size,
        ):
            outfile.write(json.dumps(preset))
            outfile.write("\n")
    LOGGER.info("Wrote %d preset hand group(s) to %s", args.num_presets, args.output.resolve())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-hands", type=int, default=2)
    parser.add_argument(
        "--model",
        default=os.environ.get("MODEL_NAME", "gemini-2.5-flash"),
    )
    args = parser.parse_args()

    if "GEMINI_API_KEY" not in os.environ and "OPENAI_API_KEY" not in os.environ:
        sys.exit("GEMINI_API_KEY or OPENAI_API_KEY must be set in the environment.")

    os.environ["MODEL_NAME"] = args.model
    os.environ.setdefault(
        "MODEL_PROXY_KEY",
        os.environ.get("GEMINI_API_KEY", os.environ.get("OPENAI_API_KEY", "unused")),
    )
    os.environ.setdefault("MODEL_PROXY_URL", "dummy_url")

    open_spiel_env._register_game_envs(["repeated_poker"])
    env = make(
        "open_spiel_repeated_poker",
        configuration={"setNumHands": args.num_hands},
        debug=True,
    )
    env.reset()
    _wrap_litellm_with_logging()

    agent_fn = create_agent_fn(_PokerHarness())

    move_count = 0
    while not env.done:
        submissions = []
        for s in env.state:
            if s["status"] == "ACTIVE":
                result = agent_fn(s["observation"], {})
                submissions.append(result)
            else:
                submissions.append({"submission": -1})

        if any(isinstance(sub, dict) and sub.get("actionString") for sub in submissions):
            move_count += 1
            played = next(
                sub["actionString"]
                for sub in submissions
                if isinstance(sub, dict) and sub.get("actionString")
            )
            print(f"\n========== Move {move_count}: {played} ==========")

        env.step(submissions)

    print("\n========== Final state ==========")
    print(env.state[0]["observation"].get("observationString", "(no observation)"))
    print("\n========== Results ==========")
    for i, s in enumerate(env.state):
        print(f"Agent {i}: status={s['status']}, reward={s['reward']}")


def main() -> None:
    if "GEMINI_API_KEY" not in os.environ:
        sys.exit("GEMINI_API_KEY must be set in the environment.")

    os.environ.setdefault("MODEL_NAME", "gemini-2.5-flash")
    os.environ.setdefault("MODEL_PROXY_KEY", os.environ["GEMINI_API_KEY"])
    os.environ.setdefault("MODEL_PROXY_URL", "dummy_url")

    open_spiel_env._register_game_envs(["ultimate_tic_tac_toe"])
    env = make("open_spiel_ultimate_tic_tac_toe", debug=True)
    env.reset()

    agent_fn = create_agent_fn(_UltimateTicTacToeHarness())

    move_count = 0
    while not env.done:
        submissions = []
        for s in env.state:
            if s["status"] == "ACTIVE":
                result = agent_fn(s["observation"], {})
                submissions.append(result)
            else:
                submissions.append({"submission": -1})

        # Print step actions
        for i, sub in enumerate(submissions):
            if isinstance(sub, dict) and sub.get("actionString"):
                move_count += 1
                print(f"\n========== Move {move_count} (Agent {i}): {sub['actionString']} ==========")
                if sub.get("thoughts"):
                    print(f"Thoughts: {sub['thoughts']}")

        env.step(submissions)

    print("\n========== Final board ==========")
    print(env.state[0]["observation"].get("observationString", "(no observation)"))
    print("\n========== Results ==========")
    for i, s in enumerate(env.state):
        print(f"Agent {i}: status={s['status']}, reward={s['reward']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=("Verify migrated repeated_poker harness prompts against an old replay.")
    )
    parser.add_argument("replay", help="Path to old-format repeated_poker replay JSON")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print a line per matching prompt")
    args = parser.parse_args()

    mismatches = verify(args.replay, verbose=args.verbose)
    sys.exit(1 if mismatches else 0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify migrated connect_four harness prompts against an old replay."
    )
    parser.add_argument("replay", help="Path to old-format connect_four replay JSON")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print a line per matching prompt"
    )
    args = parser.parse_args()

    mismatches = verify(args.replay, verbose=args.verbose)
    sys.exit(1 if mismatches else 0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify migrated chess harness prompts against an old replay."
    )
    parser.add_argument("replay", help="Path to old-format chess replay JSON")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print a line per matching prompt"
    )
    args = parser.parse_args()

    mismatches = verify(args.replay, verbose=args.verbose)
    sys.exit(1 if mismatches else 0)


def main():
    atheris.instrument_all()
    atheris.Setup(
        sys.argv,
        test_schemas.hypothesis.fuzz_one_input,
        enable_python_coverage=True,
    )
    atheris.Fuzz()


def main(argv):
  if len(argv) != 1:
    raise app.UsageError('No positional arguments are accepted.')

  if not _IR_DEST.value and not _IR_HUMAN_DEST.value:
    raise app.Error('At least one of --ir_dest and '
                    '--ir_human_dest is required.')

  raw_input_shapes = _INPUT_SHAPES.value
  raw_fn_name = _FN.value
  assert raw_input_shapes is not None  # required by set_up_flags
  assert raw_fn_name is not None  # required by set_up_flags

  module_name, fn_name = raw_fn_name.rsplit('.', 1)
  module = importlib.import_module(module_name)
  fn = getattr(module, fn_name)

  input_shapes = [(name, parse_shape_str(shape_str))
                  for name, shape_str in literal_eval(raw_input_shapes)]

  # Parse --constants and --evaled_constants.
  constants = {}
  for k, v in literal_eval(_CONSTANTS.value).items():
    if isinstance(v, list):
      v = jnp.asarray(v)
    constants[k] = v

  for k, v in literal_eval(_EVALED_CONSTANTS.value).items():
    if isinstance(v, str):
      v = literal_eval(v)
    if isinstance(v, list):
      v = jnp.asarray(v)
    if k in constants:
      raise ValueError(
          'Argument appears in both --constants and --evaled_constants: %s' % k)
    constants[k] = v

  ir, debug_ir = jax_to_ir(fn, input_shapes, constants=constants,
                           format=_IR_FORMAT.value)

  if _IR_DEST.value:
    with open(_IR_DEST.value, 'wb') as f:
      f.write(ir)

  if _IR_HUMAN_DEST.value:
    with open(_IR_HUMAN_DEST.value, 'w') as f:
      f.write(debug_ir)


def main(shard_main=None):
  config.config_with_absl()
  app.run(functools.partial(_main, shard_main=shard_main))


def main(unused_argv):
  num_q_heads = 16
  num_kv_heads = 16
  use_pipeline_emitter = False
  if use_pipeline_emitter:
    attention_impl = attention_with_pipeline_emitter
    schedule_barrier_opts = (True, False)
  else:
    attention_impl = attention
    schedule_barrier_opts = (True,)

  problem_it = itertools.product(
      (1,), (4096, 32768,), (64, 128, 256,), schedule_barrier_opts, (False, True))
  for batch_size, seq_len, head_dim, use_schedule_barrier, causal in problem_it:
    assert cuda_versions is not None
    cuda_runtime_version = cuda_versions.cuda_runtime_get_version()
    # TODO(pobudzey): Undo when we upgrade to cuda 12.9.1.
    if causal and cuda_runtime_version >= 12080 and cuda_runtime_version < 12091:
      continue

    if causal and use_pipeline_emitter:
      continue
    q_seq_len = kv_seq_len = seq_len
    print(f"==== {batch_size=:<6} {kv_seq_len=:<6} {q_seq_len=:<6}"
          f"{num_q_heads=:<4} {head_dim=:<6} {use_schedule_barrier=:} {causal=:} ====")
    k1, k2, k3 = jax.random.split(jax.random.key(42), 3)
    q = jax.random.normal(k1, (batch_size, q_seq_len, num_q_heads, head_dim), jnp.float16)
    k = jax.random.normal(k2, (batch_size, kv_seq_len, num_kv_heads, head_dim), jnp.float16)
    v = jax.random.normal(k3, (batch_size, kv_seq_len, num_kv_heads, head_dim), jnp.float16)
    block_q = 64
    best = None
    for block_kv in (256, 128, 64):
      config = TuningConfig(block_q=block_q, block_kv=block_kv, max_concurrent_steps=2, use_schedule_barrier=use_schedule_barrier, causal=causal)
      try:
        out, runtime_ms = profiler.measure(functools.partial(attention_impl, config=config))(q, k, v)
        if seq_len < 32768:
          out_ref = attention_reference(q, k, v, causal=causal)
          np.testing.assert_allclose(out, out_ref, atol=2e-3, rtol=1e-3)
      except ValueError as e:
        if "exceeds available shared memory" in e.args[0]:
          continue
        raise
      assert runtime_ms is not None
      runtime_us = runtime_ms * 1e3
      matmul_flops = (
          4 * q_seq_len * kv_seq_len * head_dim * num_q_heads * batch_size
      )
      if causal:
        matmul_flops //= 2
      peak_flops = 1e15  # f16 TensorCore peak = 1000TFLOPS
      optimal_time = matmul_flops / peak_flops * 1e6  # us
      achieved_tc_util = optimal_time / runtime_us * 100
      print(
          f"block_q={block_q:<4}block_kv={block_kv:<4}:  {runtime_us:<7.1f}us"
          f" = {achieved_tc_util:4.1f}% TC utilization"
      )
      if best is None or runtime_us < best[0]:
        best = (runtime_us, achieved_tc_util)
      break  # Remove this for full autotuning.
    if best is not None:
      print(f"Best: {best[0]:<7.1f}us = {best[1]:4.1f}% TC utilization")


def main(_) -> None:
  problem_it = [(4096, 8192, 4096)]
  for M, N, K in problem_it:
    print(f"==== {M=} {N=} {K=} ====")
    matmul_flops = 2 * M * N * K
    peak_flops = 2.25e15  # f16 TensorCore peak = 2250 TFLOPS
    a = jax.random.uniform(jax.random.key(1), (M, K), jnp.float16, -1, 1)
    b = jax.random.uniform(jax.random.key(2), (K, N), jnp.float16, -1, 1)
    tuning_it = itertools.product(
        (128,),  # tile_m
        (128, 256),  # tile_n
        (64,),  # tile_k
        MatmulDimension,  # grid_minor_dim
        (1, 4, 8, 12, 16),  # grid_tile_width
        (2, 4, 6),  # max_concurrent_steps
        (False, True),  # collective
        (32,),  # epilogue_tile_n
    )
    best_util = -float("inf")
    expected = jnp.dot(a, b, precision=jax.lax.DotAlgorithmPreset.F16_F16_F32)
    for (tile_m, tile_n, tile_k, grid_minor_dim, grid_tile_width,
         max_concurrent_steps, collective, epilogue_tile_n) in tuning_it:
      # Only N <= 128 are supported for collective MMAs
      if collective and tile_n > 128:
        continue
      config = TuningConfig(
          tile_m=tile_m,
          tile_n=tile_n,
          tile_k=tile_k,
          max_concurrent_steps=max_concurrent_steps,
          collective=collective,
          epilogue_tile_n=epilogue_tile_n,
          grid_minor_dim=grid_minor_dim,
          grid_tile_width=grid_tile_width,
      )
      if collective:
        tile_m *= 2
        tile_n *= 2
      try:
        out, runtimes_ms = profiler.measure(
            functools.partial(matmul_kernel, config=config), iterations=10
        )(a, b)
        assert runtimes_ms is not None
        runtime_ms = statistics.median(runtimes_ms)
      except ValueError as e:
        if ("exceeds available shared memory" in e.args[0] or
            "Accumulator layout mismatch:" in e.args[0]):
          # Accumulator layout mismatch triggers for tile_n=256 on some configs.
          continue
        raise
      runtime_us = runtime_ms * 1e3
      optimal_time = matmul_flops / peak_flops * 1e6  # us
      achieved_tc_util = optimal_time / runtime_us * 100
      if achieved_tc_util > best_util:
        np.testing.assert_allclose(out, expected)
        best_util = achieved_tc_util
      print(
          f"{tile_m=} {tile_n=} {tile_k=} {max_concurrent_steps=} "
          f"{grid_minor_dim=} {grid_tile_width=} "
          f"{epilogue_tile_n=} "
          f"{collective=} : "
          f"{runtime_us:<7.1f}us"
          f" = {achieved_tc_util:4.1f}% TC utilization"
      )
    print(f"\tBest utilization: {best_util:4.1f}%")
    _, runtimes_ms = profiler.measure(
        functools.partial(
            jnp.dot, precision=jax.lax.DotAlgorithmPreset.F16_F16_F32
        ),
        iterations=10,
    )(a, b)
    assert runtimes_ms is not None
    runtime_ms = statistics.median(runtimes_ms)
    runtime_us = runtime_ms * 1e3
    optimal_time = matmul_flops / peak_flops * 1e6  # us
    achieved_tc_util = optimal_time / runtime_us * 100
    print(f"\tReference: {achieved_tc_util:4.1f}%")


def main(_) -> None:
  M = 16 * 1024
  K = 2048
  N = 16 * 1024
  num_groups = 16
  group_sizes = sample_group_sizes(jax.random.key(0), num_groups, M, alpha=10.0)

  print(f"==== {M=} {N=} {K=} {num_groups=}====")
  matmul_flops = 2 * M * N * K
  peak_flops = 2.25e15  # f16 TensorCore peak = 2250 TFLOPS
  a = jax.random.uniform(jax.random.key(1), (M, K), jnp.float16)
  b = jax.random.uniform(jax.random.key(2), (num_groups, K, N), jnp.float16)
  expected = ragged_dot_reference(a, b, group_sizes)

  tuning_it = itertools.product(
      (128,),  # tile_m
      (128,),  # tile_n
      (64,),  # tile_k
      (1, 8, 12, 16),  # grid_tile_width
      blackwell_matmul_mgpu.MatmulDimension,  # grid_minor_dim
      (4, 6)  # max_concurrent_steps
  )
  best_util = -float("inf")
  for (tile_m, tile_n, tile_k, grid_tile_width, grid_minor_dim,
        max_concurrent_steps,) in tuning_it:
    config = TuningConfig(
      tile_m=tile_m,
      tile_n=tile_n,
      tile_k=tile_k,
      grid_tile_width=grid_tile_width,
      grid_minor_dim=grid_minor_dim,
      max_concurrent_steps=max_concurrent_steps,
      collective=True,
    )
    try:
      out, runtime_ms = profiler.measure(
          functools.partial(ragged_dot_kernel, config=config),
          iterations=10
      )(a, b, group_sizes)
      runtime_ms = np.median(runtime_ms if runtime_ms else [])
    except ValueError as e:
      if ("exceeds available shared memory" in e.args[0] or
          "Accumulator layout mismatch:" in e.args[0]):
        print(e.args[0])
        continue
      raise
    np.testing.assert_allclose(out, expected)

    runtime_us = runtime_ms * 1e3
    optimal_time = matmul_flops / peak_flops * 1e6  # us
    achieved_tc_util = optimal_time / runtime_us * 100
    if achieved_tc_util > best_util:
      best_util = achieved_tc_util
    print(
        f"{tile_m=} {tile_n=} {tile_k=} {grid_tile_width=} {grid_minor_dim=} {max_concurrent_steps=} "
        f"{runtime_us:<7.1f}us"
        f" = {achieved_tc_util:4.1f}% TC utilization"
    )
  print(f"\tBest utilization: {best_util:4.1f}%")


def main(_) -> None:
  problem_it = [(4096, 8192, 4096)]
  for M, N, K in problem_it:
    print(f"==== {M=} {N=} {K=} ====")
    matmul_flops = 2 * M * N * K
    peak_flops = 990e12  # f16 TensorCore peak = 990 TFLOPS
    a = jax.random.uniform(jax.random.key(0), (M, K), jnp.float16)
    b = jax.random.uniform(jax.random.key(1), (K, N), jnp.float16)
    ref = a @ b
    tuning_it = itertools.product(
        (128, 256,),  # tile_m
        (64, 128),  # tile_n
        (64,),  # tile_k
        (4,),  # max_concurrent_steps
        (True,),  # Tiled epilogue
        (MatmulDimension.M, MatmulDimension.N),  # grid_minor_dim
        (4, 8, 16),  # grid_tile_width
        MatmulDimension,  # wg_dimension
        # Consider adding MatmulDimension here to try out collective TMA kernels
        (None,)  # cluster_dimension
    )
    best_util = 0.0
    best_runtime = float("inf")
    for tile_m, tile_n, tile_k, max_concurrent_steps, tiled_epilogue, grid_minor_dim, grid_tile_width, wg_dimension, cluster_dimension in tuning_it:
      config = TuningConfig(
          tile_m=tile_m,
          tile_n=tile_n,
          tile_k=tile_k,
          max_concurrent_steps=max_concurrent_steps,
          epi_tile_n=64 if tiled_epilogue else None,
          epi_tile_m=64 if tiled_epilogue else None,
          grid_minor_dim=grid_minor_dim,
          grid_tile_width=grid_tile_width,
          wg_dimension=wg_dimension,
          cluster_dimension=cluster_dimension,
      )
      try:
        out, runtimes_ms = profiler.measure(
            functools.partial(matmul, config=config), iterations=10,
        )(a, b, None)
        assert runtimes_ms is not None
        runtime_ms = statistics.median(runtimes_ms)
      except ValueError as e:
        if "exceeds available shared memory" in e.args[0]:  # Ignore SMEM OOMs.
          continue
        raise
      np.testing.assert_allclose(out, ref)
      runtime_us = runtime_ms * 1e3
      optimal_time = matmul_flops / peak_flops * 1e6  # us
      achieved_tc_util = optimal_time / runtime_us * 100
      if achieved_tc_util > best_util:
        best_runtime = runtime_us
        best_util = achieved_tc_util
      print(
          f"{tile_m=} {tile_n=} {tile_k=} {max_concurrent_steps=} {tiled_epilogue=} {grid_minor_dim=} {grid_tile_width=} {wg_dimension=} {cluster_dimension=}:"
          f" {runtime_us:<7.1f}us = {achieved_tc_util:4.1f}% TC utilization"
      )
    print(f"\tBest: {best_runtime:<7.1f}us = {best_util:4.1f}% TC utilization")


def main(_) -> None:
  problem_it = [(4096, 8192, 4096)]
  for M, N, K in problem_it:
    print(f"==== {M=} {N=} {K=} ====")
    matmul_flops = 2 * M * N * K
    peak_flops = 990e12  # f16 TensorCore peak = 990 TFLOPS
    a = jax.random.randint(
        jax.random.key(0), minval=-128, maxval=127, shape=(M, K), dtype=jnp.int8
    )
    b = jax.random.uniform(jax.random.key(1), (K, N), jnp.bfloat16)
    ref = reference(a, b, out_dtype=jnp.bfloat16)
    tuning_it = itertools.product(
        (64, 128, 256,),  # tile_m
        (64, 128),  # tile_n
        (64, 128),  # tile_k
        (4,),  # max_concurrent_steps
        (True,),  # Tiled epilogue
        (MatmulDimension.M, MatmulDimension.N),  # grid_minor_dim
        (4, 8, 16),  # grid_tile_width
        MatmulDimension,  # wg_dimension
        # Consider adding MatmulDimension here to try out collective TMA kernels
        (None,)  # cluster_dimension
    )
    best_util = 0.0
    best_runtime = float("inf")
    for tile_m, tile_n, tile_k, max_concurrent_steps, tiled_epilogue, grid_minor_dim, grid_tile_width, wg_dimension, cluster_dimension in tuning_it:
      config = TuningConfig(
          tile_m=tile_m,
          tile_n=tile_n,
          tile_k=tile_k,
          max_concurrent_steps=max_concurrent_steps,
          epi_tile_n=64 if tiled_epilogue else None,
          epi_tile_m=64 if tiled_epilogue else None,
          grid_minor_dim=grid_minor_dim,
          grid_tile_width=grid_tile_width,
          wg_dimension=wg_dimension,
          cluster_dimension=cluster_dimension,
      )
      try:
        out, runtimes_ms = profiler.measure(
            functools.partial(
                mixed_matmul_kernel, out_dtype=jnp.bfloat16, config=config
            ),
            iterations=10,
        )(a, b)
        assert runtimes_ms is not None
        runtime_ms = statistics.median(runtimes_ms)
      except ValueError as e:
        if "exceeds available shared memory" in e.args[0]:  # Ignore SMEM OOMs.
          continue
        raise
      np.testing.assert_allclose(out, ref)
      runtime_us = runtime_ms * 1e3
      optimal_time = matmul_flops / peak_flops * 1e6  # us
      achieved_tc_util = optimal_time / runtime_us * 100
      if achieved_tc_util > best_util:
        best_runtime = runtime_us
        best_util = achieved_tc_util
      print(
          f"{tile_m=} {tile_n=} {tile_k=} {max_concurrent_steps=} {tiled_epilogue=} {grid_minor_dim=} {grid_tile_width=} {wg_dimension=} {cluster_dimension=}:"
          f" {runtime_us:<7.1f}us = {achieved_tc_util:4.1f}% TC utilization"
      )
    print(f"\tBest: {best_runtime:<7.1f}us = {best_util:4.1f}% TC utilization")


def main(unused_argv):
  for transpose_rhs in [False, True]:
    m, k, n, num_groups = 16 * 1024, 2048, 16 * 1024, 16
    kx, ky, kz = random.split(random.key(1234), num=3)

    lhs = jax.random.normal(kx, (m, k), jnp.float16)
    if transpose_rhs:
      rhs = jax.random.normal(ky, (num_groups, n, k), jnp.float16)
    else:
      rhs = jax.random.normal(ky, (num_groups, k, n), jnp.float16)
    group_boundaries = jax.lax.sort(
        jax.random.randint(kz, (num_groups - 1,), 0, m, jnp.int32)
    )
    group_starts = lax.concatenate(
        [jnp.array([0], dtype=jnp.int32), group_boundaries], 0
    )
    group_ends = lax.concatenate(
        [group_boundaries, jnp.array([m], dtype=jnp.int32)], 0
    )
    group_sizes = group_ends - group_starts
    assert group_sizes.shape == (num_groups,)

    block_m = block_n = (64, 128, 192)
    block_k = (64,)
    max_concurrent_steps = (2, 4, 5, 6)
    grid_block_n = (1, 2, 4, 8, 16)
    configs = itertools.product(
        block_m, block_n, block_k, max_concurrent_steps, grid_block_n
    )
    names = (
        "block_m", "block_n", "block_k", "max_concurrent_steps", "grid_block_n"
    )
    best_runtime = float("inf")
    best_kwargs: dict[str, int] = {}
    for config in configs:
      kwargs = dict(zip(names, config))
      if n % (kwargs["grid_block_n"] * kwargs["block_n"]):
        continue
      try:
        f = functools.partial(
            ragged_dot, group_sizes=group_sizes, transpose_rhs=transpose_rhs,
            **kwargs
        )
        _, runtime = profiler.measure(f)(lhs, rhs)
      except ValueError as e:
        if "Mosaic GPU kernel exceeds available shared memory" not in str(e):
          raise
        runtime = float("inf")
      # Enable this to get more detailed information.
      else:
        assert runtime is not None
        print(" ".join(f"{k}={v}" for k, v in kwargs.items()), int(runtime * 1000))
      if runtime < best_runtime:
        best_runtime = runtime
        best_kwargs = kwargs
    if not best_kwargs:
      raise ValueError("No valid configuration found")

    def ref_ragged_dot(lhs, rhs, group_sizes):
      if transpose_rhs:
        rhs = jnp.transpose(rhs, (0, 2, 1))
      return jax.lax.ragged_dot(lhs, rhs, group_sizes=group_sizes)

    ref, ref_runtime = profiler.measure(ref_ragged_dot)(
        lhs, rhs, group_sizes=group_sizes
    )
    assert ref_runtime is not None
    result = ragged_dot(
        lhs, rhs, group_sizes=group_sizes, transpose_rhs=transpose_rhs,
        load_group_sizes_to_register=True,
        **best_kwargs
    )
    np.testing.assert_allclose(result, ref, atol=1e-3, rtol=1e-3)

    tflops = float(2 * k * m * n) / (best_runtime / 1e3) / 1e12
    ref_tflops = float(2 * k * m * n) / (ref_runtime / 1e3) / 1e12
    print(f"Transpose RHS: {transpose_rhs}")
    print(
        "Best parameters: ", " ".join(f"{k}={v}" for k, v in best_kwargs.items())
    )
    print(f"Kernel:    {best_runtime * 1000:.1f} us = {tflops:.1f} TFLOPS")
    print(f"Reference: {ref_runtime * 1000:.1f} us = {ref_tflops:.1f} TFLOPS")


def main(unused_argv):
  k, m, n, num_groups = 16 * 1024, 2048, 2048, 16
  kx, ky, kz = random.split(random.key(1234), num=3)

  lhs = jax.random.normal(kx, (k, m), jnp.float16)
  rhs = jax.random.normal(ky, (k, n), jnp.float16)
  group_boundaries = jax.lax.sort(
      jax.random.randint(kz, (num_groups - 1,), 0, k, jnp.int32)
  )
  group_starts = lax.concatenate(
      [jnp.array([0], dtype=jnp.int32), group_boundaries], 0
  )
  group_ends = lax.concatenate(
      [group_boundaries, jnp.array([k], dtype=jnp.int32)], 0
  )
  group_sizes = group_ends - group_starts
  assert group_sizes.shape == (num_groups,)

  block_m = block_n = [64, 128]
  block_k = [64, 128]
  max_concurrent_steps = [1, 2, 4, 5, 6]
  grid_block_n = [1, 2, 4, 8, 16]

  configs = itertools.product(
      block_m, block_n, block_k, max_concurrent_steps, grid_block_n
  )
  names = (
      "block_m", "block_n", "block_k", "max_concurrent_steps", "grid_block_n",
  )
  best_runtime = float("inf")
  best_kwargs = {}
  for config in configs:
    kwargs = dict(zip(names, config))
    if n %  kwargs["block_n"]:
      continue
    try:
      f = functools.partial(
          transposed_ragged_dot, group_sizes=group_sizes,
          **kwargs
      )
      _, runtime = profiler.measure(f)(lhs, rhs)
    except ValueError as e:
      if "Mosaic GPU kernel exceeds available shared memory" not in str(e):
        raise
      runtime = float("inf")
    # Enable this to get more detailed information.
    else:
      assert runtime is not None
      print(
          " ".join(f"{k}={v}" for k, v in kwargs.items()),
          f"{int(runtime * 1000):.1f} us",
      )
    assert runtime is not None
    assert best_runtime is not None
    if runtime < best_runtime:
      best_runtime = runtime
      best_kwargs = kwargs
  if not best_kwargs:
    raise ValueError("No valid configuration found")

  ref, ref_runtime = profiler.measure(ref_transposed_ragged_dot)(
      lhs, rhs, group_sizes=group_sizes
  )
  result = transposed_ragged_dot(
      lhs, rhs, group_sizes=group_sizes, **best_kwargs
  )

  assert ref_runtime is not None
  tflops = float(2 * k * m * n) / (best_runtime / 1e3) / 1e12
  ref_tflops = float(2 * k * m * n) / (ref_runtime / 1e3) / 1e12
  print(
      "Best parameters: ", " ".join(f"{k}={v}" for k, v in best_kwargs.items())
  )
  print(f"Kernel:    {best_runtime * 1000:.1f} us = {tflops:.1f} TFLOPS")
  print(f"Reference: {ref_runtime * 1000:.1f} us = {ref_tflops:.1f} TFLOPS")
  np.testing.assert_allclose(result, ref, atol=1e-3, rtol=1e-3)


def main() -> None:
    out.warning("`huggingface-cli` is deprecated and no longer works. Use `hf` instead.\n")

    if shutil.which("hf"):
        from huggingface_hub.cli._cli_utils import check_cli_update

        check_cli_update("huggingface_hub")
        out.hint("`hf` is already installed! Use it directly.\n")
    else:
        out.hint(
            "Install `hf`:\n"
            "  Standalone (recommended): curl -LsSf https://hf.co/cli/install.sh | bash\n"
            "  Using Homebrew:           brew install hf\n"
            "  Using pip:                pip install huggingface_hub\n",
        )

    out.hint(
        "Examples:\n"
        "  hf auth login\n"
        "  hf download unsloth/gemma-4-31B-it-GGUF\n"
        "  hf upload my-cool-model . .\n"
        '  hf models ls --search "gemma"\n'
        "  hf repos ls --format json\n"
        "  hf jobs run python:3.12 python -c 'print(\"Hello!\")'\n"
        "  hf --help\n",
    )
    sys.exit(1)


def main():
    if not constants.HF_DEBUG:
        logging.set_verbosity_info()
    check_cli_update("huggingface_hub")

    try:
        app()
    except Exception as e:
        message = format_known_exception(e)
        if message:
            out.error(message)
            if constants.HF_DEBUG:
                traceback.print_exc()
            else:
                out.hint("set HF_DEBUG=1 as environment variable for full traceback.")
            sys.exit(1)
        raise


def main(args=None):
    """Convert CFF2 OTF font to CFF OTF font"""
    if args is None:
        import sys

        args = sys.argv[1:]

    import argparse

    parser = argparse.ArgumentParser(
        "fonttools cffLib.CFF2ToCFF",
        description="Convert a non-variable CFF2 font to CFF.",
    )
    parser.add_argument(
        "input", metavar="INPUT.ttf", help="Input OTF file with CFF table."
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT.ttf",
        default=None,
        help="Output instance OTF file (default: INPUT-CFF2.ttf).",
    )
    parser.add_argument(
        "--no-recalc-timestamp",
        dest="recalc_timestamp",
        action="store_false",
        help="Don't set the output font's timestamp to the current time.",
    )
    parser.add_argument(
        "--remove-overlaps",
        action="store_true",
        help="Merge overlapping contours and components. Requires skia-pathops",
    )
    parser.add_argument(
        "--ignore-overlap-errors",
        action="store_true",
        help="Don't crash if the remove-overlaps operation fails for some glyphs.",
    )
    loggingGroup = parser.add_mutually_exclusive_group(required=False)
    loggingGroup.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )
    loggingGroup.add_argument(
        "-q", "--quiet", action="store_true", help="Turn verbosity off."
    )
    options = parser.parse_args(args)

    from fontTools import configLogger

    configLogger(
        level=("DEBUG" if options.verbose else "ERROR" if options.quiet else "INFO")
    )

    import os

    infile = options.input
    if not os.path.isfile(infile):
        parser.error("No such file '{}'".format(infile))

    outfile = (
        makeOutputFileName(infile, overWrite=True, suffix="-CFF")
        if not options.output
        else options.output
    )

    font = TTFont(infile, recalcTimestamp=options.recalc_timestamp, recalcBBoxes=False)

    convertCFF2ToCFF(font)

    if options.remove_overlaps:
        from fontTools.ttLib.removeOverlaps import removeOverlaps
        from io import BytesIO

        log.debug("Removing overlaps")

        stream = BytesIO()
        font.save(stream)
        stream.seek(0)
        font = TTFont(stream, recalcTimestamp=False, recalcBBoxes=False)
        removeOverlaps(
            font,
            ignoreErrors=options.ignore_overlap_errors,
        )

    log.info(
        "Saving %s",
        outfile,
    )
    font.save(outfile)


def main(args=None):
    """Convert CFF OTF font to CFF2 OTF font"""
    if args is None:
        import sys

        args = sys.argv[1:]

    import argparse

    parser = argparse.ArgumentParser(
        "fonttools cffLib.CFFToCFF2",
        description="Upgrade a CFF font to CFF2.",
    )
    parser.add_argument(
        "input", metavar="INPUT.ttf", help="Input OTF file with CFF table."
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT.ttf",
        default=None,
        help="Output instance OTF file (default: INPUT-CFF2.ttf).",
    )
    parser.add_argument(
        "--no-recalc-timestamp",
        dest="recalc_timestamp",
        action="store_false",
        help="Don't set the output font's timestamp to the current time.",
    )
    loggingGroup = parser.add_mutually_exclusive_group(required=False)
    loggingGroup.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )
    loggingGroup.add_argument(
        "-q", "--quiet", action="store_true", help="Turn verbosity off."
    )
    options = parser.parse_args(args)

    from fontTools import configLogger

    configLogger(
        level=("DEBUG" if options.verbose else "ERROR" if options.quiet else "INFO")
    )

    import os

    infile = options.input
    if not os.path.isfile(infile):
        parser.error("No such file '{}'".format(infile))

    outfile = (
        makeOutputFileName(infile, overWrite=True, suffix="-CFF2")
        if not options.output
        else options.output
    )

    font = TTFont(infile, recalcTimestamp=options.recalc_timestamp, recalcBBoxes=False)

    convertCFFToCFF2(font)

    log.info(
        "Saving %s",
        outfile,
    )
    font.save(outfile)


def main(args=None):
    """Calculate optimum defaultWidthX/nominalWidthX values"""

    import argparse

    parser = argparse.ArgumentParser(
        "fonttools cffLib.width",
        description=main.__doc__,
    )
    parser.add_argument(
        "inputs", metavar="FILE", type=str, nargs="+", help="Input TTF files"
    )
    parser.add_argument(
        "-b",
        "--brute-force",
        dest="brute",
        action="store_true",
        help="Use brute-force approach (VERY slow)",
    )

    args = parser.parse_args(args)

    for fontfile in args.inputs:
        font = TTFont(fontfile)
        hmtx = font["hmtx"]
        widths = [m[0] for m in hmtx.metrics.values()]
        if args.brute:
            default, nominal = optimizeWidthsBruteforce(widths)
        else:
            default, nominal = optimizeWidths(widths)
        print(
            "glyphs=%d default=%d nominal=%d byteCost=%d"
            % (len(widths), default, nominal, byteCost(widths, default, nominal))
        )


def main():
    run_benchmark("cu2qu", "curve_to_quadratic")
    run_benchmark("cu2qu", "curves_to_quadratic")


def main(args=None):
    """Roundtrip .designspace file through the DesignSpaceDocument class"""

    if args is None:
        import sys

        args = sys.argv[1:]

    from argparse import ArgumentParser

    parser = ArgumentParser(prog="designspaceLib", description=main.__doc__)
    parser.add_argument("input")
    parser.add_argument("output")

    options = parser.parse_args(args)

    ds = DesignSpaceDocument.fromfile(options.input)
    ds.write(options.output)


def main():
    """Compare two fonts for differences"""
    # try/except block rationale:
    # handles "premature" socket closure exception that is
    # raised by Python when stdout is piped to tools like
    # the `head` executable and socket is closed early
    # see: https://docs.python.org/3/library/signal.html#note-on-sigpipe
    ret = 0
    try:
        ret = run(sys.argv[1:])
    except KeyboardInterrupt:
        pass
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
    return ret


def main(args=None):
    """Add features from a feature file (.fea) into an OTF font"""
    parser = argparse.ArgumentParser(
        description="Use fontTools to compile OpenType feature files (*.fea)."
    )
    parser.add_argument(
        "input_fea", metavar="FEATURES", help="Path to the feature file"
    )
    parser.add_argument(
        "input_font", metavar="INPUT_FONT", help="Path to the input font"
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_font",
        metavar="OUTPUT_FONT",
        help="Path to the output font.",
    )
    parser.add_argument(
        "-t",
        "--tables",
        metavar="TABLE_TAG",
        choices=Builder.supportedTables,
        nargs="+",
        help="Specify the table(s) to be built.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Add source-level debugging information to font.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase the logger verbosity. Multiple -v " "options are allowed.",
        action="count",
        default=0,
    )
    parser.add_argument(
        "--traceback", help="show traceback for exceptions.", action="store_true"
    )
    options = parser.parse_args(args)

    levels = ["WARNING", "INFO", "DEBUG"]
    configLogger(level=levels[min(len(levels) - 1, options.verbose)])

    output_font = options.output_font or makeOutputFileName(options.input_font)
    log.info("Compiling features to '%s'" % (output_font))

    font = TTFont(options.input_font)
    try:
        addOpenTypeFeatures(
            font, options.input_fea, tables=options.tables, debug=options.debug
        )
    except FeatureLibError as e:
        if options.traceback:
            raise
        log.error(e)
        sys.exit(1)
    font.save(output_font)


def main(args=None):
    """Merge multiple fonts into one"""
    from fontTools import configLogger

    if args is None:
        args = sys.argv[1:]

    options = Options()
    args = options.parse_opts(args)
    fontfiles = []
    if options.input_file:
        with open(options.input_file) as inputfile:
            fontfiles = [
                line.strip()
                for line in inputfile.readlines()
                if not line.lstrip().startswith("#")
            ]
    for g in args:
        fontfiles.append(g)

    if len(fontfiles) < 1:
        print(
            "usage: fonttools merge [font1 ... fontN] [--input-file=filelist.txt] [--output-file=merged.ttf] [--import-file=tables.ttx]",
            file=sys.stderr,
        )
        print(
            "                                   [--drop-tables=tags] [--verbose] [--timing]",
            file=sys.stderr,
        )
        print("", file=sys.stderr)
        print(" font1 ... fontN              Files to merge.", file=sys.stderr)
        print(
            " --input-file=<filename>      Read files to merge from a text file, each path new line. # Comment lines allowed.",
            file=sys.stderr,
        )
        print(
            " --output-file=<filename>     Specify output file name (default: merged.ttf).",
            file=sys.stderr,
        )
        print(
            " --import-file=<filename>     TTX file to import after merging. This can be used to set metadata.",
            file=sys.stderr,
        )
        print(
            " --drop-tables=<table tags>   Comma separated list of table tags to skip, case sensitive.",
            file=sys.stderr,
        )
        print(
            " --verbose                    Output progress information.",
            file=sys.stderr,
        )
        print(" --timing                     Output progress timing.", file=sys.stderr)
        return 1

    configLogger(level=logging.INFO if options.verbose else logging.WARNING)
    if options.timing:
        timer.logger.setLevel(logging.DEBUG)
    else:
        timer.logger.disabled = True

    merger = Merger(options=options)
    font = merger.merge(fontfiles)

    if options.import_file:
        font.importXML(options.import_file)

    with timer("compile and save font"):
        font.save(options.output_file)


def main(args=None, font=None):
    """Convert a FontDame OTL file to TTX XML

    Writes XML output to stdout.

    Args:
            args: Command line arguments (``--font``, ``--table``, input files).
    """
    import sys
    from fontTools import configLogger
    from fontTools.misc.testTools import MockFont

    if args is None:
        args = sys.argv[1:]

    # configure the library logger (for >= WARNING)
    configLogger()
    # comment this out to enable debug messages from mtiLib's logger
    # log.setLevel(logging.DEBUG)

    import argparse

    parser = argparse.ArgumentParser(
        "fonttools mtiLib",
        description=main.__doc__,
    )

    parser.add_argument(
        "--font",
        "-f",
        metavar="FILE",
        dest="font",
        help="Input TTF files (used for glyph classes and sorting coverage tables)",
    )
    parser.add_argument(
        "--table",
        "-t",
        metavar="TABLE",
        dest="tableTag",
        help="Table to fill (sniffed from input file if not provided)",
    )
    parser.add_argument(
        "inputs", metavar="FILE", type=str, nargs="+", help="Input FontDame .txt files"
    )

    args = parser.parse_args(args)

    if font is None:
        if args.font:
            font = ttLib.TTFont(args.font)
        else:
            font = MockFont()

    for f in args.inputs:
        log.debug("Processing %s", f)
        with open(f, "rt", encoding="utf-8-sig") as f:
            table = build(f, font, tableTag=args.tableTag)
        blob = table.compile(font)  # Make sure it compiles
        decompiled = table.__class__()
        decompiled.decompile(blob, font)  # Make sure it decompiles!

        # continue
        from fontTools.misc import xmlWriter

        tag = table.tableTag
        writer = xmlWriter.XMLWriter(sys.stdout)
        writer.begintag(tag)
        writer.newline()
        # table.toXML(writer, font)
        decompiled.toXML(writer, font)
        writer.endtag(tag)
        writer.newline()


def main(args):
    """Report font glyph shape geometricsl statistics"""

    if args is None:
        import sys

        args = sys.argv[1:]

    import argparse

    parser = argparse.ArgumentParser(
        "fonttools pens.statisticsPen",
        description="Report font glyph shape geometricsl statistics",
    )
    parser.add_argument("font", metavar="font.ttf", help="Font file.")
    parser.add_argument("glyphs", metavar="glyph-name", help="Glyph names.", nargs="*")
    parser.add_argument(
        "-y",
        metavar="<number>",
        help="Face index into a collection to open. Zero based.",
    )
    parser.add_argument(
        "-c",
        "--control",
        action="store_true",
        help="Use the control-box pen instead of the Green therem.",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Only report font-wide statistics."
    )
    parser.add_argument(
        "--variations",
        metavar="AXIS=LOC",
        default="",
        help="List of space separated locations. A location consist in "
        "the name of a variation axis, followed by '=' and a number. E.g.: "
        "wght=700 wdth=80. The default is the location of the base master.",
    )

    options = parser.parse_args(args)

    glyphs = options.glyphs
    fontNumber = int(options.y) if options.y is not None else 0

    location = {}
    for tag_v in options.variations.split():
        fields = tag_v.split("=")
        tag = fields[0].strip()
        v = int(fields[1])
        location[tag] = v

    from fontTools.ttLib import TTFont

    font = TTFont(options.font, fontNumber=fontNumber)
    if not glyphs:
        glyphs = font.getGlyphOrder()
    _test(
        font.getGlyphSet(location=location),
        font["head"].unitsPerEm,
        glyphs,
        quiet=options.quiet,
        control=options.control,
    )


def main(args=None):
    """Generate per-character SVG from font and text"""

    if args is None:
        import sys

        args = sys.argv[1:]

    from fontTools.ttLib import TTFont
    import argparse

    parser = argparse.ArgumentParser(
        "fonttools pens.svgPathPen", description="Generate SVG from text"
    )
    parser.add_argument("font", metavar="font.ttf", help="Font file.")
    parser.add_argument("text", metavar="text", nargs="?", help="Text string.")
    parser.add_argument(
        "-y",
        metavar="<number>",
        help="Face index into a collection to open. Zero based.",
    )
    parser.add_argument(
        "--glyphs",
        metavar="whitespace-separated list of glyph names",
        type=str,
        help="Glyphs to show. Exclusive with text option",
    )
    parser.add_argument(
        "--variations",
        metavar="AXIS=LOC",
        default="",
        help="List of space separated locations. A location consist in "
        "the name of a variation axis, followed by '=' and a number. E.g.: "
        "wght=700 wdth=80. The default is the location of the base master.",
    )

    options = parser.parse_args(args)

    fontNumber = int(options.y) if options.y is not None else 0

    font = TTFont(options.font, fontNumber=fontNumber)
    text = options.text
    glyphs = options.glyphs

    location = {}
    for tag_v in options.variations.split():
        fields = tag_v.split("=")
        tag = fields[0].strip()
        v = float(fields[1])
        location[tag] = v

    hhea = font["hhea"]
    ascent, descent = hhea.ascent, hhea.descent

    glyphset = font.getGlyphSet(location=location)
    cmap = font["cmap"].getBestCmap()

    if glyphs is not None and text is not None:
        raise ValueError("Options --glyphs and --text are exclusive")

    if glyphs is None:
        glyphs = " ".join(cmap[ord(u)] for u in text)

    glyphs = glyphs.split()

    s = ""
    width = 0
    for g in glyphs:
        glyph = glyphset[g]

        pen = SVGPathPen(glyphset)
        glyph.draw(pen)
        commands = pen.getCommands()

        s += '<g transform="translate(%d %d) scale(1 -1)"><path d="%s"/></g>\n' % (
            width,
            ascent,
            commands,
        )

        width += glyph.width

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print(
        '<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg">'
        % (width, ascent - descent)
    )
    print(s, end="")
    print("</svg>")


def main():
    run_benchmark("qu2cu", "quadratic_to_curves")


def main():
    from fontTools.cu2qu.benchmark import generate_curve
    from fontTools.cu2qu import curve_to_quadratic

    tolerance = 0.05
    reconstruct_tolerance = tolerance * 1
    curve = generate_curve()
    quadratics = curve_to_quadratic(curve, tolerance)
    print(
        "cu2qu tolerance %g. qu2cu tolerance %g." % (tolerance, reconstruct_tolerance)
    )
    print("One random cubic turned into %d quadratics." % len(quadratics))
    curves = quadratic_to_curves([quadratics], reconstruct_tolerance)
    print("Those quadratics turned back into %d cubics. " % len(curves))
    print("Original curve:", curve)
    print("Reconstructed curve(s):", curves)


def main(args=None):
    """OpenType font subsetter and optimizer"""
    from os.path import splitext
    from fontTools import configLogger

    if args is None:
        args = sys.argv[1:]

    if "--help" in args:
        print(__doc__)
        return 0

    options = Options()
    try:
        args = options.parse_opts(
            args,
            ignore_unknown=[
                "gids",
                "gids-file",
                "glyphs",
                "glyphs-file",
                "text",
                "text-file",
                "unicodes",
                "unicodes-file",
                "output-file",
            ],
        )
    except options.OptionError as e:
        usage()
        print("ERROR:", e, file=sys.stderr)
        return 2

    if len(args) < 2:
        usage()
        return 1

    configLogger(level=logging.INFO if options.verbose else logging.WARNING)
    if options.timing:
        timer.logger.setLevel(logging.DEBUG)
    else:
        timer.logger.disabled = True

    fontfile = args[0]
    args = args[1:]

    subsetter = Subsetter(options=options)
    outfile = None
    glyphs = []
    gids = []
    unicodes = []
    wildcard_glyphs = False
    wildcard_unicodes = False
    text = ""
    for g in args:
        if g == "*":
            wildcard_glyphs = True
            continue
        if g.startswith("--output-file="):
            outfile = g[14:]
            continue
        if g.startswith("--text="):
            text += g[7:]
            continue
        if g.startswith("--text-file="):
            with open(g[12:], encoding="utf-8-sig") as f:
                text += f.read().replace("\n", "")
            continue
        if g.startswith("--unicodes="):
            if g[11:] == "*":
                wildcard_unicodes = True
            else:
                unicodes.extend(parse_unicodes(g[11:]))
            continue
        if g.startswith("--unicodes-file="):
            with open(g[16:]) as f:
                for line in f.readlines():
                    unicodes.extend(parse_unicodes(line.split("#")[0]))
            continue
        if g.startswith("--gids="):
            gids.extend(parse_gids(g[7:]))
            continue
        if g.startswith("--gids-file="):
            with open(g[12:]) as f:
                for line in f.readlines():
                    gids.extend(parse_gids(line.split("#")[0]))
            continue
        if g.startswith("--glyphs="):
            if g[9:] == "*":
                wildcard_glyphs = True
            else:
                glyphs.extend(parse_glyphs(g[9:]))
            continue
        if g.startswith("--glyphs-file="):
            with open(g[14:]) as f:
                for line in f.readlines():
                    glyphs.extend(parse_glyphs(line.split("#")[0]))
            continue
        glyphs.append(g)

    dontLoadGlyphNames = not options.glyph_names and not glyphs
    lazy = options.lazy
    font = load_font(
        fontfile, options, dontLoadGlyphNames=dontLoadGlyphNames, lazy=lazy
    )

    if outfile is None:
        ext = "." + options.flavor.lower() if options.flavor is not None else None
        outfile = makeOutputFileName(
            fontfile, extension=ext, overWrite=True, suffix=".subset"
        )

    with timer("compile glyph list"):
        if wildcard_glyphs:
            glyphs.extend(font.getGlyphOrder())
        if wildcard_unicodes:
            for t in font["cmap"].tables:
                if t.isUnicode():
                    unicodes.extend(t.cmap.keys())
                    if t.format == 14:
                        unicodes.extend(t.uvsDict.keys())
        assert "" not in glyphs

    log.info("Text: '%s'" % text)
    log.info("Unicodes: %s", unicodes)
    log.info("Glyphs: %s", glyphs)
    log.info("Gids: %s", gids)

    subsetter.populate(glyphs=glyphs, gids=gids, unicodes=unicodes, text=text)
    subsetter.subset(font)

    save_font(font, outfile, options)

    if options.verbose:
        import os

        log.info("Input font:% 7d bytes: %s" % (os.path.getsize(fontfile), fontfile))
        log.info("Subset font:% 7d bytes: %s" % (os.path.getsize(outfile), outfile))

    if options.xml:
        font.saveXML(sys.stdout)

    font.close()


def main(args=None):
    """Simplify glyphs in TTFont by merging overlapping contours."""

    import argparse

    parser = argparse.ArgumentParser(
        "fonttools ttLib.removeOverlaps", description=__doc__
    )

    parser.add_argument("input", metavar="INPUT.ttf", help="Input font file")
    parser.add_argument("output", metavar="OUTPUT.ttf", help="Output font file")
    parser.add_argument(
        "glyphs",
        metavar="GLYPHS",
        nargs="*",
        help="Optional list of glyph names to remove overlaps from",
    )
    parser.add_argument(
        "--keep-hinting",
        action="store_true",
        help="Keep hinting for unmodified glyphs, default is to drop hinting",
    )
    parser.add_argument(
        "--ignore-errors",
        action="store_true",
        help="ignore errors while removing overlaps, "
        "thus keeping the tricky glyphs unchanged",
    )
    parser.add_argument(
        "--keep-unused-subroutines",
        action="store_true",
        help="Keep unused subroutines in CFF table after removing overlaps, "
        "default is to remove them if any glyphs are modified",
    )
    args = parser.parse_args(args)

    with ttFont.TTFont(args.input) as font:
        removeOverlaps(
            font=font,
            glyphNames=args.glyphs or None,
            removeHinting=not args.keep_hinting,
            ignoreErrors=args.ignore_errors,
            removeUnusedSubroutines=not args.keep_unused_subroutines,
        )
        font.save(args.output)


def main(args=None):
    """Change the units-per-EM of fonts"""

    if args is None:
        import sys

        args = sys.argv[1:]

    from fontTools.ttLib import TTFont
    from fontTools.misc.cliTools import makeOutputFileName
    import argparse

    parser = argparse.ArgumentParser(
        "fonttools ttLib.scaleUpem", description="Change the units-per-EM of fonts"
    )
    parser.add_argument("font", metavar="font", help="Font file.")
    parser.add_argument(
        "new_upem", metavar="new-upem", help="New units-per-EM integer value."
    )
    parser.add_argument(
        "--output-file", metavar="path", default=None, help="Output file."
    )

    options = parser.parse_args(args)

    font = TTFont(options.font)
    new_upem = int(options.new_upem)
    output_file = (
        options.output_file
        if options.output_file is not None
        else makeOutputFileName(options.font, overWrite=True, suffix="-scaled")
    )

    scale_upem(font, new_upem)

    print("Writing %s" % output_file)
    font.save(output_file)


def main(args=None):
    """Compress and decompress WOFF2 fonts"""
    import argparse
    from fontTools import configLogger
    from fontTools.ttx import makeOutputFileName

    class _HelpAction(argparse._HelpAction):
        def __call__(self, parser, namespace, values, option_string=None):
            subparsers_actions = [
                action
                for action in parser._actions
                if isinstance(action, argparse._SubParsersAction)
            ]
            for subparsers_action in subparsers_actions:
                for choice, subparser in subparsers_action.choices.items():
                    print(subparser.format_help())
            parser.exit()

    class _NoGlyfTransformAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            namespace.transform_tables.difference_update({"glyf", "loca"})

    class _HmtxTransformAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            namespace.transform_tables.add("hmtx")

    parser = argparse.ArgumentParser(
        prog="fonttools ttLib.woff2", description=main.__doc__, add_help=False
    )

    parser.add_argument(
        "-h", "--help", action=_HelpAction, help="show this help message and exit"
    )

    parser_group = parser.add_subparsers(title="sub-commands")
    parser_compress = parser_group.add_parser(
        "compress", description="Compress a TTF or OTF font to WOFF2"
    )
    parser_decompress = parser_group.add_parser(
        "decompress", description="Decompress a WOFF2 font to OTF"
    )

    for subparser in (parser_compress, parser_decompress):
        group = subparser.add_mutually_exclusive_group(required=False)
        group.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="print more messages to console",
        )
        group.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="do not print messages to console",
        )

    parser_compress.add_argument(
        "input_file",
        metavar="INPUT",
        help="the input OpenType font (.ttf or .otf)",
    )
    parser_decompress.add_argument(
        "input_file",
        metavar="INPUT",
        help="the input WOFF2 font",
    )

    parser_compress.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT",
        help="the output WOFF2 font",
    )
    parser_decompress.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT",
        help="the output OpenType font",
    )

    transform_group = parser_compress.add_argument_group()
    transform_group.add_argument(
        "--no-glyf-transform",
        dest="transform_tables",
        nargs=0,
        action=_NoGlyfTransformAction,
        help="Do not transform glyf (and loca) tables",
    )
    transform_group.add_argument(
        "--hmtx-transform",
        dest="transform_tables",
        nargs=0,
        action=_HmtxTransformAction,
        help="Enable optional transformation for 'hmtx' table",
    )

    parser_compress.set_defaults(
        subcommand=compress,
        transform_tables={"glyf", "loca"},
    )
    parser_decompress.set_defaults(subcommand=decompress)

    options = vars(parser.parse_args(args))

    subcommand = options.pop("subcommand", None)
    if not subcommand:
        parser.print_help()
        return

    quiet = options.pop("quiet")
    verbose = options.pop("verbose")
    configLogger(
        level=("ERROR" if quiet else "DEBUG" if verbose else "INFO"),
    )

    if not options["output_file"]:
        if subcommand is compress:
            extension = ".woff2"
        elif subcommand is decompress:
            # choose .ttf/.otf file extension depending on sfntVersion
            with open(options["input_file"], "rb") as f:
                f.seek(4)  # skip 'wOF2' signature
                sfntVersion = f.read(4)
            assert len(sfntVersion) == 4, "not enough data"
            extension = ".otf" if sfntVersion == b"OTTO" else ".ttf"
        else:
            raise AssertionError(subcommand)
        options["output_file"] = makeOutputFileName(
            options["input_file"], outputDir=None, extension=extension
        )

    try:
        subcommand(**options)
    except TTLibError as e:
        parser.error(e)


def main(args=None):
    """Open/save fonts with TTFont() or TTCollection()

      ./fonttools ttLib [-oFILE] [-yNUMBER] files...

    If multiple files are given on the command-line,
    they are each opened (as a font or collection),
    and added to the font list.

    If -o (output-file) argument is given, the font
    list is then saved to the output file, either as
    a single font, if there is only one font, or as
    a collection otherwise.

    If -y (font-number) argument is given, only the
    specified font from collections is opened.

    The above allow extracting a single font from a
    collection, or combining multiple fonts into a
    collection.

    If --lazy or --no-lazy are give, those are passed
    to the TTFont() or TTCollection() constructors.
    """
    from fontTools import configLogger

    if args is None:
        args = sys.argv[1:]

    import argparse

    parser = argparse.ArgumentParser(
        "fonttools ttLib",
        description="Open/save fonts with TTFont() or TTCollection()",
        epilog="""
		If multiple files are given on the command-line,
		they are each opened (as a font or collection),
		and added to the font list.

		The above, when combined with -o / --output,
		allows for extracting a single font from a
		collection, or combining multiple fonts into a
		collection.
		""",
    )
    parser.add_argument("font", metavar="font", nargs="*", help="Font file.")
    parser.add_argument(
        "-t", "--table", metavar="table", action="append", help="Tables to decompile."
    )
    parser.add_argument(
        "-o", "--output", metavar="FILE", default=None, help="Output file."
    )
    parser.add_argument(
        "-y", metavar="NUMBER", default=-1, help="Font number to load from collections."
    )
    parser.add_argument(
        "--lazy", action="store_true", default=None, help="Load fonts lazily."
    )
    parser.add_argument(
        "--no-lazy", dest="lazy", action="store_false", help="Load fonts immediately."
    )
    parser.add_argument(
        "--flavor",
        dest="flavor",
        default=None,
        help="Flavor of output font. 'woff' or 'woff2'.",
    )
    parser.add_argument(
        "--no-recalc-timestamp",
        dest="recalcTimestamp",
        action="store_false",
        help="Keep the original font 'modified' timestamp.",
    )
    parser.add_argument(
        "-b",
        dest="recalcBBoxes",
        action="store_false",
        help="Don't recalc glyph bounding boxes: use the values in the original font.",
    )
    parser.add_argument(
        "--optimize-font-speed",
        action="store_true",
        help=(
            "Enable optimizations that prioritize speed over file size. This "
            "mainly affects how glyf table and gvar / VARC tables are compiled."
        ),
    )
    options = parser.parse_args(args)

    fontNumber = int(options.y) if options.y is not None else None
    outFile = options.output
    lazy = options.lazy
    flavor = options.flavor
    tables = options.table
    recalcBBoxes = options.recalcBBoxes
    recalcTimestamp = options.recalcTimestamp
    optimizeFontSpeed = options.optimize_font_speed

    fonts = []
    for f in options.font:
        try:
            font = TTFont(
                f,
                recalcBBoxes=recalcBBoxes,
                recalcTimestamp=recalcTimestamp,
                fontNumber=fontNumber,
                lazy=lazy,
            )
            if optimizeFontSpeed:
                font.cfg[OPTIMIZE_FONT_SPEED] = optimizeFontSpeed
            fonts.append(font)
        except TTLibFileIsCollectionError:
            collection = TTCollection(f, lazy=lazy)
            fonts.extend(collection.fonts)

    if tables is None:
        if lazy is False:
            tables = ["*"]
        elif optimizeFontSpeed:
            tables = {"glyf", "gvar", "VARC"}.intersection(font.keys())
        else:
            tables = []
    for font in fonts:
        if "GlyphOrder" in tables:
            font.getGlyphOrder()
        for table in tables if "*" not in tables else font.keys():
            font[table]  # Decompiles

    if outFile is not None:
        if len(fonts) == 1:
            fonts[0].flavor = flavor
            fonts[0].save(outFile)
        else:
            if flavor is not None:
                raise TTLibError("Cannot set flavor for collections.")
            collection = TTCollection()
            collection.fonts = fonts
            collection.save(outFile)


def main(args=None):
    from .avar.plan import main

    main(args)


def main(args=None):
    """Add `HVAR` table to variable font."""

    if args is None:
        import sys

        args = sys.argv[1:]

    from fontTools import configLogger
    from fontTools.designspaceLib import DesignSpaceDocument
    import argparse

    parser = argparse.ArgumentParser(
        "fonttools varLib.hvar",
        description="Add `HVAR` table from to variable font.",
    )
    parser.add_argument("font", metavar="varfont.ttf", help="Variable-font file.")
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="Output font file name.",
    )

    options = parser.parse_args(args)

    configLogger(level="WARNING")

    font = TTFont(options.font)
    if not "fvar" in font:
        log.error("Not a variable font.")
        return 1

    add_HVAR(font)
    if "vmtx" in font:
        add_VVAR(font)

    if options.output_file is None:
        outfile = makeOutputFileName(options.font, overWrite=True, suffix=".hvar")
    else:
        outfile = options.output_file
    if outfile:
        log.info("Saving %s", outfile)
        font.save(outfile)


def main(args=None):
    """Test for interpolatability issues between fonts"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        "fonttools varLib.interpolatable",
        description=main.__doc__,
    )
    parser.add_argument(
        "--glyphs",
        action="store",
        help="Space-separate name of glyphs to check",
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Show all glyph pairs, even if no problems are found",
    )
    parser.add_argument(
        "--tolerance",
        action="store",
        type=float,
        help="Error tolerance. Between 0 and 1. Default %s" % DEFAULT_TOLERANCE,
    )
    parser.add_argument(
        "--kinkiness",
        action="store",
        type=float,
        help="How aggressively report kinks. Default %s" % DEFAULT_KINKINESS,
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output report in JSON format",
    )
    parser.add_argument(
        "--pdf",
        action="store",
        help="Output report in PDF format",
    )
    parser.add_argument(
        "--ps",
        action="store",
        help="Output report in PostScript format",
    )
    parser.add_argument(
        "--html",
        action="store",
        help="Output report in HTML format",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only exit with code 1 or 0, no output",
    )
    parser.add_argument(
        "--output",
        action="store",
        help="Output file for the problem report; Default: stdout",
    )
    parser.add_argument(
        "--ignore-missing",
        action="store_true",
        help="Will not report glyphs missing from sparse masters as errors",
    )
    parser.add_argument(
        "inputs",
        metavar="FILE",
        type=str,
        nargs="+",
        help="Input a single variable font / DesignSpace / Glyphs file, or multiple TTF/UFO files",
    )
    parser.add_argument(
        "--name",
        metavar="NAME",
        type=str,
        action="append",
        help="Name of the master to use in the report. If not provided, all are used.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Run verbosely.")
    parser.add_argument("--debug", action="store_true", help="Run with debug output.")

    args = parser.parse_args(args)

    from fontTools import configLogger

    configLogger(level=("INFO" if args.verbose else "WARNING"))
    if args.debug:
        configLogger(level="DEBUG")

    glyphs = args.glyphs.split() if args.glyphs else None

    from os.path import basename

    fonts = []
    names = []
    locations = []
    discrete_axes = set()
    upem = DEFAULT_UPEM

    original_args_inputs = tuple(args.inputs)

    if len(args.inputs) == 1:
        designspace = None
        if args.inputs[0].endswith(".designspace"):
            from fontTools.designspaceLib import DesignSpaceDocument

            designspace = DesignSpaceDocument.fromfile(args.inputs[0])
            args.inputs = [master.path for master in designspace.sources]
            locations = [master.location for master in designspace.sources]
            discrete_axes = {
                a.name for a in designspace.axes if not hasattr(a, "minimum")
            }
            axis_triples = {
                a.name: (a.minimum, a.default, a.maximum)
                for a in designspace.axes
                if a.name not in discrete_axes
            }
            axis_mappings = {a.name: a.map for a in designspace.axes}
            axis_triples = {
                k: tuple(piecewiseLinearMap(v, dict(axis_mappings[k])) for v in vv)
                for k, vv in axis_triples.items()
            }

        elif args.inputs[0].endswith((".glyphs", ".glyphspackage")):
            from glyphsLib import GSFont, to_designspace

            gsfont = GSFont(args.inputs[0])
            upem = gsfont.upm
            designspace = to_designspace(gsfont)
            fonts = [source.font for source in designspace.sources]
            names = ["%s-%s" % (f.info.familyName, f.info.styleName) for f in fonts]
            args.inputs = []
            locations = [master.location for master in designspace.sources]
            axis_triples = {
                a.name: (a.minimum, a.default, a.maximum) for a in designspace.axes
            }
            axis_mappings = {a.name: a.map for a in designspace.axes}
            axis_triples = {
                k: tuple(piecewiseLinearMap(v, dict(axis_mappings[k])) for v in vv)
                for k, vv in axis_triples.items()
            }

        elif args.inputs[0].endswith(".ttf") or args.inputs[0].endswith(".otf"):
            from fontTools.ttLib import TTFont

            # Is variable font?

            font = TTFont(args.inputs[0])
            upem = font["head"].unitsPerEm

            fvar = font["fvar"]
            axisMapping = {}
            for axis in fvar.axes:
                axisMapping[axis.axisTag] = {
                    -1: axis.minValue,
                    0: axis.defaultValue,
                    1: axis.maxValue,
                }
            normalized = False
            if "avar" in font:
                avar = font["avar"]
                if getattr(avar.table, "VarStore", None):
                    axisMapping = {tag: {-1: -1, 0: 0, 1: 1} for tag in axisMapping}
                    normalized = True
                else:
                    for axisTag, segments in avar.segments.items():
                        fvarMapping = axisMapping[axisTag].copy()
                        for location, value in segments.items():
                            axisMapping[axisTag][value] = piecewiseLinearMap(
                                location, fvarMapping
                            )

            # Gather all glyphs at their "master" locations
            ttGlyphSets = {}
            glyphsets = defaultdict(dict)

            if "gvar" in font:
                gvar = font["gvar"]
                glyf = font["glyf"]

                if glyphs is None:
                    glyphs = sorted(gvar.variations.keys())
                for glyphname in glyphs:
                    for var in gvar.variations[glyphname]:
                        locDict = {}
                        loc = []
                        for tag, val in sorted(var.axes.items()):
                            locDict[tag] = val[1]
                            loc.append((tag, val[1]))

                        locTuple = tuple(loc)
                        if locTuple not in ttGlyphSets:
                            ttGlyphSets[locTuple] = font.getGlyphSet(
                                location=locDict, normalized=True, recalcBounds=False
                            )

                        recursivelyAddGlyph(
                            glyphname, glyphsets[locTuple], ttGlyphSets[locTuple], glyf
                        )

            elif "CFF2" in font:
                fvarAxes = font["fvar"].axes
                cff2 = font["CFF2"].cff.topDictIndex[0]
                charstrings = cff2.CharStrings

                if glyphs is None:
                    glyphs = sorted(charstrings.keys())
                for glyphname in glyphs:
                    cs = charstrings[glyphname]
                    private = cs.private

                    # Extract vsindex for the glyph
                    vsindices = {getattr(private, "vsindex", 0)}
                    vsindex = getattr(private, "vsindex", 0)
                    last_op = 0
                    # The spec says vsindex can only appear once and must be the first
                    # operator in the charstring, but we support multiple.
                    # https://github.com/harfbuzz/boring-expansion-spec/issues/158
                    for op in cs.program:
                        if op == "blend":
                            vsindices.add(vsindex)
                        elif op == "vsindex":
                            assert isinstance(last_op, int)
                            vsindex = last_op
                        last_op = op

                    if not hasattr(private, "vstore"):
                        continue

                    varStore = private.vstore.otVarStore
                    for vsindex in vsindices:
                        varData = varStore.VarData[vsindex]
                        for regionIndex in varData.VarRegionIndex:
                            region = varStore.VarRegionList.Region[regionIndex]

                            locDict = {}
                            loc = []
                            for axisIndex, axis in enumerate(region.VarRegionAxis):
                                tag = fvarAxes[axisIndex].axisTag
                                val = axis.PeakCoord
                                locDict[tag] = val
                                loc.append((tag, val))

                            locTuple = tuple(loc)
                            if locTuple not in ttGlyphSets:
                                ttGlyphSets[locTuple] = font.getGlyphSet(
                                    location=locDict,
                                    normalized=True,
                                    recalcBounds=False,
                                )

                            glyphset = glyphsets[locTuple]
                            glyphset[glyphname] = ttGlyphSets[locTuple][glyphname]

            names = ["''"]
            fonts = [font.getGlyphSet()]
            locations = [{}]
            axis_triples = {a: (-1, 0, +1) for a in sorted(axisMapping.keys())}
            for locTuple in sorted(glyphsets.keys(), key=lambda v: (len(v), v)):
                name = (
                    "'"
                    + " ".join(
                        "%s=%s"
                        % (
                            k,
                            floatToFixedToStr(
                                piecewiseLinearMap(v, axisMapping[k]), 14
                            ),
                        )
                        for k, v in locTuple
                    )
                    + "'"
                )
                if normalized:
                    name += " (normalized)"
                names.append(name)
                fonts.append(glyphsets[locTuple])
                locations.append(dict(locTuple))

            args.ignore_missing = True
            args.inputs = []

    if not locations:
        locations = [{} for _ in fonts]

    for filename in args.inputs:
        if filename.endswith(".ufo"):
            from fontTools.ufoLib import UFOReader

            font = UFOReader(filename)
            info = SimpleNamespace()
            font.readInfo(info)
            upem = info.unitsPerEm
            fonts.append(font)
        else:
            from fontTools.ttLib import TTFont

            font = TTFont(filename)
            upem = font["head"].unitsPerEm
            fonts.append(font)

        names.append(basename(filename).rsplit(".", 1)[0])

    if len(fonts) < 2:
        log.warning("Font file does not seem to be variable. Nothing to check.")
        return

    glyphsets = []
    for font in fonts:
        if hasattr(font, "getGlyphSet"):
            glyphset = font.getGlyphSet()
        else:
            glyphset = font
        glyphsets.append({k: glyphset[k] for k in glyphset.keys()})

    if args.name:
        accepted_names = set(args.name)
        glyphsets = [
            glyphset
            for name, glyphset in zip(names, glyphsets)
            if name in accepted_names
        ]
        locations = [
            location
            for name, location in zip(names, locations)
            if name in accepted_names
        ]
        names = [name for name in names if name in accepted_names]

    if not glyphs:
        glyphs = sorted(set([gn for glyphset in glyphsets for gn in glyphset.keys()]))

    glyphsSet = set(glyphs)
    for glyphset in glyphsets:
        glyphSetGlyphNames = set(glyphset.keys())
        diff = glyphsSet - glyphSetGlyphNames
        if diff:
            for gn in diff:
                glyphset[gn] = None

    # Normalize locations
    locations = [
        {
            **normalizeLocation(loc, axis_triples),
            **{k: v for k, v in loc.items() if k in discrete_axes},
        }
        for loc in locations
    ]
    tolerance = args.tolerance or DEFAULT_TOLERANCE
    kinkiness = args.kinkiness if args.kinkiness is not None else DEFAULT_KINKINESS

    try:
        log.info("Running on %d glyphsets", len(glyphsets))
        log.info("Locations: %s", pformat(locations))
        problems_gen = test_gen(
            glyphsets,
            glyphs=glyphs,
            names=names,
            locations=locations,
            upem=upem,
            ignore_missing=args.ignore_missing,
            tolerance=tolerance,
            kinkiness=kinkiness,
            show_all=args.show_all,
            discrete_axes=discrete_axes,
        )
        problems = defaultdict(list)

        f = (
            sys.stdout
            if args.output is None
            else open(ensure_parent_dir(args.output), "w")
        )

        if not args.quiet:
            if args.json:
                import json

                for glyphname, problem in problems_gen:
                    problems[glyphname].append(problem)

                print(json.dumps(problems), file=f)
            else:
                last_glyphname = None
                for glyphname, p in problems_gen:
                    problems[glyphname].append(p)

                    if glyphname != last_glyphname:
                        print(f"Glyph {glyphname} was not compatible:", file=f)
                        last_glyphname = glyphname
                        last_master_idxs = None

                    master_idxs = (
                        (p["master_idx"],)
                        if "master_idx" in p
                        else (p["master_1_idx"], p["master_2_idx"])
                    )
                    if master_idxs != last_master_idxs:
                        master_names = (
                            (p["master"],)
                            if "master" in p
                            else (p["master_1"], p["master_2"])
                        )
                        print(f"  Masters: %s:" % ", ".join(master_names), file=f)
                        last_master_idxs = master_idxs

                    if p["type"] == InterpolatableProblem.MISSING:
                        print(
                            "    Glyph was missing in master %s" % p["master"], file=f
                        )
                    elif p["type"] == InterpolatableProblem.OPEN_PATH:
                        print(
                            "    Glyph has an open path in master %s" % p["master"],
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.PATH_COUNT:
                        print(
                            "    Path count differs: %i in %s, %i in %s"
                            % (
                                p["value_1"],
                                p["master_1"],
                                p["value_2"],
                                p["master_2"],
                            ),
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.NODE_COUNT:
                        print(
                            "    Node count differs in path %i: %i in %s, %i in %s"
                            % (
                                p["path"],
                                p["value_1"],
                                p["master_1"],
                                p["value_2"],
                                p["master_2"],
                            ),
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.NODE_INCOMPATIBILITY:
                        print(
                            "    Node %d incompatible in path %i: %s in %s, %s in %s"
                            % (
                                p["node"],
                                p["path"],
                                p["value_1"],
                                p["master_1"],
                                p["value_2"],
                                p["master_2"],
                            ),
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.CONTOUR_ORDER:
                        print(
                            "    Contour order differs: %s in %s, %s in %s"
                            % (
                                p["value_1"],
                                p["master_1"],
                                p["value_2"],
                                p["master_2"],
                            ),
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.WRONG_START_POINT:
                        print(
                            "    Contour %d start point differs: %s in %s, %s in %s; reversed: %s"
                            % (
                                p["contour"],
                                p["value_1"],
                                p["master_1"],
                                p["value_2"],
                                p["master_2"],
                                p["reversed"],
                            ),
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.UNDERWEIGHT:
                        print(
                            "    Contour %d interpolation is underweight: %s, %s"
                            % (
                                p["contour"],
                                p["master_1"],
                                p["master_2"],
                            ),
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.OVERWEIGHT:
                        print(
                            "    Contour %d interpolation is overweight: %s, %s"
                            % (
                                p["contour"],
                                p["master_1"],
                                p["master_2"],
                            ),
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.KINK:
                        print(
                            "    Contour %d has a kink at %s: %s, %s"
                            % (
                                p["contour"],
                                p["value"],
                                p["master_1"],
                                p["master_2"],
                            ),
                            file=f,
                        )
                    elif p["type"] == InterpolatableProblem.NOTHING:
                        print(
                            "    Showing %s and %s"
                            % (
                                p["master_1"],
                                p["master_2"],
                            ),
                            file=f,
                        )
        else:
            for glyphname, problem in problems_gen:
                problems[glyphname].append(problem)

        problems = sort_problems(problems)

        for p in "ps", "pdf":
            arg = getattr(args, p)
            if arg is None:
                continue
            log.info("Writing %s to %s", p.upper(), arg)
            from .interpolatablePlot import InterpolatablePS, InterpolatablePDF

            PlotterClass = InterpolatablePS if p == "ps" else InterpolatablePDF

            with PlotterClass(
                ensure_parent_dir(arg), glyphsets=glyphsets, names=names
            ) as doc:
                doc.add_title_page(
                    original_args_inputs, tolerance=tolerance, kinkiness=kinkiness
                )
                if problems:
                    doc.add_summary(problems)
                doc.add_problems(problems)
                if not problems and not args.quiet:
                    doc.draw_cupcake()
                if problems:
                    doc.add_index()
                    doc.add_table_of_contents()

        if args.html:
            log.info("Writing HTML to %s", args.html)
            from .interpolatablePlot import InterpolatableSVG

            svgs = []
            glyph_starts = {}
            with InterpolatableSVG(svgs, glyphsets=glyphsets, names=names) as svg:
                svg.add_title_page(
                    original_args_inputs,
                    show_tolerance=False,
                    tolerance=tolerance,
                    kinkiness=kinkiness,
                )
                for glyph, glyph_problems in problems.items():
                    glyph_starts[len(svgs)] = glyph
                    svg.add_problems(
                        {glyph: glyph_problems},
                        show_tolerance=False,
                        show_page_number=False,
                    )
                if not problems and not args.quiet:
                    svg.draw_cupcake()

            import base64

            with open(ensure_parent_dir(args.html), "wb") as f:
                f.write(b"<!DOCTYPE html>\n")
                f.write(
                    b'<html><body align="center" style="font-family: sans-serif; text-color: #222">\n'
                )
                f.write(b"<title>fonttools varLib.interpolatable report</title>\n")
                for i, svg in enumerate(svgs):
                    if i in glyph_starts:
                        f.write(f"<h1>Glyph {glyph_starts[i]}</h1>\n".encode("utf-8"))
                    f.write("<img src='data:image/svg+xml;base64,".encode("utf-8"))
                    f.write(base64.b64encode(svg))
                    f.write(b"' />\n")
                    f.write(b"<hr>\n")
                f.write(b"</body></html>\n")

    except Exception as e:
        e.args += original_args_inputs
        log.error(e)
        raise

    if problems:
        return problems


def main(args=None):
    """Interpolate GDEF/GPOS/GSUB tables for a point on a designspace"""
    from fontTools import configLogger
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        "fonttools varLib.interpolate_layout",
        description=main.__doc__,
    )
    parser.add_argument(
        "designspace_filename", metavar="DESIGNSPACE", help="Input TTF files"
    )
    parser.add_argument(
        "locations",
        metavar="LOCATION",
        type=str,
        nargs="+",
        help="Axis locations (e.g. wdth=120",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT",
        help="Output font file (defaults to <designspacename>-instance.ttf)",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        metavar="LEVEL",
        default="INFO",
        help="Logging level (defaults to INFO)",
    )

    args = parser.parse_args(args)

    if not args.output:
        args.output = os.path.splitext(args.designspace_filename)[0] + "-instance.ttf"

    configLogger(level=args.loglevel)

    finder = lambda s: s.replace("master_ufo", "master_ttf_interpolatable").replace(
        ".ufo", ".ttf"
    )

    loc = {}
    for arg in args.locations:
        tag, val = arg.split("=")
        loc[tag] = float(val)

    font = interpolate_layout(args.designspace_filename, loc, finder)
    log.info("Saving font %s", args.output)
    font.save(args.output)


def main(args=None):
    """Normalize locations on a given designspace"""
    from fontTools import configLogger
    import argparse

    parser = argparse.ArgumentParser(
        "fonttools varLib.models",
        description=main.__doc__,
    )
    parser.add_argument(
        "--loglevel",
        metavar="LEVEL",
        default="INFO",
        help="Logging level (defaults to INFO)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--designspace", metavar="DESIGNSPACE", type=str)
    group.add_argument(
        "-l",
        "--locations",
        metavar="LOCATION",
        nargs="+",
        help="Master locations as comma-separate coordinates. One must be all zeros.",
    )

    args = parser.parse_args(args)

    configLogger(level=args.loglevel)
    from pprint import pprint

    if args.designspace:
        from fontTools.designspaceLib import DesignSpaceDocument

        doc = DesignSpaceDocument()
        doc.read(args.designspace)
        locs = [s.location for s in doc.sources]
        print("Original locations:")
        pprint(locs)
        doc.normalize()
        print("Normalized locations:")
        locs = [s.location for s in doc.sources]
        pprint(locs)
    else:
        axes = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
        locs = [
            dict(zip(axes, (float(v) for v in s.split(",")))) for s in args.locations
        ]

    model = VariationModel(locs)
    print("Sorted locations:")
    pprint(model.locations)
    print("Supports:")
    pprint(model.supports)


def main(args=None):
    """Instantiate a variation font"""
    from fontTools import configLogger
    import argparse

    parser = argparse.ArgumentParser(
        "fonttools varLib.mutator", description="Instantiate a variable font"
    )
    parser.add_argument("input", metavar="INPUT.ttf", help="Input variable TTF file.")
    parser.add_argument(
        "locargs",
        metavar="AXIS=LOC",
        nargs="*",
        help="List of space separated locations. A location consist in "
        "the name of a variation axis, followed by '=' and a number. E.g.: "
        " wght=700 wdth=80. The default is the location of the base master.",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT.ttf",
        default=None,
        help="Output instance TTF file (default: INPUT-instance.ttf).",
    )
    parser.add_argument(
        "--no-recalc-timestamp",
        dest="recalc_timestamp",
        action="store_false",
        help="Don't set the output font's timestamp to the current time.",
    )
    logging_group = parser.add_mutually_exclusive_group(required=False)
    logging_group.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )
    logging_group.add_argument(
        "-q", "--quiet", action="store_true", help="Turn verbosity off."
    )
    parser.add_argument(
        "--no-overlap",
        dest="overlap",
        action="store_false",
        help="Don't set OVERLAP_SIMPLE/OVERLAP_COMPOUND glyf flags.",
    )
    options = parser.parse_args(args)

    varfilename = options.input
    outfile = (
        os.path.splitext(varfilename)[0] + "-instance.ttf"
        if not options.output
        else options.output
    )
    configLogger(
        level=("DEBUG" if options.verbose else "ERROR" if options.quiet else "INFO")
    )

    loc = {}
    for arg in options.locargs:
        try:
            tag, val = arg.split("=")
            assert len(tag) <= 4
            loc[tag.ljust(4)] = float(val)
        except (ValueError, AssertionError):
            parser.error("invalid location argument format: %r" % arg)
    log.info("Location: %s", loc)

    log.info("Loading variable font")
    varfont = TTFont(varfilename, recalcTimestamp=options.recalc_timestamp)

    instantiateVariableFont(varfont, loc, inplace=True, overlap=options.overlap)

    log.info("Saving instance font %s", outfile)
    varfont.save(outfile)


def main(args=None):
    from fontTools import configLogger

    if args is None:
        args = sys.argv[1:]

    # configure the library logger (for >= WARNING)
    configLogger()
    # comment this out to enable debug messages from logger
    # log.setLevel(logging.DEBUG)

    if len(args) < 1:
        print("usage: fonttools varLib.plot source.designspace", file=sys.stderr)
        print("  or")
        print("usage: fonttools varLib.plot location1 location2 ...", file=sys.stderr)
        print("  or")
        print(
            "usage: fonttools varLib.plot location1=value1 location2=value2 ...",
            file=sys.stderr,
        )
        sys.exit(1)

    fig = pyplot.figure()
    fig.set_tight_layout(True)

    if len(args) == 1 and args[0].endswith(".designspace"):
        doc = DesignSpaceDocument()
        doc.read(args[0])
        plotDocument(doc, fig)
    else:
        axes = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
        if "=" not in args[0]:
            locs = [dict(zip(axes, (float(v) for v in s.split(",")))) for s in args]
            plotLocations(locs, fig)
        else:
            locations = []
            masterValues = []
            for arg in args:
                loc, v = arg.split("=")
                locations.append(dict(zip(axes, (float(v) for v in loc.split(",")))))
                masterValues.append(float(v))
            model = VariationModel(locations, axes[: len(locations[0])])
            plotModelFromMasters(model, masterValues, fig)

    pyplot.show()


def main(args=None):
    """Optimize a font's GDEF variation store"""
    from argparse import ArgumentParser
    from fontTools import configLogger
    from fontTools.ttLib import TTFont
    from fontTools.ttLib.tables.otBase import OTTableWriter

    parser = ArgumentParser(prog="varLib.varStore", description=main.__doc__)
    parser.add_argument("--quantization", type=int, default=1)
    parser.add_argument("fontfile")
    parser.add_argument("outfile", nargs="?")
    options = parser.parse_args(args)

    # TODO: allow user to configure logging via command-line options
    configLogger(level="INFO")

    quantization = options.quantization
    fontfile = options.fontfile
    outfile = options.outfile

    font = TTFont(fontfile)
    gdef = font["GDEF"]
    store = gdef.table.VarStore

    writer = OTTableWriter()
    store.compile(writer, font)
    size = len(writer.getAllData())
    print("Before: %7d bytes" % size)

    varidx_map = store.optimize(quantization=quantization)

    writer = OTTableWriter()
    store.compile(writer, font)
    size = len(writer.getAllData())
    print("After:  %7d bytes" % size)

    if outfile is not None:
        gdef.table.remap_device_varidxes(varidx_map)
        if "GPOS" in font:
            font["GPOS"].table.remap_device_varidxes(varidx_map)

        font.save(outfile)


def main(args=None):
    """Build variable fonts from a designspace file and masters"""
    from argparse import ArgumentParser
    from fontTools import configLogger

    parser = ArgumentParser(prog="varLib", description=main.__doc__)
    parser.add_argument("designspace")
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-o", metavar="OUTPUTFILE", dest="outfile", default=None, help="output file"
    )
    output_group.add_argument(
        "-d",
        "--output-dir",
        metavar="OUTPUTDIR",
        default=None,
        help="output dir (default: same as input designspace file)",
    )
    parser.add_argument(
        "-x",
        metavar="TAG",
        dest="exclude",
        action="append",
        default=[],
        help="exclude table",
    )
    parser.add_argument(
        "--disable-iup",
        dest="optimize",
        action="store_false",
        help="do not perform IUP optimization",
    )
    parser.add_argument(
        "--no-colr-layer-reuse",
        dest="colr_layer_reuse",
        action="store_false",
        help="do not rebuild variable COLR table to optimize COLR layer reuse",
    )
    parser.add_argument(
        "--drop-implied-oncurves",
        action="store_true",
        help=(
            "drop on-curve points that can be implied when exactly in the middle of "
            "two off-curve points (only applies to TrueType fonts)"
        ),
    )
    parser.add_argument(
        "--master-finder",
        default="master_ttf_interpolatable/{stem}.ttf",
        help=(
            "templated string used for finding binary font "
            "files given the source file names defined in the "
            "designspace document. The following special strings "
            "are defined: {fullname} is the absolute source file "
            "name; {basename} is the file name without its "
            "directory; {stem} is the basename without the file "
            "extension; {ext} is the source file extension; "
            "{dirname} is the directory of the absolute file "
            'name. The default value is "%(default)s".'
        ),
    )
    parser.add_argument(
        "--variable-fonts",
        default=".*",
        metavar="VF_NAME",
        help=(
            "Filter the list of variable fonts produced from the input "
            "Designspace v5 file. By default all listed variable fonts are "
            "generated. To generate a specific variable font (or variable fonts) "
            'that match a given "name" attribute, you can pass as argument '
            "the full name or a regular expression. E.g.: --variable-fonts "
            '"MyFontVF_WeightOnly"; or --variable-fonts "MyFontVFItalic_.*".'
        ),
    )
    logging_group = parser.add_mutually_exclusive_group(required=False)
    logging_group.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )
    logging_group.add_argument(
        "-q", "--quiet", action="store_true", help="Turn verbosity off."
    )
    options = parser.parse_args(args)

    configLogger(
        level=("DEBUG" if options.verbose else "ERROR" if options.quiet else "INFO")
    )

    designspace_filename = options.designspace
    designspace = DesignSpaceDocument.fromfile(designspace_filename)

    vf_descriptors = designspace.getVariableFonts()
    if not vf_descriptors:
        parser.error(f"No variable fonts in given designspace {designspace.path!r}")

    vfs_to_build = []
    for vf in vf_descriptors:
        # Skip variable fonts that do not match the user's inclusion regex if given.
        if not fullmatch(options.variable_fonts, vf.name):
            continue
        vfs_to_build.append(vf)

    if not vfs_to_build:
        parser.error(f"No variable fonts matching {options.variable_fonts!r}")

    if options.outfile is not None and len(vfs_to_build) > 1:
        parser.error(
            "can't specify -o because there are multiple VFs to build; "
            "use --output-dir, or select a single VF with --variable-fonts"
        )

    output_dir = options.output_dir
    if output_dir is None:
        output_dir = os.path.dirname(designspace_filename)

    vf_name_to_output_path = {}
    if len(vfs_to_build) == 1 and options.outfile is not None:
        vf_name_to_output_path[vfs_to_build[0].name] = options.outfile
    else:
        for vf in vfs_to_build:
            if vf.filename is not None:
                # Only use basename to prevent path traversal attacks
                filename = os.path.basename(vf.filename)
            else:
                filename = vf.name + ".{ext}"
            vf_name_to_output_path[vf.name] = os.path.join(output_dir, filename)

    vf_names_to_build = {vf.name for vf in vfs_to_build}
    finder = MasterFinder(options.master_finder)

    vfs = build_many(
        designspace,
        finder,
        exclude=options.exclude,
        optimize=options.optimize,
        skip_vf=lambda name: name not in vf_names_to_build,
        colr_layer_reuse=options.colr_layer_reuse,
        drop_implied_oncurves=options.drop_implied_oncurves,
    )

    for vf_name, vf in vfs.items():
        ext = "otf" if vf.sfntVersion == "OTTO" else "ttf"
        output_path = vf_name_to_output_path[vf_name].format(ext=ext)
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        log.info("Saving variation font %s", output_path)
        vf.save(output_path)


def main(args=None):
    """Convert MS VOLT to AFDKO feature files."""

    import argparse
    from pathlib import Path

    from fontTools import configLogger

    parser = argparse.ArgumentParser(
        "fonttools voltLib.voltToFea", description=main.__doc__
    )
    parser.add_argument(
        "input", metavar="INPUT", type=Path, help="input font/VTP file to process"
    )
    parser.add_argument(
        "featurefile", metavar="OUTPUT", type=Path, help="output feature file"
    )
    parser.add_argument(
        "-t",
        "--table",
        action="append",
        choices=TABLES,
        dest="tables",
        help="List of tables to write, by default all tables are written",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress non-error messages"
    )
    parser.add_argument(
        "--traceback", action="store_true", help="Don’t catch exceptions"
    )

    options = parser.parse_args(args)

    configLogger(level=("ERROR" if options.quiet else "INFO"))

    file_or_path = options.input
    font = None
    try:
        font = TTFont(file_or_path)
        if "TSIV" in font:
            file_or_path = StringIO(font["TSIV"].data.decode("utf-8"))
        else:
            log.error('"TSIV" table is missing, font was not saved from VOLT?')
            return 1
    except TTLibError:
        pass

    converter = VoltToFea(file_or_path, font)
    try:
        fea = converter.convert(options.tables)
    except NotImplementedError as e:
        if options.traceback:
            raise
        location = getattr(e.args[0], "location", None)
        message = f'"{e}" is not supported'
        if location:
            path, line, column = location
            log.error(f"{path}:{line}:{column}: {message}")
        else:
            log.error(message)
        return 1
    with open(options.featurefile, "w") as feafile:
        feafile.write(fea)


def main(args=None):
    """Build tables from a MS VOLT project into an OTF font"""
    parser = argparse.ArgumentParser(
        description="Use fontTools to compile MS VOLT projects."
    )
    parser.add_argument(
        "input",
        metavar="INPUT",
        help="Path to the input font/VTP file to process",
        type=Path,
    )
    parser.add_argument(
        "-f",
        "--font",
        metavar="INPUT_FONT",
        help="Path to the input font (if INPUT is a VTP file)",
        type=Path,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        metavar="OUTPUT",
        help="Path to the output font.",
        type=Path,
    )
    parser.add_argument(
        "-t",
        "--tables",
        metavar="TABLE_TAG",
        choices=SUPPORTED_TABLES,
        nargs="+",
        help="Specify the table(s) to be built.",
    )
    parser.add_argument(
        "-F",
        "--debug-feature-file",
        help="Write the generated feature file to disk.",
        action="store_true",
    )
    parser.add_argument(
        "--ship",
        help="Remove source VOLT tables from output font.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase the logger verbosity. Multiple -v options are allowed.",
        action="count",
        default=0,
    )
    parser.add_argument(
        "-T",
        "--traceback",
        help="show traceback for exceptions.",
        action="store_true",
    )
    options = parser.parse_args(args)

    levels = ["WARNING", "INFO", "DEBUG"]
    configLogger(level=levels[min(len(levels) - 1, options.verbose)])

    output_font = options.output or Path(
        makeOutputFileName(options.font or options.input)
    )
    log.info(f"Compiling MS VOLT to '{output_font}'")

    file_or_path = options.input
    font = None

    # If the input is a font file, extract the VOLT data from the "TSIV" table
    try:
        font = TTFont(file_or_path)
        if "TSIV" in font:
            file_or_path = StringIO(font["TSIV"].data.decode("utf-8"))
        else:
            log.error('"TSIV" table is missing')
            return 1
    except TTLibError:
        pass

    # If input is not a font file, the font must be provided
    if font is None:
        if not options.font:
            log.error("Please provide an input font")
            return 1
        font = TTFont(options.font)

    # FEA syntax does not allow some glyph names that VOLT accepts, so if we
    # found such glyph name we will temporarily rename such glyphs.
    glyphOrder = font.getGlyphOrder()
    tempGlyphOrder = None
    if any(invalid_fea_glyph_name(n) for n in glyphOrder):
        tempGlyphOrder = []
        for n in glyphOrder:
            if invalid_fea_glyph_name(n):
                n = sanitize_glyph_name(n)
                existing = set(tempGlyphOrder) | set(glyphOrder)
                while n in existing:
                    n = "a" + n
            tempGlyphOrder.append(n)
        font.setGlyphOrder(tempGlyphOrder)

    doc = Parser(file_or_path).parse()

    log.info("Converting VTP data to FEA")
    converter = VoltToFea(doc, font)
    try:
        fea = converter.convert(options.tables, ignore_unsupported_settings=True)
    except NotImplementedError as e:
        if options.traceback:
            raise
        location = getattr(e.args[0], "location", None)
        message = f'"{e}" is not supported'
        if location:
            path, line, column = location
            log.error(f"{path}:{line}:{column}: {message}")
        else:
            log.error(message)
        return 1

    fea_filename = options.input
    if options.debug_feature_file:
        fea_filename = output_font.with_suffix(".fea")
        log.info(f"Writing FEA to '{fea_filename}'")
        with open(fea_filename, "w") as fp:
            fp.write(fea)

    log.info("Compiling FEA to OpenType tables")
    try:
        addOpenTypeFeaturesFromString(
            font,
            fea,
            filename=fea_filename,
            tables=options.tables,
        )
    except FeatureLibError as e:
        if options.traceback:
            raise
        log.error(e)
        return 1

    if options.ship:
        for tag in ["TSIV", "TSIS", "TSIP", "TSID"]:
            if tag in font:
                del font[tag]

    # Restore original glyph names.
    if tempGlyphOrder:
        import io

        f = io.BytesIO()
        font.save(f)
        font = TTFont(f)
        font.setGlyphOrder(glyphOrder)
        font["post"].extraNames = []

    font.save(output_font)


def main(args=None):
    """Add `avar` table from designspace file to variable font."""

    from fontTools.ttLib import TTFont
    from fontTools.misc.cliTools import makeOutputFileName
    from fontTools import configLogger
    import argparse

    if args is None:
        import sys

        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        "fonttools varLib.avar.build",
        description="Add `avar` table from designspace file to variable font.",
    )
    parser.add_argument("font", metavar="varfont.ttf", help="Variable-font file.")
    parser.add_argument(
        "designspace",
        metavar="family.designspace",
        help="Designspace file.",
        default=None,
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="Output font file name.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )

    options = parser.parse_args(args)

    configLogger(level=("INFO" if options.verbose else "WARNING"))

    font = TTFont(options.font)

    build(font, options.designspace)

    if options.output_file is None:
        outfile = makeOutputFileName(options.font, overWrite=True, suffix=".avar")
    else:
        outfile = options.output_file
    if outfile:
        log.info("Saving %s", outfile)
        font.save(outfile)


def main(args=None):
    """Map variation coordinates through the `avar` table."""

    from fontTools.ttLib import TTFont
    import argparse

    if args is None:
        import sys

        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        "fonttools varLib.avar.map",
        description="Map variation coordinates through the `avar` table.",
    )
    parser.add_argument("font", metavar="varfont.ttf", help="Variable-font file.")
    parser.add_argument(
        "coords",
        metavar="[AXIS=value...]",
        help="Coordinates to map, e.g. 'wght=700 wdth=75'.",
        nargs="*",
        default=None,
    )
    parser.add_argument(
        "-f", action="store_true", help="Do not omit axes at default location."
    )
    parser.add_argument(
        "-i", action="store_true", help="Input coordinates are normalized (-1..1)."
    )
    parser.add_argument(
        "-o", action="store_true", help="Output coordinates as normalized (-1..1)."
    )

    options = parser.parse_args(args)

    if not options.coords:
        parser.error(
            "No coordinates provided. Please specify at least one axis coordinate (e.g., wght=500)"
        )

    if options.font.endswith(".designspace"):
        from .build import build

        font = TTFont()
        build(font, options.font)
    else:
        font = TTFont(options.font)
        if "fvar" not in font:
            parser.error(f"Font '{options.font}' does not contain an 'fvar' table.")

    location = {}
    for item in options.coords:
        tag, sep, value = item.partition("=")
        if not sep or not tag or not value:
            parser.error(
                f"Invalid coordinate {item!r}. Expected AXIS=value, e.g. wght=500"
            )
        try:
            location[tag] = float(value)
        except ValueError:
            parser.error(
                f"Invalid coordinate value in {item!r}. Expected a number after '='"
            )

    try:
        mapped = map(
            font,
            location,
            inputNormalized=options.i,
            outputNormalized=options.o,
            dropZeroes=not options.f,
        )
    except ValueError as e:
        parser.error(str(e))
    assert mapped is not None

    for tag in mapped:
        v = mapped[tag]
        v = int(v) if v == int(v) else v
        print(f"{tag}={v:g}")


def main(args=None):
    """Plan the standard axis mappings for a variable font"""

    if args is None:
        import sys

        args = sys.argv[1:]

    from fontTools import configLogger
    from fontTools.ttLib import TTFont
    import argparse

    parser = argparse.ArgumentParser(
        "fonttools varLib.avar.plan",
        description="Plan `avar` table for variable font",
    )
    parser.add_argument("font", metavar="varfont.ttf", help="Variable-font file.")
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="Output font file name.",
    )
    parser.add_argument(
        "--weights", type=str, help="Space-separate list of weights to generate."
    )
    parser.add_argument(
        "--widths", type=str, help="Space-separate list of widths to generate."
    )
    parser.add_argument(
        "--slants", type=str, help="Space-separate list of slants to generate."
    )
    parser.add_argument(
        "--sizes", type=str, help="Space-separate list of optical-sizes to generate."
    )
    parser.add_argument("--samples", type=int, help="Number of samples.")
    parser.add_argument(
        "-s", "--sanitize", action="store_true", help="Sanitize axis limits"
    )
    parser.add_argument(
        "-g",
        "--glyphs",
        type=str,
        help="Space-separate list of glyphs to use for sampling.",
    )
    parser.add_argument(
        "--weight-design-limits",
        type=str,
        help="min:default:max in design units for the `wght` axis.",
    )
    parser.add_argument(
        "--width-design-limits",
        type=str,
        help="min:default:max in design units for the `wdth` axis.",
    )
    parser.add_argument(
        "--slant-design-limits",
        type=str,
        help="min:default:max in design units for the `slnt` axis.",
    )
    parser.add_argument(
        "--optical-size-design-limits",
        type=str,
        help="min:default:max in design units for the `opsz` axis.",
    )
    parser.add_argument(
        "--weight-pins",
        type=str,
        help="Space-separate list of before:after pins for the `wght` axis.",
    )
    parser.add_argument(
        "--width-pins",
        type=str,
        help="Space-separate list of before:after pins for the `wdth` axis.",
    )
    parser.add_argument(
        "--slant-pins",
        type=str,
        help="Space-separate list of before:after pins for the `slnt` axis.",
    )
    parser.add_argument(
        "--optical-size-pins",
        type=str,
        help="Space-separate list of before:after pins for the `opsz` axis.",
    )
    parser.add_argument(
        "-p", "--plot", action="store_true", help="Plot the resulting mapping."
    )

    logging_group = parser.add_mutually_exclusive_group(required=False)
    logging_group.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )
    logging_group.add_argument(
        "-q", "--quiet", action="store_true", help="Turn verbosity off."
    )

    options = parser.parse_args(args)

    configLogger(
        level=("DEBUG" if options.verbose else "WARNING" if options.quiet else "INFO")
    )

    font = TTFont(options.font)
    if not "fvar" in font:
        log.error("Not a variable font.")
        return 1

    if options.glyphs is not None:
        glyphs = options.glyphs.split()
        if ":" in options.glyphs:
            glyphs = {}
            for g in options.glyphs.split():
                if ":" in g:
                    glyph, frequency = g.split(":")
                    glyphs[glyph] = float(frequency)
                else:
                    glyphs[g] = 1.0
    else:
        glyphs = None

    designspaceSnippets = []

    designspaceSnippets.append(
        processAxis(
            font,
            planWeightAxis,
            "wght",
            "Weight",
            values=options.weights,
            samples=options.samples,
            glyphs=glyphs,
            designLimits=options.weight_design_limits,
            pins=options.weight_pins,
            sanitize=options.sanitize,
            plot=options.plot,
        )
    )
    designspaceSnippets.append(
        processAxis(
            font,
            planWidthAxis,
            "wdth",
            "Width",
            values=options.widths,
            samples=options.samples,
            glyphs=glyphs,
            designLimits=options.width_design_limits,
            pins=options.width_pins,
            sanitize=options.sanitize,
            plot=options.plot,
        )
    )
    designspaceSnippets.append(
        processAxis(
            font,
            planSlantAxis,
            "slnt",
            "Slant",
            values=options.slants,
            samples=options.samples,
            glyphs=glyphs,
            designLimits=options.slant_design_limits,
            pins=options.slant_pins,
            sanitize=options.sanitize,
            plot=options.plot,
        )
    )
    designspaceSnippets.append(
        processAxis(
            font,
            planOpticalSizeAxis,
            "opsz",
            "OpticalSize",
            values=options.sizes,
            samples=options.samples,
            glyphs=glyphs,
            designLimits=options.optical_size_design_limits,
            pins=options.optical_size_pins,
            sanitize=options.sanitize,
            plot=options.plot,
        )
    )

    log.info("Designspace snippet:")
    for snippet in designspaceSnippets:
        if snippet:
            print(snippet)

    if options.output_file is None:
        outfile = makeOutputFileName(options.font, overWrite=True, suffix=".avar")
    else:
        outfile = options.output_file
    if outfile:
        log.info("Saving %s", outfile)
        font.save(outfile)


def main(args=None):
    """Print `avar` table as a designspace snippet."""

    if args is None:
        args = sys.argv[1:]

    from fontTools.ttLib import TTFont
    import argparse

    parser = argparse.ArgumentParser(
        "fonttools varLib.avar.unbuild",
        description="Print `avar` table as a designspace snippet.",
    )
    parser.add_argument("font", metavar="varfont.ttf", help="Variable-font file.")
    options = parser.parse_args(args)

    font = TTFont(options.font)
    if "fvar" not in font:
        print("Not a variable font.", file=sys.stderr)
        return 1

    unbuild(font)


def main(args=None):
    from fontTools.ttLib import TTFont
    from fontTools.misc.cliTools import makeOutputFileName
    from fontTools import configLogger
    import argparse
    import sys

    print(
        "WARNING: This script is deprecated. Use `fonttools varLib.avar.build` "
        "or `fonttools varLib.avar.unbuild` instead.\n",
        file=sys.stderr,
    )

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        "fonttools varLib.avar",
        description="Add `avar` table from designspace file to variable font.",
    )
    parser.add_argument("font", metavar="varfont.ttf", help="Variable-font file.")
    parser.add_argument(
        "designspace",
        metavar="family.designspace",
        help="Designspace file.",
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        help="Output font file name.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )

    options = parser.parse_args(args)

    configLogger(level=("INFO" if options.verbose else "WARNING"))

    font = TTFont(options.font)

    if options.designspace is None:
        from .unbuild import unbuild

        unbuild(font)
        return 0

    from .build import build

    build(font, options.designspace)

    if options.output_file is None:
        outfile = makeOutputFileName(options.font, overWrite=True, suffix=".avar")
    else:
        outfile = options.output_file
    if outfile:
        log.info("Saving %s", outfile)
        font.save(outfile)


def main(args=None):
    """Partially instantiate a variable font"""
    infile, axisLimits, options = parseArgs(args)
    log.info("Restricting axes: %s", axisLimits)

    log.info("Loading variable font")
    varfont = TTFont(
        infile,
        recalcTimestamp=options.recalc_timestamp,
        recalcBBoxes=options.recalc_bounds,
    )

    isFullInstance = options.static or {
        axisTag
        for axisTag, limit in axisLimits.items()
        if limit is None or limit[0] == limit[2]
    }.issuperset(axis.axisTag for axis in varfont["fvar"].axes)

    varfont = instantiateVariableFont(
        varfont,
        axisLimits,
        inplace=True,
        optimize=options.optimize,
        overlap=options.overlap,
        updateFontNames=options.update_name_table,
        downgradeCFF2=options.downgrade_cff2,
        static=options.static,
    )

    suffix = "-instance" if isFullInstance else "-partial"
    outfile = (
        makeOutputFileName(infile, overWrite=True, suffix=suffix)
        if not options.output
        else options.output
    )

    log.info(
        "Saving %s font %s",
        "instance" if isFullInstance else "partial variable",
        outfile,
    )
    varfont.save(outfile)


def main(args=None):
    """Optimize the layout tables of an existing font"""
    from argparse import ArgumentParser

    from fontTools import configLogger

    parser = ArgumentParser(
        prog="otlLib.optimize",
        description=main.__doc__,
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("font")
    parser.add_argument(
        "-o", metavar="OUTPUTFILE", dest="outfile", default=None, help="output file"
    )
    parser.add_argument(
        "--gpos-compression-level",
        help=COMPRESSION_LEVEL.help,
        default=COMPRESSION_LEVEL.default,
        choices=list(range(10)),
        type=int,
    )
    logging_group = parser.add_mutually_exclusive_group(required=False)
    logging_group.add_argument(
        "-v", "--verbose", action="store_true", help="Run more verbosely."
    )
    logging_group.add_argument(
        "-q", "--quiet", action="store_true", help="Turn verbosity off."
    )
    options = parser.parse_args(args)

    configLogger(
        level=("DEBUG" if options.verbose else "ERROR" if options.quiet else "INFO")
    )

    font = TTFont(options.font)
    compact(font, options.gpos_compression_level)
    font.save(options.outfile or options.font)


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the main bit of the application.

    This handles the creation of an instance of :class:`Application`, runs it,
    and then exits the application.

    :param argv:
        The arguments to be passed to the application for parsing.
    """
    if argv is None:
        argv = sys.argv[1:]

    app = application.Application()
    app.run(argv)
    return app.exit_code()


def main():
    """Execute Bandit."""
    # our cleanup function needs this and can't be passed arguments
    global current_commit
    global repo

    parent_commit = None
    output_format = None
    repo = None
    report_fname = None

    init_logger()

    output_format, repo, report_fname = initialize()

    if not repo:
        sys.exit(2)

    # #################### Find current and parent commits ####################
    try:
        commit = repo.commit()
        current_commit = commit.hexsha
        LOG.info("Got current commit: [%s]", commit.name_rev)

        commit = commit.parents[0]
        parent_commit = commit.hexsha
        LOG.info("Got parent commit: [%s]", commit.name_rev)

    except git.GitCommandError:
        LOG.error("Unable to get current or parent commit")
        sys.exit(2)
    except IndexError:
        LOG.error("Parent commit not available")
        sys.exit(2)

    # #################### Run Bandit against both commits ####################
    output_type = (
        ["-f", "txt"]
        if output_format == default_output_format
        else ["-o", report_fname]
    )

    with baseline_setup() as t:
        bandit_tmpfile = f"{t}/{baseline_tmp_file}"

        steps = [
            {
                "message": "Getting Bandit baseline results",
                "commit": parent_commit,
                "args": bandit_args + ["-f", "json", "-o", bandit_tmpfile],
            },
            {
                "message": "Comparing Bandit results to baseline",
                "commit": current_commit,
                "args": bandit_args + ["-b", bandit_tmpfile] + output_type,
            },
        ]

        return_code = None

        for step in steps:
            repo.head.reset(commit=step["commit"], working_tree=True)

            LOG.info(step["message"])

            bandit_command = ["bandit"] + step["args"]

            try:
                output = subprocess.check_output(bandit_command)  # nosec: B603
            except subprocess.CalledProcessError as e:
                output = e.output
                return_code = e.returncode
            else:
                return_code = 0
                output = output.decode("utf-8")  # subprocess returns bytes

            if return_code not in [0, 1]:
                LOG.error(
                    "Error running command: %s\nOutput: %s\n",
                    bandit_args,
                    output,
                )

    # #################### Output and exit ####################################
    # print output or display message about written report
    if output_format == default_output_format:
        print(output)
    else:
        LOG.info("Successfully wrote %s", report_fname)

    # exit with the code the last Bandit run returned
    sys.exit(return_code)


def main():
    """Config generator to write configuration file."""
    init_logger()
    args = parse_args()

    yaml_settings = get_config_settings()

    if args.show_defaults:
        print(yaml_settings)

    if args.output_file:
        if os.path.exists(os.path.abspath(args.output_file)):
            LOG.error("File %s already exists, exiting", args.output_file)
            sys.exit(2)

        try:
            with open(args.output_file, "w") as f:
                skips = args.skips.split(",") if args.skips else []
                tests = args.tests.split(",") if args.tests else []

                for skip in skips:
                    if not extension_loader.MANAGER.check_id(skip):
                        raise RuntimeError(f"unknown ID in skips: {skip}")

                for test in tests:
                    if not extension_loader.MANAGER.check_id(test):
                        raise RuntimeError(f"unknown ID in tests: {test}")

                tpl = "# {0} : {1}"
                test_list = [
                    tpl.format(t.plugin._test_id, t.name)
                    for t in extension_loader.MANAGER.plugins
                ]

                others = [
                    tpl.format(k, v["name"])
                    for k, v in (
                        extension_loader.MANAGER.blacklist_by_id.items()
                    )
                ]
                test_list.extend(others)
                test_list.sort()

                contents = template.format(
                    cli=" ".join(sys.argv),
                    settings=yaml_settings,
                    test_list="\n".join(test_list),
                    skip="skips: " + str(skips) if skips else "skips:",
                    test="tests: " + str(tests) if tests else "tests:",
                )
                f.write(contents)

        except OSError:
            LOG.error("Unable to open %s for writing", args.output_file)

        except Exception as e:
            LOG.error("Error: %s", e)

        else:
            LOG.info("Successfully wrote profile: %s", args.output_file)

    return 0


def main():
    """Bandit CLI."""
    # bring our logging stuff up as early as possible
    debug = (
        logging.DEBUG
        if "-d" in sys.argv or "--debug" in sys.argv
        else logging.INFO
    )
    _init_logger(debug)
    extension_mgr = _init_extensions()

    baseline_formatters = [
        f.name
        for f in filter(
            lambda x: hasattr(x.plugin, "_accepts_baseline"),
            extension_mgr.formatters,
        )
    ]

    # now do normal startup
    parser = argparse.ArgumentParser(
        description="Bandit - a Python source code security analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    if sys.version_info >= (3, 14):
        parser.suggest_on_error = True
        parser.color = False

    parser.add_argument(
        "targets",
        metavar="targets",
        type=str,
        nargs="*",
        help="source file(s) or directory(s) to be tested",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        help="find and process files in subdirectories",
    )
    parser.add_argument(
        "-a",
        "--aggregate",
        dest="agg_type",
        action="store",
        default="file",
        type=str,
        choices=["file", "vuln"],
        help="aggregate output by vulnerability (default) or by filename",
    )
    parser.add_argument(
        "-n",
        "--number",
        dest="context_lines",
        action="store",
        default=3,
        type=int,
        help="maximum number of code lines to output for each issue",
    )
    parser.add_argument(
        "-c",
        "--configfile",
        dest="config_file",
        action="store",
        default=None,
        type=str,
        help="optional config file to use for selecting plugins and "
        "overriding defaults",
    )
    parser.add_argument(
        "-p",
        "--profile",
        dest="profile",
        action="store",
        default=None,
        type=str,
        help="profile to use (defaults to executing all tests)",
    )
    parser.add_argument(
        "-t",
        "--tests",
        dest="tests",
        action="store",
        default=None,
        type=str,
        help="comma-separated list of test IDs to run",
    )
    parser.add_argument(
        "-s",
        "--skip",
        dest="skips",
        action="store",
        default=None,
        type=str,
        help="comma-separated list of test IDs to skip",
    )
    severity_group = parser.add_mutually_exclusive_group(required=False)
    severity_group.add_argument(
        "-l",
        "--level",
        dest="severity",
        action="count",
        default=1,
        help="report only issues of a given severity level or "
        "higher (-l for LOW, -ll for MEDIUM, -lll for HIGH)",
    )
    severity_group.add_argument(
        "--severity-level",
        dest="severity_string",
        action="store",
        help="report only issues of a given severity level or higher."
        ' "all" and "low" are likely to produce the same results, but it'
        " is possible for rules to be undefined which will"
        ' not be listed in "low".',
        choices=["all", "low", "medium", "high"],
    )
    confidence_group = parser.add_mutually_exclusive_group(required=False)
    confidence_group.add_argument(
        "-i",
        "--confidence",
        dest="confidence",
        action="count",
        default=1,
        help="report only issues of a given confidence level or "
        "higher (-i for LOW, -ii for MEDIUM, -iii for HIGH)",
    )
    confidence_group.add_argument(
        "--confidence-level",
        dest="confidence_string",
        action="store",
        help="report only issues of a given confidence level or higher."
        ' "all" and "low" are likely to produce the same results, but it'
        " is possible for rules to be undefined which will"
        ' not be listed in "low".',
        choices=["all", "low", "medium", "high"],
    )
    output_format = (
        "screen"
        if (
            sys.stdout.isatty()
            and os.getenv("NO_COLOR") is None
            and os.getenv("TERM") != "dumb"
        )
        else "txt"
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        action="store",
        default=output_format,
        help="specify output format",
        choices=sorted(extension_mgr.formatter_names),
    )
    parser.add_argument(
        "--msg-template",
        action="store",
        default=None,
        help="specify output message template"
        " (only usable with --format custom),"
        " see CUSTOM FORMAT section"
        " for list of available values",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        action="store",
        nargs="?",
        type=argparse.FileType("w", encoding="utf-8"),
        default=sys.stdout,
        help="write report to filename",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="output extra information like excluded and included files",
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="turn on debug mode",
    )
    group.add_argument(
        "-q",
        "--quiet",
        "--silent",
        dest="quiet",
        action="store_true",
        help="only show output in the case of an error",
    )
    parser.add_argument(
        "--ignore-nosec",
        dest="ignore_nosec",
        action="store_true",
        help="do not skip lines with # nosec comments",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        dest="excluded_paths",
        action="store",
        default=",".join(constants.EXCLUDE),
        help="comma-separated list of paths (glob patterns "
        "supported) to exclude from scan "
        "(note that these are in addition to the excluded "
        "paths provided in the config file) (default: "
        + ",".join(constants.EXCLUDE)
        + ")",
    )
    parser.add_argument(
        "-b",
        "--baseline",
        dest="baseline",
        action="store",
        default=None,
        help="path of a baseline report to compare against "
        "(only JSON-formatted files are accepted)",
    )
    parser.add_argument(
        "--ini",
        dest="ini_path",
        action="store",
        default=None,
        help="path to a .bandit file that supplies command line arguments",
    )
    parser.add_argument(
        "--exit-zero",
        action="store_true",
        dest="exit_zero",
        default=False,
        help="exit with 0, " "even with results found",
    )
    python_ver = sys.version.replace("\n", "")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {bandit.__version__}\n"
        f"  python version = {python_ver}",
    )

    parser.set_defaults(debug=False)
    parser.set_defaults(verbose=False)
    parser.set_defaults(quiet=False)
    parser.set_defaults(ignore_nosec=False)

    plugin_info = [
        f"{a[0]}\t{a[1].name}" for a in extension_mgr.plugins_by_id.items()
    ]
    blacklist_info = []
    for a in extension_mgr.blacklist.items():
        for b in a[1]:
            blacklist_info.append(f"{b['id']}\t{b['name']}")

    plugin_list = "\n\t".join(sorted(set(plugin_info + blacklist_info)))
    dedent_text = textwrap.dedent(
        """
    CUSTOM FORMATTING
    -----------------

    Available tags:

        {abspath}, {relpath}, {line}, {col}, {test_id},
        {severity}, {msg}, {confidence}, {range}

    Example usage:

        Default template:
        bandit -r examples/ --format custom --msg-template \\
        "{abspath}:{line}: {test_id}[bandit]: {severity}: {msg}"

        Provides same output as:
        bandit -r examples/ --format custom

        Tags can also be formatted in python string.format() style:
        bandit -r examples/ --format custom --msg-template \\
        "{relpath:20.20s}: {line:03}: {test_id:^8}: DEFECT: {msg:>20}"

        See python documentation for more information about formatting style:
        https://docs.python.org/3/library/string.html

    The following tests were discovered and loaded:
    -----------------------------------------------
    """
    )
    parser.epilog = dedent_text + f"\t{plugin_list}"

    # setup work - parse arguments, and initialize BanditManager
    args = parser.parse_args()
    # Check if `--msg-template` is not present without custom formatter
    if args.output_format != "custom" and args.msg_template is not None:
        parser.error("--msg-template can only be used with --format=custom")

    # Check if confidence or severity level have been specified with strings
    if args.severity_string is not None:
        if args.severity_string == "all":
            args.severity = 1
        elif args.severity_string == "low":
            args.severity = 2
        elif args.severity_string == "medium":
            args.severity = 3
        elif args.severity_string == "high":
            args.severity = 4
        # Other strings will be blocked by argparse

    if args.confidence_string is not None:
        if args.confidence_string == "all":
            args.confidence = 1
        elif args.confidence_string == "low":
            args.confidence = 2
        elif args.confidence_string == "medium":
            args.confidence = 3
        elif args.confidence_string == "high":
            args.confidence = 4
        # Other strings will be blocked by argparse

    # Handle .bandit files in projects to pass cmdline args from file
    ini_options = _get_options_from_ini(args.ini_path, args.targets)
    if ini_options:
        # prefer command line, then ini file
        args.config_file = _log_option_source(
            parser.get_default("configfile"),
            args.config_file,
            ini_options.get("configfile"),
            "config file",
        )

        args.excluded_paths = _log_option_source(
            parser.get_default("excluded_paths"),
            args.excluded_paths,
            ini_options.get("exclude"),
            "excluded paths",
        )

        args.skips = _log_option_source(
            parser.get_default("skips"),
            args.skips,
            ini_options.get("skips"),
            "skipped tests",
        )

        args.tests = _log_option_source(
            parser.get_default("tests"),
            args.tests,
            ini_options.get("tests"),
            "selected tests",
        )

        ini_targets = ini_options.get("targets")
        if ini_targets:
            ini_targets = ini_targets.split(",")

        args.targets = _log_option_source(
            parser.get_default("targets"),
            args.targets,
            ini_targets,
            "selected targets",
        )

        # TODO(tmcpeak): any other useful options to pass from .bandit?

        args.recursive = _log_option_source(
            parser.get_default("recursive"),
            args.recursive,
            ini_options.get("recursive"),
            "recursive scan",
        )

        args.agg_type = _log_option_source(
            parser.get_default("agg_type"),
            args.agg_type,
            ini_options.get("aggregate"),
            "aggregate output type",
        )

        args.context_lines = _log_option_source(
            parser.get_default("context_lines"),
            args.context_lines,
            int(ini_options.get("number") or 0) or None,
            "max code lines output for issue",
        )

        args.profile = _log_option_source(
            parser.get_default("profile"),
            args.profile,
            ini_options.get("profile"),
            "profile",
        )

        args.severity = _log_option_source(
            parser.get_default("severity"),
            args.severity,
            ini_options.get("level"),
            "severity level",
        )

        args.confidence = _log_option_source(
            parser.get_default("confidence"),
            args.confidence,
            ini_options.get("confidence"),
            "confidence level",
        )

        args.output_format = _log_option_source(
            parser.get_default("output_format"),
            args.output_format,
            ini_options.get("format"),
            "output format",
        )

        args.msg_template = _log_option_source(
            parser.get_default("msg_template"),
            args.msg_template,
            ini_options.get("msg-template"),
            "output message template",
        )

        args.output_file = _log_option_source(
            parser.get_default("output_file"),
            args.output_file,
            ini_options.get("output"),
            "output file",
        )

        args.verbose = _log_option_source(
            parser.get_default("verbose"),
            args.verbose,
            ini_options.get("verbose"),
            "output extra information",
        )

        args.debug = _log_option_source(
            parser.get_default("debug"),
            args.debug,
            ini_options.get("debug"),
            "debug mode",
        )

        args.quiet = _log_option_source(
            parser.get_default("quiet"),
            args.quiet,
            ini_options.get("quiet"),
            "silent mode",
        )

        args.ignore_nosec = _log_option_source(
            parser.get_default("ignore_nosec"),
            args.ignore_nosec,
            ini_options.get("ignore-nosec"),
            "do not skip lines with # nosec",
        )

        args.baseline = _log_option_source(
            parser.get_default("baseline"),
            args.baseline,
            ini_options.get("baseline"),
            "path of a baseline report",
        )

    try:
        b_conf = b_config.BanditConfig(config_file=args.config_file)
    except utils.ConfigError as e:
        LOG.error(e)
        sys.exit(2)

    if not args.targets:
        parser.print_usage()
        sys.exit(2)

    # if the log format string was set in the options, reinitialize
    if b_conf.get_option("log_format"):
        log_format = b_conf.get_option("log_format")
        _init_logger(log_level=logging.DEBUG, log_format=log_format)

    if args.quiet:
        _init_logger(log_level=logging.WARN)

    try:
        profile = _get_profile(b_conf, args.profile, args.config_file)
        _log_info(args, profile)

        profile["include"].update(args.tests.split(",") if args.tests else [])
        profile["exclude"].update(args.skips.split(",") if args.skips else [])
        extension_mgr.validate_profile(profile)

    except (utils.ProfileNotFound, ValueError) as e:
        LOG.error(e)
        sys.exit(2)

    b_mgr = b_manager.BanditManager(
        b_conf,
        args.agg_type,
        args.debug,
        profile=profile,
        verbose=args.verbose,
        quiet=args.quiet,
        ignore_nosec=args.ignore_nosec,
    )

    if args.baseline is not None:
        try:
            with open(args.baseline) as bl:
                data = bl.read()
                b_mgr.populate_baseline(data)
        except OSError:
            LOG.warning("Could not open baseline report: %s", args.baseline)
            sys.exit(2)

        if args.output_format not in baseline_formatters:
            LOG.warning(
                "Baseline must be used with one of the following "
                "formats: " + str(baseline_formatters)
            )
            sys.exit(2)

    if args.output_format != "json":
        if args.config_file:
            LOG.info("using config: %s", args.config_file)

        LOG.info(
            "running on Python %d.%d.%d",
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro,
        )

    # initiate file discovery step within Bandit Manager
    b_mgr.discover_files(args.targets, args.recursive, args.excluded_paths)

    if not b_mgr.b_ts.tests:
        LOG.error("No tests would be run, please check the profile.")
        sys.exit(2)

    # initiate execution of tests within Bandit Manager
    b_mgr.run_tests()
    LOG.debug(b_mgr.b_ma)
    LOG.debug(b_mgr.metrics)

    # trigger output of results by Bandit Manager
    sev_level = constants.RANKING[args.severity - 1]
    conf_level = constants.RANKING[args.confidence - 1]
    b_mgr.output_results(
        args.context_lines,
        sev_level,
        conf_level,
        args.output_file,
        args.output_format,
        args.msg_template,
    )

    if (
        b_mgr.results_count(sev_filter=sev_level, conf_filter=conf_level) > 0
        and not args.exit_zero
    ):
        sys.exit(1)
    else:
        sys.exit(0)


def main(*args: str, **kwargs: Any) -> None:
  """Executes a set of Python unit tests.

  Usually this function is called without arguments, so the
  unittest.TestProgram instance will get created with the default settings,
  so it will run all test methods of all TestCase classes in the ``__main__``
  module.

  Args:
    *args: Positional arguments passed through to
        ``unittest.TestProgram.__init__``.
    **kwargs: Keyword arguments passed through to
        ``unittest.TestProgram.__init__``.
  """
  print_python_version()
  _run_in_app(run_tests, args, kwargs)

