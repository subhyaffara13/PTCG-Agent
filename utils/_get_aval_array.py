
def _get_aval_array(self):
  return core.update_aval_with_sharding(self.aval, self.sharding)

