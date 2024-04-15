import os
import shutil


# 刪除資料夾內所有內容
def delete_information(folder_path = 'home/n66104571/NLP/chroma_db'):
    for filename in os.listdir(folder_path = folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # 刪除檔案或連結
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 刪除子資料夾及其所有內容
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

