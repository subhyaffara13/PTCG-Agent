
def worker_loop(log_dir, max_records, q, running_flag, current_file_ref, records_written_ref, stats_ref):
    import logging
    logger = logging.getLogger(__name__)
    while running_flag or not q.empty():
        try: record = q.get(timeout=1.0)
        except queue.Empty: continue
        try:
            start_time = time.time()
            if current_file_ref is None or records_written_ref >= max_records:
                if current_file_ref is not None: current_file_ref.close()
                current_file_ref = open(get_new_file_path(log_dir), 'at', encoding='utf-8')
                records_written_ref = 0
            json_str = json.dumps(record) + "\n"
            current_file_ref.write(json_str); current_file_ref.flush()
            records_written_ref += 1
            stats_ref["total_records"] += 1
            stats_ref["total_bytes"] += len(json_str.encode('utf-8'))
            stats_ref["total_write_time"] += (time.time() - start_time)
        except Exception as e:
            logger.error(f"TrajectoryLogger failed to write record: {e}")
        finally:
            q.task_done()
    if current_file_ref is not None: current_file_ref.close()

