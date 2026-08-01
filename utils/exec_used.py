
def exec_used(context):
    if context.call_function_name_qual == "exec":
        return exec_issue()

