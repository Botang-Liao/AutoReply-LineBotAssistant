from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
import torch
from transformers import BloomTokenizerFast

# 加載 Bloom 模型和分詞器，並應用 LoRA 改造（假設您已按前一段程式碼操作）
# ...
checkpoint = "ckip-joint/bloom-1b1-zh"
tokenizer = BloomTokenizerFast.from_pretrained(checkpoint)

# 準備訓練數據
train_file = 'train.txt'  # 這應該是您的訓練數據文件
train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=train_file,
    block_size=128  # 可以根據需要調整塊大小
)
print(train_dataset)