import streamlit as st  #运行请使用 streamlit run
import os
from dotenv import load_dotenv
from openai import OpenAI
# 加载环境变量
load_dotenv()
# 初始化 OpenAI 客户端
client = OpenAI(
    api_key='ollama',
    base_url="http://localhost:11434/v1"
    # api_key=os.getenv("DEEPSEEK_API_KEY"),
    # base_url="https://api.deepseek.com/v1"
)
# 设置页面配置
st.set_page_config(
    page_title="DeepSeek 聊天助手",
    page_icon=" ",
    layout="wide"
)
# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个有帮助的AI助手"}
]
# 页面标题
st.title(" DeepSeek 聊天助手")
# 显示聊天历史
# 用户输入
if prompt := st.chat_input("请输入您的问题"):
    # 添加用户消息到历史
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
# 获取 AI 响应
with st.chat_message("assistant"):
    with st.spinner("思考中..."):
        response = client.chat.completions.create(
            model="deepseek-r1:7b",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1000,
            stream=False
)
        ai_response = response.choices[0].message.content
        st.markdown(ai_response)
# 添加 AI 响应到历史
st.session_state.messages.append({
    "role":	"assistant",
    "content": ai_response
    })
# 添加清除聊天按钮
if st.button("清除聊天历史"):
    st.session_state.messages = [
        {"role": "system", "content": "你是一个有帮助的AI助手"}]
