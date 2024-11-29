# 🕵️‍♂️ AI广告检测助手

一个基于人工智能的工具，帮助检测文本中的软广告内容。

## 📝 项目简介

AI广告检测助手是一个使用Streamlit开发的Web应用，能够智能识别文本中可能包含的广告内容。它可以帮助用户快速判断内容是否包含商业推广、诱导私聊等营销特征。

## ✨ 主要功能

- 文本广告检测
- 实时分析反馈
- 详细的检测原因说明

## 🛠️ 技术栈

- Python
- Streamlit
- DeepSeek API
- PIL (Python Imaging Library)

## 🚀 如何使用

1. 克隆项目到本地：
```bash
pip install -r requirements.txt
```
2. 配置API密钥：
   - 在项目根目录创建 `.streamlit/secrets.toml` 文件
   - 添加你的DeepSeek API密钥
   - 示例：
   ```toml
   [APIKEY]
   deepseek_api_key = "your_deepseek_api_key"
   ```
4. 运行应用
```bash
streamlit run app.py
```

## 💡 使用说明

1. 在文本框中输入需要检测的内容
2. 点击"开始检测"按钮
3. 系统将自动分析内容并给出检测结果
4. 如果检测到广告内容，系统会提供具体的判定原因

## 📋 检测标准

系统主要识别以下特征：
- 引导私聊/添加联系方式
- 暗示利益/福利
- 模糊诱导表达
- 商业推广意图