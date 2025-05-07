import streamlit as st
import time
import random
from utils import youhua
import pandas as pd

st.write("你好")
uploaded_file = st.file_uploader("选择一个文件",type=["xlsx", "xls"])
if uploaded_file is not None:
    # 显示文件信息
    try:
        st.write("文件名:", uploaded_file.name)
        st.write("文件类型:", uploaded_file.type)
        st.write("文件大小:", uploaded_file.size, "bytes")
    except Exception as e:
        st.error(f"读取文件时出错: {e}")

Np=(st.number_input('保证发电Np'))
low_h=st.number_input('死水位')
start_h=st.number_input('初水位')
end_h=st.number_input('末水位')
q_low=st.number_input('最小下泄流量')
n_max=st.number_input('最大出力')
years=int(st.number_input('时间跨度（多少年）'))
b=st.number_input('惩罚系数')
num=int(st.number_input('分割成多少份'))
df=pd.read_excel(uploaded_file,sheet_name=None)

if 'List' not in st.session_state:  # 初始化session state
    st.session_state.List = None

click1=st.button('开始')
if click1:
    with st.spinner('正在运行，请稍候...'):
        st.session_state.List = list(youhua(df,num,Np,low_h,start_h,end_h,q_low,years,b,n_max))
    st.success('完成!')

click2=st.button('展示')
if click2:
    df_list=pd.DataFrame(st.session_state.List)
    df_list = df_list.rename(index={
        0: '水位',
        1: '出力',
        2: '出流',
        3: '弃水'
    })

    st.dataframe(df_list)



