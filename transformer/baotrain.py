import math
import torch
import torch.nn as nn
from torch.nn import functional as F
import pandas as pd
import baomodel as bm

stock_k = pd.read_csv('../datas/bao/sh.600000.csv')
diff_close = stock_k['close'].diff()
# 计算收盘价与开盘价之差
close_open_diff = stock_k['close'] - stock_k['open']
# 将收盘价差分小于-10和大于10的部分替换为收盘价与开盘价之差
diff_close[(diff_close < -10) | (diff_close > 10)] = close_open_diff[(diff_close < -10) | (diff_close > 10)]
tokenized_text = diff_close
tokenized_text.iloc[0] = 0
tokenized_text = (tokenized_text + 10) * 100
# tokenized_text = tokenized_text.astype(int)
# tokenized_text = range(-10,10,0.01)
tokenized_text = torch.tensor(tokenized_text, dtype=torch.long, device=bm.device)  # put tokenized text into tensor
# max_token_value = max(tokenized_text) + 1  # the maximum value of the tokenized numbers

# Split train and validation
split_idx = int(len(tokenized_text) * 0.9)
train_data = tokenized_text[:split_idx]
val_data = tokenized_text[split_idx:]

# Initialize the model
model = bm.TransformerLanguageModel()
model = model.to(bm.device)



# Get input embedding batch
def get_batch(split: str):
    data = train_data if split == 'train' else val_data
    idxs = torch.randint(low=0, high=len(data) - bm.context_length, size=(bm.batch_size,))
    x = torch.stack([data[idx:idx + bm.context_length] for idx in idxs]).to(bm.device)
    y = torch.stack([data[idx + 1:idx + bm.context_length + 1] for idx in idxs]).to(bm.device)
    return x, y


# Calculate loss
@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'valid']:
        losses = torch.zeros(bm.eval_iters)
        for k in range(bm.eval_iters):
            x_batch, y_batch = get_batch(split)
            logits, loss = model(x_batch, y_batch)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out


# Use AdamW optimizer
optimizer = torch.optim.AdamW(params=model.parameters(), lr=bm.learning_rate)
tracked_losses = list()
for step in range(bm.max_iters):
    if step % bm.eval_iters == 0 or step == bm.max_iters - 1:
        losses = estimate_loss()
        tracked_losses.append(losses)
        print('Step:', step, 'Training Loss:', round(losses['train'].item(), 3), 'Validation Loss:',
              round(losses['valid'].item(), 3))

    xb, yb = get_batch('train')
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

# Save the model state dictionary
torch.save(model.state_dict(), 'bao-600000.pt')
