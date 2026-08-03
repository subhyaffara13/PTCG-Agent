from pathlib import Path


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

