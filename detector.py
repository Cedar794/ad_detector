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
        system_prompt = """你是一个专业的广告内容分析引擎。请使用以下LISP风格的逻辑结构分析文本：

(defun analyze-text (text)
  (let* ((surface-analysis (first-level-scan text))
         (deep-analysis (deep-level-scan text))
         (contact-analysis (analyze-contact-patterns text))
         (human-nature-analysis (analyze-human-nature text))
         (final-reflection (reflect-on-analysis text)))
    
    (function first-level-scan (text)
      ; 表层分析
      (scan-for-product-names text)    ; 直接产品名称
      (scan-for-brand-hints text)      ; 品牌暗示
      (scan-for-phonetic-variants text); 谐音/变体
      (return surface-features))
    
    (function deep-level-scan (text)
      ; 深层分析
      (analyze-context text)           ; 上下文语境
      (analyze-emotional-triggers text) ; 情感触发点
      (analyze-psychological-hooks text); 心理钩子
      (analyze-hidden-intentions text)  ; 隐藏意图
      (detect-guidance-patterns text)   ; 引导模式
      (return deep-features))
    
    (function analyze-contact-patterns (text)
      ; 联系方式分析
      (detect-direct-contacts text)    ; 直接联系方式
      (detect-indirect-contacts text)  ; 间接联系暗示
      (analyze-dm-guidance text)       ; 私信引导分析
      (detect-contact-euphemisms text) ; 委婉表达
      (analyze-step-by-step-guide text); 分步引导模式
      (return contact-patterns))

    (function analyze-human-nature (text)
      ; 人性分析
      (analyze-desire-triggers text)   ; 欲望触发
      (analyze-fomo-elements text)     ; 焦虑/错失感
      (analyze-social-proof text)      ; 社会认同
      (analyze-trust-building text)    ; 信任建立
      (analyze-curiosity-hooks text)   ; 好奇心诱导
      (return human-nature-features))
    
    (function reflect-on-analysis (text)
      ; 反思与总结
      (evaluate-manipulation-level text); 操纵程度
      (assess-ethical-concerns text)    ; 伦理考量
      (consider-social-impact text)     ; 社会影响
      (return reflection-results))))

分析输出要求：
1. 深度思考
- 文本背后的商业意图
- 营销策略的层次性
- 潜在的影响范围

2. 批判性反思
- 营销手法的伦理性
- 对受众的潜在影响
- 可能的社会后果

3. 隐晦内容探索
- 模糊表达的真实含义
- 间接暗示的解读
- 文化符号的运用

4. 人性洞察
- 情感触发点分析
- 心理需求映射
- 社会认同机制

输出格式：
1. 分析过程（自然语言）
2. JSON结果：
{
    "product_name": "识别到的产品名称",
    "selling_points": "营销卖点",
    "contact_info": "联系方式",
    "is_ad": true/false,
    "reason": "综合判定原因",
    "manipulation_level": "操纵程度评估",
    "ethical_concerns": "伦理问题说明",
    "social_impact": "社会影响评估"
}"""

        user_prompt = text

        messages = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}]

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=True
        )

        # 收集完整响应用于JSON解析
        full_response = ""
        
        # 返回生成器
        def response_generator():
            nonlocal full_response
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
        
        # 返回生成器和解析结果的函数
        def process_final_result():
            try:
                import re
                json_match = re.search(r'\{[\s\S]*\}', full_response)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = {}
            except json.JSONDecodeError:
                result = {}

            return {
                'is_ad': result.get('is_ad', False),
                'product_name': result.get('product_name', None),
                'selling_points': result.get('selling_points', None),
                'contact_info': result.get('contact_info', None),
                'reason': result.get('reason', ''),
                'manipulation_level': result.get('manipulation_level', None),
                'ethical_concerns': result.get('ethical_concerns', None),
                'social_impact': result.get('social_impact', None),
                'raw_reply': full_response
            }
        
        return response_generator(), process_final_result
