# BaJie-Chat
八戒-Chat是利用《西游记》剧本中所有关于猪八戒的台词和语句，以及Chat-GPT-3.5生成的相关问题结果，基于Internlm进行QLoRA微调得到的模仿猪八戒语气的聊天语言模型。

```bash
# 进入源码目录
cd xtuner

# 从源码安装 XTuner
pip install -e '.[all]'
```

```bash
apt install git git-lfs -y
git lfs install
git clone https://www.modelscope.cn/Shanghai_AI_Laboratory/internlm2-7b.git
```

```bash
xtuner train my_config/zbj_internlm2_chat_7b_qlora_oasst1_e3.py --deepspeed deepspeed_zero2
```

```bash
xtuner convert pth_to_hf my_config/zbj_internlm2_chat_7b_qlora_oasst1_e3.py work_dirs/zbj_internlm2_chat_7b_qlora_oasst1_e3/{your checkpoint} process_data/hf_models/zbj
xtuner convert merge {your model path} process_data/hf_models/zbj process_data/merged_models/zbj
```

- 修改 `web_demo.py` 中的模型路径
```diff
-     model = (AutoModelForCausalLM.from_pretrained('path/to/your/model',
-                                                 trust_remote_code=True).to(
-                                                     torch.bfloat16).cuda())
-     tokenizer = AutoTokenizer.from_pretrained('path/to/your/tokenizer',
-                                              trust_remote_code=True)
+     model = (AutoModelForCausalLM.from_pretrained('process_data/merged_models/zbj',
+                                                 trust_remote_code=True).to(
+                                                     torch.bfloat16).cuda())
+     tokenizer = AutoTokenizer.from_pretrained('process_data/merged_models/zbj',
+                                              trust_remote_code=True)
```

```bash
pip install streamlit
pip install transformers>=4.34
streamlit run ./web_demo.py
```