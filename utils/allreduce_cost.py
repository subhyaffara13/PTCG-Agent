
def allreduce_cost(bytes_gb: float, mesh_topo: MeshTopoInfo, mesh_dim: int) -> float:
    num_devices_on_mesh_dim = mesh_topo.mesh_dim_devices[mesh_dim]
    mesh_dim_bandwidth = mesh_topo.mesh_dim_bandwidth[mesh_dim]
    # allreduce have almost 2x comm bytes compare to allgather/reduce_scatter
    num_hops = 2 * (num_devices_on_mesh_dim - 1)

    latency = 6.6 + num_hops * mesh_topo.mesh_dim_latency[mesh_dim]
    bw = (bytes_gb * num_hops / num_devices_on_mesh_dim) / mesh_dim_bandwidth
    return latency + bw * 1e6

