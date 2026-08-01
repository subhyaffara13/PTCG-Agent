
def collect_one_node(collector: Collector) -> CollectReport:
    ihook = collector.ihook
    ihook.pytest_collectstart(collector=collector)
    rep: CollectReport = ihook.pytest_make_collect_report(collector=collector)
    call = rep.__dict__.pop("call", None)
    if call and check_interactive_exception(call, rep):
        ihook.pytest_exception_interact(node=collector, call=call, report=rep)
    return rep

