import torch.nn as nn

class QuantumSimHybridHead(nn.Module):
    def __init__(self, in_dim, h1=32, h2=16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, h1),
            nn.Tanh(),
            nn.Linear(h1, h2),
            nn.Tanh(),
            nn.Linear(h2, 2)
        )

    def forward(self, x):
        return self.net(x)

class VariationalLikeHead(nn.Module):
    def __init__(self, in_dim, h1=48, h2=24):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, h1),
            nn.Tanh(),
            nn.Linear(h1, h2),
            nn.Tanh(),
            nn.Linear(h2, 2)
        )

    def forward(self, x):
        return self.net(x)