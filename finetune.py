import torch
import numpy as np
from transformers.models.gpt2 import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer
from transformers import BertTokenizer
model = GPT2LMHeadModel.from_pretrained("gpt")
tokenizer = BertTokenizer(vocab_file="gpt2通用中文模型/vocab.txt")

inputs_text = "你说"
input_ids = tokenizer.encode(inputs_text)
input_ids = input_ids[:-1]
inputs = {"input_ids": torch.tensor([input_ids])}
outputs = model(**inputs, labels=torch.tensor([input_ids]))
print(outputs.loss, outputs.logits)

