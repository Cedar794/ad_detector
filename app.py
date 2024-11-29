import streamlit as st
from detector import TextDetector

def main():
    st.title("🕵️‍♂️ AI广告检测助手")
    
    st.write("请输入文字，AI将帮您检测是否包含软广告内容。")
    
    # 创建检测器实例
    text_detector = TextDetector()
    
    # 文字输入区
    text_input = st.text_area("请输入要检测的文字:", height=150)
    
    if st.button("开始检测"):
        if text_input:
            with st.spinner('🔍 正在仔细检测中，请稍候...'):
                st.divider()
                result = text_detector.detect(text_input)
            display_result("文字", result)
            
        else:
            st.warning("请输入文字后再检测！")

def display_result(input_type, result):
    st.subheader(f"{input_type}检测结果：")
    
    if result['is_ad']:
        st.error("⚠️ 检测到疑似广告内容！")
        st.write("原因：", result['reason'])
    else:
        st.success("✅ 你是个好人！未检测到广告内容。")

if __name__ == "__main__":
    main() 