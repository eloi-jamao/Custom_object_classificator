import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import os
import argparse

root = os.getcwd()
images_dir = root + '/images'
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.cuda.current_device()

transform = transforms.Compose([
                                transforms.Resize(150), # Resize the short side of the image to 150 keeping aspect ratio
                                transforms.CenterCrop(150), # Crop a square in the center of the image
                                transforms.ToTensor(), # Convert the image to a tensor with pixels in the range [0, 1]
                                ])
def train_model(model, optimizer, criterion, train_loader, epochs):

    for epoch in range(epochs):
        # train
        model.train()
        train_loop = tqdm(train_loader, unit=" batches")  # For printing the progress bar
        for data, target in train_loop:
            train_loop.set_description('[TRAIN] Epoch {}/{}'.format(epoch + 1, epochs))
            data, target = data.float().to(device), target.float().to(device)
            target = target.unsqueeze(-1)
            optimizer.zero_grad()
            output = model(data)
            #print(output, target)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            train_loop.set_postfix(loss=train_loss.avg, accuracy=train_accuracy.avg)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pipeline execution')
    parser.add_argument('-o', '--objects', default=None, help='classes to train')
    parser.add_argument('-e', '--num_epochs', type=int, default=1, help='Number of epochs')
    parser.add_argument('-b', '--batch_size', type=int, default=5, help='Batch size')
    parser.add_argument('-ld', '--logdir', default=(os.getcwd() + r'/tf_logs'), help='Location of saved tf.summary')
    args = parser.parse_args()

    train_dataset = ImageFolder(images_dir, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)

    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss = nn.BCELoss()
    train_model(net, optimizer, loss, train_loader, args.num_epochs)