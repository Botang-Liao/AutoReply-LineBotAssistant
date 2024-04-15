import json
from copy import deepcopy
from typing import Any, Dict, List, Tuple, Union

from dotenv import load_dotenv
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_openai import ChatOpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from VDB_API.agent.gpt_api import llm_agent
from VDB_API.agent.tool_config import TOOLS
from VDB_API.utils import file_processor
from VDB_API.utils.config import (CHAT_MODELS, DEVICE, PROMPT_TEMPLATE)
from VDB_API.vectordb_manager import VectordbManager
from VDB_API.utils.transfer_chinese import traditional_to_simplified, simplified_to_traditional


load_dotenv()  # 加載.env檔案


class NTTU_tools:
    def __init__(self):
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            CHAT_MODELS["offline"], trust_remote_code=True
        )
        #self.llm = self.set_llm("offline")
        self.llm =  AutoModelForCausalLM.from_pretrained(
            CHAT_MODELS["offline"], device_map="auto", trust_remote_code=True
        ).eval()
        self.vectordb_manager = VectordbManager()
        self.file_path = []
        self.files = []
        
    def set_llm(self, llm_type: str):      
        print("Your device: ", DEVICE)
        model = AutoModelForCausalLM.from_pretrained(CHAT_MODELS[llm_type], trust_remote_code=True, device_map = 'auto').eval()
        # inputs = self.tokenizer.encode("你今天好嗎?", return_tensors="pt").to("cuda")
        # outputs = model.generate(inputs)
        # print(self.tokenizer.decode(outputs[0]))
        pipe = pipeline(
            "text-generation",
            model=model.to(DEVICE),
            tokenizer=self.tokenizer,
            max_new_tokens=100,
            #device=DEVICE,
        )
        print("set chat model to ", CHAT_MODELS[llm_type])
        return HuggingFacePipeline(pipeline=pipe)
    
    def add_documents_to_vdb(self, file_paths: List[str]):
        """
        Arg:
            file_paths: 文件路徑 list (需含檔名)
        """
        self.file_path = file_paths
        print('file_paths :', self.file_path)
        for file_path in file_paths:
            texts, file_name = file_processor.get_split_data(file_path)
            self.files.append(file_name)
            self.vectordb_manager.add(texts)
                 
    def chat(self, query: str):
        docs = []
        tmp_docs = self._search_vdb(query)
        docs = file_processor.add_unique_docs(docs, tmp_docs)
        ans = self._get_llm_reply(query, docs)
        contents, metadatas = [], []
        for doc in docs:
            tmp_content = doc.page_content.split("--")
            tmp_content = "".join(tmp_content[1:])
            contents.append(tmp_content)
            metadatas.append(doc.metadata)
        return ans, contents, metadatas
    
    def _search_vdb(self, query):
        where = self._get_filter(self.files)
        #print('where', where)
        docs = self.vectordb_manager.query(query, n_results=3, where=where)
        #print('docs :', docs)
        return docs
    
    def _get_filter(self, file_list) -> Union[Dict[str, Any], None]:
        if len(file_list) == 1:
            return {"source": file_list[0]}
        elif len(file_list) > 1:
            return {"$or": [{"source": name} for name in file_list]}
        else:
            raise ValueError("file_list is empty")
        
    def _get_llm_reply(self, query, docs):
        templated_query = PROMPT_TEMPLATE.format(query=query)
        # ans = self.chain.invoke(
        #     {"input_documents": docs, "question": templated_query},
        #     return_only_outputs=True,
        # )["output_text"]
        # ans = ans.split("\nSOURCES:")[0]
        contents = ""
        for doc in docs:
            contents += doc.page_content + "\n"
        question = traditional_to_simplified(f"[參考資料] {contents} \n" + templated_query)
        #question = self.ts.convert(templated_query)
        #print('Q :', question)
        print(question)
        ans, _ = self.llm.chat(self.tokenizer, question, history=None)
        #print('A :', ans)
        ans = simplified_to_traditional(ans)
        return ans
    
 