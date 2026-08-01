
def log_ir_post_fusion(nodes: SchedulerNodeList) -> None:
    if ir_post_fusion_log.isEnabledFor(logging.INFO):
        ir_post_fusion_log.info("AFTER FUSION\n%s", DebugFormatter._write_ir(nodes))

    V.debug.ir_post_fusion(nodes)

