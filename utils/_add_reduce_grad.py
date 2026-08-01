
def _add_reduce_grad(
    actions: list[_Action | None], n_microbatches: int
) -> list[_Action | None]:
    """
    REDUCE_GRAD refers to joint across minibatches grad reduction.
    reduce_grad frees memory and we want to schedule it just after the last "backward"-like stage.
    """
    actions_with_reduce_grad: list[_Action | None] = []
    cnt: dict[int, int] = defaultdict(int)

    def _leaf_action(a, to_schedule):
        if _requires_reduce_grad(a.computation_type):
            stage_index = a.stage_index
            cnt[stage_index] += 1
            if cnt[stage_index] == n_microbatches:
                to_schedule.append(stage_index)

    for a in actions:
        if a is None:
            continue
        actions_with_reduce_grad.append(a)
        schedule_reduce_grad_stage_idxs: list[int] = []
        if a.computation_type == OVERLAP_F_B and a.sub_actions is not None:
            for sub_action in a.sub_actions:
                _leaf_action(sub_action, schedule_reduce_grad_stage_idxs)
        else:
            _leaf_action(a, schedule_reduce_grad_stage_idxs)

        for stage_idx in schedule_reduce_grad_stage_idxs:
            actions_with_reduce_grad.append(_Action(stage_idx, REDUCE_GRAD, None))
    return actions_with_reduce_grad

