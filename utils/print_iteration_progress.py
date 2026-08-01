
def print_iteration_progress(iteration, residual, bc_residual, total_nodes,
                             nodes_added):
    print(f"{iteration:^15}{residual:^15.2e}{bc_residual:^15.2e}"
          f"{total_nodes:^15}{nodes_added:^15}")

