import json
from openai import OpenAI
import streamlit as st
class TextDetector:
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets["APIKEY"]["deepseek_api_key"], base_url="https://api.deepseek.com/")
        pass
    
    def detect(self, text):
        """
        调用API检测文字中的广告内容
        返回格式: {'is_ad': bool, 'reason': str}
        """
        system_prompt = """
        (defun detect-ad (text)
          "分析文本是否包含广告内容，返回JSON格式结果"
          
          ;; 示例广告文本特征:
          ;; - 引导私聊/加好友
          ;; - 暗示利益/福利
          ;; - 神秘/诱导性表达
          ;; - 商业推广意图
          
          ;; JSON返回格式示例:
          ;; {
          ;;   "is_ad": true/false,      // 是否为广告
          ;;   "reason": "string"        // 判定原因说明
          ;; }
          
          ;; 广告文本示例:
          ;; 1. "这件事情挺有意思的，想了解更多的可以私聊我哦"
          ;; 2. "最近发现一个不错的资源，有需要的可以找我聊聊"
          ;; 3. "想给大家分享个小福利，感兴趣的加我了解"
          
          ;; 请分析输入文本是否包含:
          ;; 1. 引导私聊/添加联系方式
          ;; 2. 暗示利益/福利
          ;; 3. 模糊诱导表达
          ;; 4. 商业推广意图
          
          ;; 如发现以上特征，判定为广告，并说明原因
          )
        """

        user_prompt = text

        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}]

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={
                'type': 'json_object'
            }
        )

        result = json.loads(response.choices[0].message.content)
        return {
            'is_ad': result.get('is_ad', False),
            'reason': result.get('reason', '')
        }
