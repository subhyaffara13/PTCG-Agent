
def update_state_ip(state, x, last_iteration_failed, objective,
                    prepared_constraints, start_time,
                    tr_radius, constr_penalty, cg_info,
                    barrier_parameter, barrier_tolerance):
    state = update_state_sqp(state, x, last_iteration_failed, objective,
                             prepared_constraints, start_time, tr_radius,
                             constr_penalty, cg_info)
    state.barrier_parameter = barrier_parameter
    state.barrier_tolerance = barrier_tolerance
    return state

