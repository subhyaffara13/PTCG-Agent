
def _rb_anneal_beta(self):
    with self.lock: self.beta = min(1.0, self.beta + self.beta_increment)

