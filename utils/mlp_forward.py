
def mlp_forward(self, hidden_states):
    import torch.distributed as dist

    if dist.is_available() and dist.is_initialized() and hasattr(self, "_is_hooked"):
        routing = routing_torch_dist
    else:
        routing = triton_kernels_hub.routing.routing

    batch_size = hidden_states.shape[0]
    hidden_states = hidden_states.reshape(-1, self.router.hidden_dim)
    router_logits = nn.functional.linear(hidden_states, self.router.weight, self.router.bias)

    with on_device(router_logits.device):
        routing_data, gather_idx, scatter_idx = routing(router_logits, self.router.top_k)

    routed_out = self.experts(hidden_states, routing_data, gather_idx, scatter_idx=scatter_idx)
    routed_out = routed_out.reshape(batch_size, -1, self.router.hidden_dim)
    return routed_out, router_logits

