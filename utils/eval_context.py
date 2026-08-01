
def eval_context():
  with set_current_trace(eval_trace):
    yield

