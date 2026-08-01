
def get_info_string(solver, info):
    if info == FTARGET_ACHIEVED:
        reason = 'the target function value is achieved.'
    elif info == MAXFUN_REACHED:
        reason = 'the objective function has been evaluated MAXFUN times.'
    elif info == MAXTR_REACHED:
        reason = 'the maximal number of trust region iterations has been reached.'
    elif info == SMALL_TR_RADIUS:
        reason = 'the trust region radius reaches its lower bound.'
    elif info == TRSUBP_FAILED:
        reason = 'a trust region step has failed to reduce the quadratic model.'
    elif info == NAN_INF_X:
        reason = 'NaN or Inf occurs in x.'
    elif info == NAN_INF_F:
        reason = 'the objective function returns NaN/+Inf.'
    elif info == NAN_INF_MODEL:
        reason = 'NaN or Inf occurs in the models.'
    elif info == DAMAGING_ROUNDING:
        reason = 'rounding errors are becoming damaging.'
    elif info == NO_SPACE_BETWEEN_BOUNDS:
        reason = 'there is no space between the lower and upper bounds of variable.'
    elif info == ZERO_LINEAR_CONSTRAINT:
        reason = 'one of the linear constraints has a zero gradient'
    elif info == CALLBACK_TERMINATE:
        reason = 'the callback function requested termination'
    else:
        reason = 'UNKNOWN EXIT FLAG'
    ret_message = f'Return from {solver} because {reason.strip()}'
    return ret_message

