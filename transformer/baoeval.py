import math
import torch
import numpy as np
import torch.nn as nn
from torch.nn import functional as F
import pandas as pd
import baomodel as bm
import encode as ec

# Initialize the model
model = bm.TransformerLanguageModel()
model = model.to(bm.device)

# Generate
model.load_state_dict(torch.load('bao-600000.pt', weights_only=True))
model.eval()

# start = np.random.random(bm.context_length)
# start_ids = start * 2000
rand_ids = np.random.random_integers(-10.00,10.00,bm.context_length)

# tokenized_text = encoder.decode([-9.1, 5.2])
start_ids = bm.encoder.decode(rand_ids)

# tokenized_text.iloc[0] = 0
x = (torch.tensor(start_ids, dtype=torch.long, device=bm.device)[None, ...])
y = model.generate(x, max_new_tokens=1)
print('---------------')
print(x)
print(y)
decoded_list = bm.encoder.decode_ranges(y.tolist()[0])
print(decoded_list)
print('---------------')
