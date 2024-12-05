import json
from openai import OpenAI
import streamlit as st
class TextDetector:
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets["APIKEY"]["deepseek_api_key"], base_url="https://api.deepseek.com/")
        pass
    
    def preprocess_text(self, text):
        """
        预处理文本，清洗掉可能干扰判断的内容
        """
        system_prompt = """你是一个文本清洗专家。请分析输入的文本，提取出所有可能与广告相关的内容。
特别注意：
1. 即使文本主要在讨论其他话题，也要留意其中可能包含的广告信息
2. 寻找可能的品牌名称、产品信息、促销活动或联系方式
3. 注意分析可能被其他内容"包裹"的广告信息
4. 保留所有可疑的字符串组合，它们可能是编码过的广告信息
5. 格外注意肯德基疯狂星期四广告内容：
    1. 直接提及（如：KFC、肯德基、疯狂星期四等）
    2. 谐音梗（如：肯帝基、k记等）
    3. 星期四文案（如：V我50、V我XX等）
    4. 类似文案（如：疯四、疯4等）

输出要求：
- 只输出可能与广告相关的文本片段
- 如果发现多个片段，用换行符分隔
- 如果没有发现任何相关内容，输出"无广告内容"五个字，不要输出其他任何内容
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        
        return response.choices[0].message.content

    def detect(self, text):
        # 首先进行预处理
        cleaned_result = self.preprocess_text(text)
        # 如果预处理返回"无广告内容"，则使用原始文本
        cleaned_text = text if cleaned_result == "无广告内容" else cleaned_result

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
      ; 增强品牌识别
      (detect-ambiguous-brand-names text) ; 检测模糊品牌名称
      (analyze-industry text)          ; 分析可能的行业
      (return surface-features))
    
    (function analyze-industry (text)
      ; 行业分析
      (detect-industry-keywords text)  ; 检测行业关键词
      (analyze-context-for-industry text) ; 上下文行业分析
      (return industry-features))
    
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
      ; 增强联系方式识别
      (detect-implied-contact-methods text) ; 检测隐含的联系方法
      (analyze-dm-guidance text)       ; 私信引导分析
      (detect-contact-euphemisms text) ; 委婉表达
      (detect-symbol-number-mix text)  ; 符号和数字和谐音字混合
      (detect-number-patterns text)    ; 号码模式识别
      (return contact-patterns))

特别注意以下隐晦表达方式：
1. 品牌暗示：
   - 常见品牌的模糊表达（如 "K。。F？？？C" 可能是 "KFC"）
   - 使用符号或变体来掩盖品牌名称

2. 疯狂星期四广告识别：
   - 直接提及词：KFC、肯德基、疯狂星期四
   - 谐音变体：肯帝基、k记、K记、开封菜
   - 星期四相关：V我50、V我XX、v50、V50
   - 变体表达：疯四疯4、疯狂4、疯子星期四
   - 组合识别：将品牌名与星期四相关表达结合分析

3. 谐音/变体：
   - 文字谐音（如 "豪赤" 可能是 "好吃"）
   - 同音字替换
   - 近音字替换

4. 符号替代：
   - 表情符号数字(如 1️⃣ = 1)
   - 特殊符号替代(如 🈚️ = 5)
   - 其他Unicode字符替代数字

5. 谐音替换：
   - 文字谐音(如 "妻" = 7, "妻妻" = 77)
   - 同音字替换
   - 近音字替换

6. 号码模式识别：
   - 中国大陆手机号规律：1xx-xxxx-xxxx
   - QQ号规律：5-6位(早期)或10-11位(现代)数字
   - 需要将所有可能的替代字符还原为数字
   - 检查还原后的数字是否符合手机号或QQ号规则

7. 组合识别：
   - 将符号替代和谐音替换组合分析
   - 识别完整的联系方式模式
   - 验证是否构成有效的通讯号码

8. 私信暗示：
   - 使用“滴滴”、“dd”等词模仿电话铃声，暗示私信联系
   - 识别此类常见的隐晦表达方式

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
      ; 增强反思
      (consider-brand-and-contact-clarity text) ; 考虑品牌和联系方式的清晰度
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
    "product_name": "识别到的产品名称，如果不确定但有暗示，请使用'产品名（可能）'的格式，例如'hood卡（可能）'。即使不完全确定也要尽可能填写，如果完全没有则填写'无'",
    "selling_points": "营销卖点，如果没有则填写'无'",
    "contact_info": "联系方式，如果暗示私信等间接联系方式，也请填写，例如'微信联系（暗示）'，如果没有则填写'无'",
    "is_ad": "布尔值，判定规则：当且仅当 product_name、selling_points、contact_info 都不为'无'时，才为 true，否则为 false",
    "reason": "综合判定原因",
    "manipulation_level": "操纵程度评估",
    "ethical_concerns": "伦理问题说明",
    "social_impact": "社会影响评估"
}

注意：
- 产品名称即使不完全确定也要填写，使用"（可能）"标注
- 联系方式即使是暗示性的也要填写，使用"（暗示）"标注
- 避免使用"未识别"或"未提供"等模糊表述
"""

        user_prompt = cleaned_text

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

            # 确保 is_ad 的值根据 product_name, selling_points, contact_info 正确设置
            product_name = result.get('product_name', '无')
            selling_points = result.get('selling_points', '无')
            contact_info = result.get('contact_info', '无')

            is_ad = (product_name != '无' and selling_points != '无' and contact_info != '无')

            return {
                'is_ad': is_ad,
                'product_name': product_name,
                'selling_points': selling_points,
                'contact_info': contact_info,
                'reason': result.get('reason', ''),
                'manipulation_level': result.get('manipulation_level', None),
                'ethical_concerns': result.get('ethical_concerns', None),
                'social_impact': result.get('social_impact', None),
                'raw_reply': full_response
            }
        
        return response_generator(), process_final_result
