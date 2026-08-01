
def get_real_stack(
    exc: Exception, frame: DynamoFrameType | None = None
) -> StackSummary | None:
    real_stack = getattr(exc, "real_stack", None)
    if real_stack is None:
        return None

    # NB: it's possible for real_stack to be []; we still attempt to
    # report a stack anyway because the stack_above_dynamo may still
    # be useful for debugging

    if frame is not None:
        # NB: frame is PyInterpreterFrame on Python 3.11 and later,
        # not a TRUE frame object.  You can't actually feed it
        # to traceback because it doesn't have enough information.
        # To solve this problem, we technically should just materialize
        # the frame, the same way _PyFrame_GetFrameObject would do
        # (but we cannot actually do this, because this populates
        # frame_obj field, which default eval frame doesn't like).
        #
        # Fortunately, in this case, we can hack it: there's no need
        # to actually use the truly top frame, we can just extract
        # from where we are right now and rely on filter_stack to
        # get rid of all the dynamo frames.  For ease of testing
        # we apply this behavior to ALL Python versions
        stack_above_dynamo = get_stack_above_dynamo()
    else:
        stack_above_dynamo = StackSummary()

    return StackSummary.from_list(stack_above_dynamo + real_stack)

