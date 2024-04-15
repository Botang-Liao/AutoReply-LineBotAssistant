from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from opencc import OpenCC

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True).eval()
ts = OpenCC('t2s')
st = OpenCC('s2t')
history = None



text = "請介紹你自己"
message = ts.convert(text)
response, history = model.chat(tokenizer, message, history=history)
response = st.convert(response)
print(response)

text = "請問我剛剛問什麼"
message = ts.convert(text)
response, history = model.chat(tokenizer, message, history=history)
response = st.convert(response)
print(response)
print('='*10)
print(history)
