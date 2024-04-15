from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from opencc import OpenCC

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True).eval()

def qwen(text, model=model, tokenizer=tokenizer, history = None):
    ts = OpenCC('t2s')
    st = OpenCC('s2t')
    message = ts.convert(text)
    response, history = model.chat(tokenizer, message, history=history)
    response = st.convert(response)
    return(response, history)


if __name__ == '__main__':
    question_template = '''請依照範例將問題拆解成小問題：
    範例：台東大學的四人房相較於六人房貴多少錢?
    1. 台東大學的四人房價格是多少？
    2. 台東大學的六人房價格是多少？
    3. 兩者價格相差多少錢？
    '''
    response, history = qwen('台東大學的四人房相較於六人房貴多少錢？')
    
    
