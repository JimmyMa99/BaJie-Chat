# 临时demo ,配置已更新，进去全部更新完毕！！

import os
base_path = './JimmyMa99/BaJie-Chat-llama3_1-8b'
#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('JimmyMa99/BaJie-Chat-llama3_1-8b',cache_dir='./')
os.system(f'cd .. && pip install lmdeploy')
os.system(f'lmdeploy serve gradio {base_path} --model-name llama3 --server-port 7860')
