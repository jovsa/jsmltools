# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/custom_pytorch_training.ipynb (unless otherwise specified).

__all__ = ['train', 'eval_loss', 'train_epochs']

# Cell
def train(model, train_loader, optimizer):
    model.train()
    for x in train_loader:
        loss = model.nll(x)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


def eval_loss(model, data_loader):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for x in data_loader:
            loss = model.nll(x)
            total_loss += loss * x.shape[0]
        avg_loss = total_loss / len(data_loader.dataset)
    return avg_loss.item()


def train_epochs(model, train_loader, test_loader, train_args):
    epochs, lr = train_args['epochs'], train_args['lr']
    optimizer = optim.Adam(model.parameters(), lr=lr)

    train_losses, test_losses = [], []
    for epoch in range(epochs):
        model.train()

        train(model, train_loader, optimizer)
        train_loss = eval_loss(model, train_loader)
        train_losses.append(train_loss)

        if test_loader is not None:
            test_loss = eval_loss(model, test_loader)
            test_losses.append(test_loss)

        if epoch in [0, 2, 10, 50, 99]:
            plot_hist(train_loader.dataset.array, bins=d,
                      title=f'Epoch {epoch}', density=model.get_density())
    if test_loader is not None:
      print('Test Loss', test_loss)

    plot_train_curves(epochs, train_losses, test_losses, title='Training Curve')