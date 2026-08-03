import logging

def log_ir_pre_fusion(nodes: SchedulerNodeList) -> None:
    if ir_pre_fusion_log.isEnabledFor(logging.INFO):
        ir_pre_fusion_log.info("BEFORE FUSION\n%s", DebugFormatter._write_ir(nodes))

    V.debug.ir_pre_fusion(nodes)

