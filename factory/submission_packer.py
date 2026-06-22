import os
import json
import tarfile
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("submission_packer")

def generate_description(skills_dir: Path) -> str:
    desc = ["Antigravity Apex Kaggle Submission."]
    
    donts_path = skills_dir / "learned_donts.json"
    if donts_path.exists():
        try:
            donts = json.loads(donts_path.read_text(encoding="utf-8"))
            if donts.get("deck_donts"):
                desc.append("Features active Deck Architect penalties to prevent bricking patterns.")
        except:
            pass
            
    tips_path = skills_dir / "strategy_tips.json"
    if tips_path.exists():
        try:
            tips = json.loads(tips_path.read_text(encoding="utf-8"))
            if tips.get("priority_modifiers"):
                desc.append("Equipped with dynamically learned Strategy Modifiers for advanced meta play.")
        except:
            pass
            
    desc.append("Engine features MCTS Lookahead and Phase 5 Gusting/Energy-Acceleration heuristics.")
    return " ".join(desc)

def pack_submission(source_tar: str = "submission_iter28_v0248.tar.gz"):
    skills_dir = Path("skills")
    desc_text = generate_description(skills_dir)
    
    # Save description
    desc_path = Path("submission_description.txt")
    desc_path.write_text(desc_text, encoding="utf-8")
    logger.info(f"Generated description at {desc_path}: \n{desc_text}")
    
    # Rename tarball to something unique
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_tar_name = f"Antigravity_Apex_{timestamp}.tar.gz"
    
    if Path(source_tar).exists():
        import shutil
        shutil.copy(source_tar, new_tar_name)
        logger.info(f"Packed Kaggle submission: {new_tar_name}")
    else:
        logger.warning(f"Could not find source tarball {source_tar}. Run the training loop first.")

if __name__ == "__main__":
    pack_submission()
