
def archive_and_delete_old(log_dir, files_to_delete, archive_dir):
    import zipfile, time
    game_arc_name = f"game_logs_{int(time.time())}.zip"
    game_arc_path = os.path.join(archive_dir, game_arc_name)
    try:
        with zipfile.ZipFile(game_arc_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for fpath in files_to_delete: zf.write(fpath, arcname=os.path.basename(fpath))
        logger.info(f"Log Pruner: Compressed {len(files_to_delete)} game logs into archive {game_arc_name}")
    except Exception as e:
        logger.warning(f"Failed to create zip archive: {e}")
    deleted_count = 0
    for fpath in files_to_delete:
        try: os.remove(fpath); deleted_count += 1
        except Exception as e: logger.warning(f"Failed to delete {fpath}: {e}")
    logger.info(f"Log Pruner finished. Archived and deleted {deleted_count} files.")

