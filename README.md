# 🕵️‍♂️ 无敌铲子王

一个基于人工智能的工具，帮助检测文本中的软广告内容。  
AI Open Day活动作品，仅用于学习交流。  

**作者、作品信息：**  
- 姓名：张悦（小兑）  
- 学校：上海外国语大学  
- 修改时间：2024/12/07

**友情链接：**  
- [AI Open Day](https://qa3dhma45mc.feishu.cn/docx/FWaXdcIfZo8BljxcD2Dc8XOvnEd)

## 📝 项目简介

无敌铲子王是一个使用 Streamlit 开发的 Web 应用，能够智能识别文本中可能包含的广告内容。它通过深度分析文本特征，帮助用户快速判断内容是否包含商业推广、诱导私聊等营销特征。

## ✨ 主要功能

- 文本广告智能检测
- 实时分析过程展示
- 多维度深度分析
  - 产品名称识别
  - 营销卖点提取
  - 诱导联系识别
  - 操纵程度评估
  - 伦理问题分析
  - 社会影响评估

## 🛠️ 技术栈

- Python
- Streamlit
- DeepSeek API
- OpenAI 客户端

## 🚀 如何使用

1. 克隆项目到本地
```bash
git clone https://github.com/Cedar794/ad_detector.git
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置API密钥：
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
3. 系统将展示实时分析过程
4. 获取详细的检测结果，包括：
   - 基础检测结果
   - 产品信息识别
   - 营销特征分析
   - 深度分析报告

## 📋 检测标准

系统采用多层次分析框架：

### 表层分析
- 产品名称识别
- 品牌暗示检测
- 谐音/变体识别

### 深层分析
- 上下文语境理解
- 情感触发点识别
- 心理钩子检测
- 隐藏意图分析
- 引导模式识别

### 人性分析
- 欲望触发点
- 焦虑/错失感营造
- 社会认同机制
- 信任建立手法
- 好奇心诱导策略