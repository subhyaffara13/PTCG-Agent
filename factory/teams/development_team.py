"""
factory/teams/development_team.py

The Unified Development Team.
Responsible for orchestrating the LLM Code Mutation (MetaAnalyst + CodeArchitect) 
and the Simulated Annealing Deck Evolution.
"""
import sys
import subprocess
import pathlib
import logging
import concurrent.futures

from factory.deck_architect import DeckArchitect
from factory.teams.meta_analyst import MetaAnalyst
from factory.teams.code_architect import CodeArchitect

logger = logging.getLogger("DevelopmentTeam")

class DevelopmentTeam:
    def __init__(self):
        self.deck_architect = DeckArchitect()
        self.meta_analyst = MetaAnalyst()
        self.code_architect = CodeArchitect()

    def run_development(self, iteration: int):
        """
        Unified entry point to evolve the agent.
        Runs Deck Evolution every time, and LLM Code Evolution every 10 iterations.
        """
        logger.info("Development Team starting evolution cycle...")
        
        # 1. Deck Evolution (Simulated Annealing)
        try:
            logger.info("Starting automated Deck Evolution...")
            best_deck = self.deck_architect.build({})
            logger.info("Deck Evolution complete. New deck written to cb_agents/deck_new.csv.")
        except Exception as e:
            logger.error(f"Deck Evolution failed: {e}", exc_info=True)

        # 2. Code Evolution (LLM Meta-Learning Phase)
        if iteration > 0 and iteration % 10 == 0:
            self._run_llm_code_mutation()

    def _run_llm_code_mutation(self):
        """
        Runs the LLM Meta-Learning loop to mutate C++ code based on log flaws.
        Safely sandboxes the changes using Git and the compiler.
        """
        logger.info("--- [LLM Meta-Learning Phase] ---")
        try:
            flaws = self.meta_analyst.analyze_logs()
            if not flaws:
                logger.info("No flaws extracted. Skipping code mutation.")
                return

            edits = self.code_architect.propose_code_fixes(flaws)
            if not edits or "files_to_edit" not in edits:
                logger.info("No code edits proposed.")
                return

            # Apply edits
            for edit in edits["files_to_edit"]:
                fp = pathlib.Path(edit["filepath"])
                if fp.exists():
                    content = fp.read_text(encoding="utf-8")
                    if edit["original_code"] in content:
                        content = content.replace(edit["original_code"], edit["new_code"])
                        fp.write_text(content, encoding="utf-8")
                        logger.info(f"LLM successfully patched {fp.name}")
                    else:
                        logger.warning(f"LLM provided mismatched original_code for {fp.name}")

            # Sandboxed Compilation Check
            logger.info("Verifying LLM C++ syntax via test compilation...")
            compile_result = subprocess.run(
                [sys.executable, "setup.py", "build_ext", "--inplace"], 
                cwd="submission", capture_output=True, text=True
            )
            
            if compile_result.returncode != 0:
                logger.error("LLM hallucinated invalid C++ syntax! Reverting changes...")
                subprocess.run(["git", "restore", "submission/src/"], check=False)
                subprocess.run(["git", "restore", "submission/cb_agents/"], check=False)
            else:
                logger.info("LLM Code Patch compiled successfully! Keeping changes.")

        except Exception as e:
            logger.error(f"LLM Meta-Learning Phase failed: {e}", exc_info=True)
