import streamlit as st
from detector import TextDetector

def main():
    st.title("🕵️‍♂️ 无敌铲子王")
    
    st.write("请输入文字，AI将帮您检测是否包含软广告内容。")
    
    # 创建检测器实例
    text_detector = TextDetector()
    
    # 文字输入区
    text_input = st.text_area("请输入要检测的文字:", height=150)
    
    if st.button("开始检测"):
        if text_input:
            with st.spinner('🔍 正在仔细检测中，请稍候...'):
                st.divider()
                
                # 预处理文本
                cleaned_result = text_detector.preprocess_text(text_input)
                
                # 显示清洗后的文本
                st.subheader("🧹 清洗后的文本：")
                if cleaned_result == "无广告内容":
                    st.write(text_input)  # 显示原始文本
                    st.success("✅ 清洗后未发现广告相关内容，直接进行深度处理。")
                else:
                    st.write(cleaned_result)  # 显示清洗后的文本
                    st.info("🔍 清洗后发现广告相关内容，进行深度处理。")
                
                # 获取生成器和处理函数
                stream_generator, process_result = text_detector.detect(text_input)  # 传入原始文本
                
                # 创建占位符用于流式输出
                thinking_header = st.subheader("💭 思考过程：")
                thinking_placeholder = st.empty()
                
                # 流式输出思考过程
                full_thinking = ""
                for chunk in stream_generator:
                    full_thinking += chunk
                    thinking_placeholder.markdown(full_thinking)
                
                # 处理最终结果
                result = process_result()
                st.divider()
                display_result("文字", result)
        else:
            st.warning("请输入文字后再检测！")

def display_result(input_type, result):
    st.subheader(f"{input_type}检测结果：")
    
    if result['is_ad']:
        st.error("⚠️ 检测到疑似广告内容！")
        
        # 显示详细信息
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if result['product_name']:
                st.info("🏷️ 产品名称")
                st.write(result['product_name'])
                
        with col2:
            if result['selling_points']:
                st.info("✨ 产品卖点")
                st.write(result['selling_points'])
                
        with col3:
            if result['contact_info']:
                st.info("📱 诱导联系")
                st.write(result['contact_info'])
        
        st.write("📝 判定原因：", result['reason'])
        
        # 添加新的分析维度
        st.divider()
        st.subheader("🔍 深度分析")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            if result.get('manipulation_level'):
                st.warning("🎯 操纵程度")
                st.write(result['manipulation_level'])
                
        with col5:
            if result.get('ethical_concerns'):
                st.warning("⚖️ 伦理问题")
                st.write(result['ethical_concerns'])
                
        with col6:
            if result.get('social_impact'):
                st.warning("🌍 社会影响")
                st.write(result['social_impact'])
    else:
        st.success("✅ 未检测到广告内容")

if __name__ == "__main__":
    main() 