
def _vjp_primal_fwd_tree_mismatch_err(self, tree):
  return (f"Custom VJP fwd rule {self.fwd.__name__} for function {self.traced.fun_name} "
          "must produce a pair (list or tuple of length two) where the first "
          "element represents the primal output "
          "(equal to the output of the custom_vjp-decorated function "
          f"{self.traced.fun_name}) and the "
          "second element represents residuals (i.e. values stored from the "
          "forward pass for use on the backward pass), but "
          f"instead the fwd rule output's first element had container/pytree "
          "structure:\n"
          f"""    {str(tree ).replace("'", "")}\n"""
          f"while the custom_vjp-decorated function {self.traced.fun_name} had output "
          "container/pytree structure:\n"
          f"""    {str(self.out_tree).replace("'", "")}.""")

