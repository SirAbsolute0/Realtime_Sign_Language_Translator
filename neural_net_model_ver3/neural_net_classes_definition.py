"""
File contain class definition for the neural net model after each iteration.
"""

import torch.nn as nn


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(2 * 21, 100),
            nn.ReLU(),
            nn.Linear(100, 160),
            nn.ReLU(),
            nn.Linear(160, 26),
            nn.LogSoftmax(dim=1),
        )

    def forward(self, x):
        return self.net(x)


class NeuralNetwork_ver3(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(2 * 21, 100),
            nn.ReLU(),
            nn.Linear(100, 160),
            nn.ReLU(),
            nn.Linear(160, 26),
            nn.LogSoftmax(dim=1),
        )

    def forward(self, x):
        return self.net(x)
