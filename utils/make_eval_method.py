
def make_eval_method(fact):
    def getit(self):
        pred = getattr(Q, fact)
        ret = ask(pred(self.expr), self.assumptions)
        return ret
    return getit

