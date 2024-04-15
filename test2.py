from transformers import BloomForCausalLM
from transformers import BloomTokenizerFast

checkpoint = "ckip-joint/bloom-1b1-zh"
model = BloomForCausalLM.from_pretrained(checkpoint)
tokenizer = BloomTokenizerFast.from_pretrained(checkpoint)

def gen(prompt, result_length):
    inputs = tokenizer(prompt, return_tensors="pt")
    return tokenizer.decode(model.generate(inputs["input_ids"],
                           max_length=result_length,
                           num_beams=2,
                           no_repeat_ngram_size=2,
                           early_stopping=True
                          )[0])

while True:
    prompt = input("prompt: ")
    length = int(input("length: "))
    result = gen(prompt, length)
    print(result)