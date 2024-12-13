import torch

# Training function
def train(model, iterator, optimizer, criterion, device):
    epoch_loss = 0
    model.train()

    for batch in iterator:
        optimizer.zero_grad()
        text, labels = batch
        text, labels = text.to(device), labels.to(device)
        predictions = model(text)
        loss = criterion(predictions, labels.argmax(dim=1))
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()

    return epoch_loss / len(iterator)

# Evaluation function
def evaluate(model, iterator, criterion, device):
    epoch_loss = 0
    model.eval()

    with torch.no_grad():
        for batch in iterator:
            text, labels = batch
            text, labels = text.to(device), labels.to(device)
            predictions = model(text)
            loss = criterion(predictions, labels.argmax(dim=1))
            epoch_loss += loss.item()

    return epoch_loss / len(iterator)