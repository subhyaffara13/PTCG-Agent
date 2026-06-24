import os
import json
import shutil
import logging
from pathlib import Path

logger = logging.getLogger("SanitizationTeam")

class SanitizationTeam:
    def __init__(self, skills_dir="skills", staging_dir="staging"):
        self.skills_dir = Path(skills_dir)
        self.staging_dir = Path(staging_dir)

    def validate_code(self, file_path: Path, content: str) -> tuple[bool, str]:
        """Runs syntax and security validations (delegated helpers)."""
        from factory.validator_syntax import check_syntax_and_inheritance
        from factory.validator_security import check_security_and_time
        
        passed, err = check_syntax_and_inheritance(file_path, content, self.skills_dir)
        if not passed:
            return False, f"Syntax/Inheritance check failed: {err}"
            
        failed_num, sec_err = check_security_and_time(file_path, content)
        if failed_num > 0:
            return False, f"Security check_{failed_num} failed: {sec_err}"
            
        return True, "All validations passed"

    def pack_tarball(self, source_tar: str, dest_name: str) -> bool:
        """Copies and packages the tarball submission with generated descriptions."""
        try:
            desc = ["Antigravity Apex Kaggle Submission."]
            for filename, keyword in [("learned_donts.json", "Deck Architect penalties"), ("strategy_tips.json", "Strategy Modifiers")]:
                p = self.skills_dir / filename
                if p.exists() and keyword in p.read_text(encoding="utf-8"):
                    desc.append(f"Features active {keyword}.")
            desc.append("Engine features MCTS Lookahead and Phase 5 Gusting/Energy-Acceleration heuristics.")
            desc_text = " ".join(desc)
            
            Path("submission_description.txt").write_text(desc_text, encoding="utf-8")
            if Path(source_tar).exists():
                shutil.copy(source_tar, dest_name)
                logger.info(f"Successfully packed submission tarball: {dest_name}")
                return True
        except Exception as e:
            logger.error(f"Failed to pack submission: {e}")
        return False
