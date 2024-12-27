import math
import torch
import numpy as np
import torch.nn as nn
from torch.nn import functional as F
import pandas as pd
import baomodel as bm

# Initialize the model
model = bm.TransformerLanguageModel()
model = model.to(bm.device)

# Generate
model.load_state_dict(torch.load('bao-600000.pt', weights_only=True))
model.eval()
# start = np.random.random(bm.context_length)
# start_ids = start * 2000
start_ids = np.random.random_integers(0,2001,bm.context_length)
x = (torch.tensor(start_ids, dtype=torch.long, device=bm.device)[None, ...])
y = model.generate(x, max_new_tokens=1)
print('---------------')
print(x)
# print(y[0]/100)
print(((y[0]/100)-10))
print('---------------')
