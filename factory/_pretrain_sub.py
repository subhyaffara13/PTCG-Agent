import logging
logger = logging.getLogger(__name__)

def _setup_training(model, train_loader, val_loader, device, epochs, lr, model_path):
    import os, time, logging, torch, torch.nn as nn, torch.optim as optim
    from factory.pretrain_helpers import run_evaluation_loader, run_train_epoch
    logger = logging.getLogger(__name__)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    best_val_loss = float('inf')
    for epoch in range(epochs):
        start_time = time.time()
        total_loss = run_train_epoch(model, train_loader, device, optimizer, criterion)
        val_loss, val_acc = run_evaluation_loader(model, val_loader, device, criterion)
        logger.info(f"Epoch {epoch+1}/{epochs} | Time: {time.time()-start_time:.1f}s | "
                    f"Train Loss: {total_loss/len(train_loader):.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            os.makedirs('models', exist_ok=True)
            torch.save(model.state_dict(), model_path)
            logger.info(f"  -> Saved new best model to {model_path}")
