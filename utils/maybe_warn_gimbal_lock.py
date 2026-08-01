
def maybe_warn_gimbal_lock(should_warn, xp):
    if should_warn:
        # We can only warn on non-lazy backends because we'd need to condition on
        # traced booleans
        with eager_warns(UserWarning, match="Gimbal lock", xp=xp):
            yield

    else:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            yield

