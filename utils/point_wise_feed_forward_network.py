
def point_wise_feed_forward_network(d_model_size, dff):
    return nn.Sequential(nn.Linear(d_model_size, dff), nn.ReLU(), nn.Linear(dff, d_model_size))

