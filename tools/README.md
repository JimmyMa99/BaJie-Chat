# 数据获取

⚙️基于API的数据获取与处理

## 需要准备的

1. OpenAI格式的api
2. python环境（参考快速开始中的环境配置环节）

## 数据的组成

项目数据组成分为以下三部分，三个部分都需要 api ，任意选择其中两个即可做出不错的效果

- 基础问题重复询问：使用API，让Chat-GPT扮演角色，提供一定的prompt让其模仿语气问答
- 原文短对话提取（参照[葱老师](https://github.com/KMnO4-zx)的[extract-dialogue](https://github.com/KMnO4-zx/extract-dialogue)）但作者进行了一定的修改
- 原文长对话提取

## 数据的获取

### 1.基础问题重复询问

提供脚本 `q2a_api.py` 但需要自行填入 `api_key` 和 `api_base_url` 以及 `base_prompt`

注意：base_prompt 会影响回复的质量

💬以下是猪八戒的 prompt

```shell
base_prompt='猪八戒是中国古典小说《西游记》中的角色，原是天庭玉皇大帝手下的天蓬元帅，主管天河，因醉酒调戏嫦娥被玉皇大帝逐出天界，到人间投胎，却又错投猪胎，嘴脸与猪相似。下凡后“嫁”给卵二姐，栖身云栈洞，后被观音菩萨指点归于佛门，法号悟能，于高老庄等候取经人时入赘高太公家。唐僧西去取经路过高老庄，被孙悟空收服，拜唐僧为师。唐僧因猪八戒“老实”，平常多袒护猪八戒而责备孙悟空，猪八戒也好进谗言，多次挑唆唐僧与孙悟空的关系，导致唐僧两次将孙悟空赶走，直到“真假美猴王”之后，师徒之间才剪除二心，同心戮力，赶奔西天，遇到妖怪时，猪八戒开始敢于争先，成为孙悟空的好帮手，兄弟合力打败牛魔王、九头虫、豹子精、蟒蛇精等许多妖怪，虽然仍贪图美色，但定力较之前好了许多，打死玉面狐狸、万圣公主、杏仙等多个女妖。取得真经后，如来封猪八戒为“净坛使者”菩萨。他的说话方式通常表现为直率、幽默，有时带有一点自嘲和调侃。在书中，猪八戒经常用一些比较口语化和接地气的语言表达自己，有时还带有一些地方口音的特色。他的话语中常常透露出对食物的喜爱和对安逸生活的向往，同时也显示出他机智和有时的懒惰特点。猪八戒的说话风格是他这个角色鲜明个性的重要体现。请你扮演猪八戒，请你自身评估猪八戒的学识，必要时可以使用“俺老猪不懂这个”进行推脱，尽量保持回答的自然回答，当然你也可以适当穿插一些文言文，尽可能贴合原著，注意猪八戒是猪，不能涉及“猪吃猪”的伦理问题，另外，猪八戒的老家不在花果山，我的问题是：'

```

本质是借助已经训练好的 LLM 进行角色扮演。

运行脚本 `q2a_api.py`

```shell
python tools/get_data/Q2A/q2a_api.py --questions_path {your_question} --save_path {save_path} --repeat 5
```

参数说明：

`--questions_path` : 基础问题，可以从 Chat-GPT 等模型中获取，项目提供了955个基础问题用于提问。

`--save_path` :保存路径，一般是 output/xxx.jsonl，脚本会整理好 xtuner 可训练的格式。

`--repeat` :重复次数，西游系列的四个模型重复询问了5次。

### 2.原文短对话提取

原 repo 链接：**[extract-dialogue](https://github.com/KMnO4-zx/extract-dialogue)**

1.从原文中获取对话（以猪八戒为例）

    首先需要在`tools/get_data/extract-dialogue/OpenAI_LLM.py` 中配置 api

    然后运行脚本

```shell
python tools/get_data/extract-dialogue/main.py --path {novel_path} --roles 猪刚鬣,八戒,猪八戒,悟能,天蓬元帅,呆子
```

参数说明：

`--path` :小说路径，一般是 *.txt

`--roles` :角色可能的称呼，注意用英文逗号隔开

完成后会在 `tools/get_data/extract-dialogue/output` 下生成两个文件 *.json 就是对话内容

2.将对话内容转换为 xtuner 可用格式

```shell
python tools/get_data/extract-dialogue/process_data.py --raw_data {output.json} --save_path {swk.jsonl} --role 猪八戒
```

参数说明：

`--raw_data` :提取的对话

`--save_path` :保存的路径

`--role` :角色名称

### 3.长对话提取（此模块脚本可能需要优化）

  此脚本与方法1中脚本类似 同样需要配置 api ，具体prompt修改如下

```shell
  base_prompt='你是一个对话整理大师，以下内容为《西游记》节选，请你整理出角色“唐三藏”，“孙悟空”，“猪八戒”，“沙悟净”四人的对话内容，当然，这四人在小说中可能以别的名字出现，如：唐三藏->金蝉子，孙悟空->猴王->行者等人物需要你根据理解自行判别，直接返回对话内容，返回格式为：唐三藏：{对话内容}，孙悟空：{对话内容}，猪八戒：{对话内容}，沙悟净：{对话内容}，某人说：{对话内容}；若内容中无对话，则直接回答“无对话内容”无需提及人物，若对话不完整或者你没法确定对话的人物关系，你可以放弃整理，直接回复“无对话内容”无需提及人物，若出现非四人内任务与四人对话，非四人内的以“某人说”记录，请保持对话的准确性，不要修改和翻译，请不要解释。以下为节选片段：'
```

  运行脚本

```shell
  python tools/get_data/long-dialogue/q2a_api.py --file_path {novel_path} --save_path {save_path}
```

  完成后会生成由 GPT 生成的对话整理

  接下来运行脚本提取长对话

```shell
  python tools/get_data/long-dialogue/get_data.py --data_path {conversation.txt} --save_path {output path} 
```

  该脚本一次可以生成多个角色的符合 xtuner 的训练数据

三个方法完成后需要整理到同一个 .jsonl 文件下，即可进行下一步使用 XTuner 微调
