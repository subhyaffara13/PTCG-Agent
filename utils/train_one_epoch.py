
def train_one_epoch(model, criterion, optimizer, data_loader, device, ntrain_batches):
    model.train()
    for cnt, (image, target) in enumerate(data_loader, start=1):
        print(".", end="")
        image, target = image.to(device), target.to(device)
        output = model(image)
        loss = criterion(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        accuracy(output, target, topk=(1, 5))
        if cnt >= ntrain_batches:
            return
    return

