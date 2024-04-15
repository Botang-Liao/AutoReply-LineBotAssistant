from transformers import BloomForCausalLM
from transformers import BloomTokenizerFast
import torch

checkpoint = "ckip-joint/bloom-1b1-zh"
model = BloomForCausalLM.from_pretrained(checkpoint)
tokenizer = BloomTokenizerFast.from_pretrained(checkpoint)

print('模型總參數量 :', model.num_parameters()) # 查看模型總參數量

question = '''問：鄭憲宗對於學校的長遠發展有何規劃？ 答：'''

# 分詞並準備模型輸入
inputs =  tokenizer(question, return_tensors="pt")

# 生成回答
output = model.generate(inputs["input_ids"], max_length=100, num_beams=2, no_repeat_ngram_size=2, early_stopping=True)

# 解碼生成的文本
answer = tokenizer.decode(output[0], skip_special_tokens=True)
print(answer)

# 出現 cuda 環境編譯錯誤，參考這裡 : https://www.baifachuan.com/posts/543c16ad.html
# 出現警告 : https://github.com/oobabooga/text-generation-webui/issues/1164 (執行pip install -i https://test.pypi.org/simple/ bitsandbytes-cuda113)

# 使用 LoRA 網路
from peft import LoraConfig, get_peft_model, TaskType, get_peft_model_state_dict

# Define LoRA Config
lora_config = LoraConfig(
 peft_type="LORA",
 task_type=TaskType.CAUSAL_LM,  # task_type, token classification (TaskType.CAUSAL_LM)
 inference_mode=False,
 r=16,                           # r, the dimension of the low-rank matrices
 lora_alpha=64,                 # lora_alpha, scaling factor for the weight matrices
 lora_dropout=0.05,              # lora_dropout, dropout probability of the LoRA layers
#  bias="lora_only"               # bias, set to only lora layers to train
)

# prepare int-8 model for training
# model = prepare_model_for_int8_training(model)

# add LoRA adaptor
model = get_peft_model(model, lora_config)
model.config.use_cache = False

model.print_trainable_parameters()

# 觀察可訓練參數
# for name, param in model.named_parameters():
#     if param.requires_grad:
#         print(f"Parameter: {name} is not frozen")
#     else:
#         print(f"Parameter: {name} is frozen")



from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
import torch

# 加載 Bloom 模型和分詞器，並應用 LoRA 改造（假設您已按前一段程式碼操作）
# ...

# 準備訓練數據
train_file = 'train.txt'  # 這應該是您的訓練數據文件
train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=train_file,
    block_size=128  # 可以根據需要調整塊大小
)
print()
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

# 設定訓練參數
output_dir = 'finetuned_bloom_model'  # 輸出目錄
training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,
    num_train_epochs=1000,  # 訓練週期
    per_device_train_batch_size=10,  # 每個設備的批次大小
    save_steps=10_000,  # 保存步數
    save_total_limit=10  # 最多保存模型數量
)

# 創建訓練器並開始訓練
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# 開始訓練
trainer.train()

# 保存微調後的模型
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)


# 用微調後的模型進行推論
from transformers import BloomForCausalLM
from transformers import BloomTokenizerFast
import torch

from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

model = None
hf_peft_repo = "./finetuned_bloom_model"
peft_config = PeftConfig.from_pretrained(hf_peft_repo)
model = AutoModelForCausalLM.from_pretrained(peft_config.base_model_name_or_path, return_dict=True)
tokenizer = AutoTokenizer.from_pretrained(peft_config.base_model_name_or_path)

# Load the finetuned Lora PEFT model
model = PeftModel.from_pretrained(model, hf_peft_repo)

# 分词并准备模型输入
inputs = tokenizer(question, return_tensors="pt")
input_ids = inputs["input_ids"]

# 设定生成参数
max_length = 100
eos_token_id = tokenizer.eos_token_id

# 预测
model.eval()
with torch.no_grad():
    output_ids = input_ids
    for _ in range(max_length):
        outputs = model(output_ids)
        next_token_logits = outputs.logits[:, -1, :]
        next_token_id = next_token_logits.argmax(1).unsqueeze(-1)
         # 检查是否生成了结束符
        if next_token_id[0] == 7979:
            break
        output_ids = torch.cat([output_ids, next_token_id], dim=-1)

       

# 解码生成的文本
answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print(answer)

