from VDB_API.nttu_llm import NTTU_tools
from VDB_API.utils import list_all_file_in_a_path, delete_information
import os

tools = NTTU_tools()
tools.vectordb_manager.set_vector_db("NTTU_db")
delete_information.delete_information()
file_path = list_all_file_in_a_path.list_all_files()
tools.add_documents_to_vdb(file_path)
#tools.set_llm_type("offline")
#query = "請問成功大學勝一舍每人學期住宿費是多少？"
#query = '柯文哲是誰?'
#query = '請問台東大學四人房的價格?'
#query = '台東大學畢業出路是不是很差?'
#query = '台東大學作為私立學校有什麼優勢嗎?'
#query = '台東大學的四人房相較於六人房貴多少錢?回答這個問題需要知道哪些資訊？'
query = '很油的蘋果派包裝可以回收嗎？'
ans, _, _ = tools.chat(query)
print("\n問答 : ")
print("Q : ", query)
print("A : ", ans)
tools.vectordb_manager.vectordb.delete_collection()
tools.vectordb_manager.vectordb.persist()