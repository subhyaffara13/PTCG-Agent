
def run_llm_code_mutation_phase(meta_analyst, code_architect):
    logger.info("--- [LLM Meta-Learning Phase] ---")
    try:
        flaws = meta_analyst.analyze_logs()
        if not flaws:
            logger.info("No flaws extracted. Skipping code mutation.")
            return
        edits = code_architect.propose_code_fixes(flaws)
        if not edits or "files_to_edit" not in edits:
            logger.info("No code edits proposed.")
            return
        _apply_code_edits(edits)
        logger.info("Verifying LLM C++ syntax via test compilation...")
        compile_result = subprocess.run([sys.executable, "setup.py", "build_ext", "--inplace"], cwd="submission", capture_output=True, text=True)
        if compile_result.returncode != 0:
            logger.error("LLM hallucinated invalid C++ syntax! Reverting changes...")
            subprocess.run(["git", "restore", "submission/src/"], check=False)
            subprocess.run(["git", "restore", "submission/cb_agents/"], check=False)
        else:
            logger.info("LLM Code Patch compiled successfully! Running Gauntlet Evaluation guard...")
            try:
                win_rate = _run_gauntlet_guard()
                if win_rate < 0.50:
                    logger.error(f"Gauntlet Guard Rejected LLM Patch: Win rate fell to {win_rate*100:.1f}%. Reverting...")
                    subprocess.run(["git", "restore", "submission/src/"], check=False)
                    subprocess.run(["git", "restore", "submission/cb_agents/"], check=False)
                else:
                    logger.info(f"Gauntlet Guard Passed! Win rate: {win_rate*100:.1f}%. Keeping patch.")
            except Exception as g_err:
                logger.warning(f"Gauntlet evaluation guard encountered exception: {g_err}. Proceeding with caution.")
    except Exception as e:
        logger.error(f"LLM Meta-Learning Phase failed: {e}", exc_info=True)

