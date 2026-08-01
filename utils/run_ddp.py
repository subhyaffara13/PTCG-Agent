
def run_ddp(rank, world_size, prepared):
    ddp_setup(rank, world_size)
    prepared.cuda()
    prepared = torch.nn.parallel.DistributedDataParallel(prepared, device_ids=[rank])
    prepared.to(rank)
    model_with_ddp = prepared
    optimizer = torch.optim.SGD(model_with_ddp.parameters(), lr=0.0001)
    train_one_epoch(model_with_ddp, criterion, optimizer, dataset, rank, 1)  # noqa: F821
    ddp_cleanup()

