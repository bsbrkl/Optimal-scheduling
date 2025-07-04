import streamlit as st
import time
import random
from utils import youhua
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

st.title("优化调度")

with st.sidebar:
    nihao=st.text_input("请输入用户名：")
    if nihao:
        st.write(f"你好，{nihao}")
    st.markdown("[获取源码](https://github.com/bsbrkl/Optimal-scheduling)")
    st.markdown("[常规调度](https://github.com/bsbrkl/Optimal-scheduling)")
uploaded_file = st.file_uploader("选择一个文件",type=["xlsx", "xls"])
if 'df' not in st.session_state:  # 初始化session state
    st.session_state.df = None
if uploaded_file is not None:
    # 显示文件信息
    try:
        st.session_state.df = pd.read_excel(uploaded_file,sheet_name=None)
    except Exception as e:
        st.error(f"读取文件时出错: {e}")
else:
    st.info("请上传一个文件")
Np=(st.number_input('保证发电Np'))
low_h=st.number_input('死水位')
start_h=st.number_input('初水位')
end_h=st.number_input('末水位')
q_low=st.number_input('最小下泄流量')
n_max=st.number_input('最大出力')
years=int(st.number_input('时间跨度（多少年）'))
b=st.number_input('惩罚系数')
num=int(st.number_input('分割成多少份'))


if 'List' not in st.session_state:  # 初始化session state
    st.session_state.List = None

click1=st.button('开始')
if click1:
    with st.spinner('正在运行，请稍候...'):
        st.session_state.List = list(youhua(st.session_state.df,num,Np,low_h,start_h,end_h,q_low,years,b,n_max))
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
click3=st.button('画图')

if click3:
    fig, ax = plt.subplots()
    ax.plot(st.session_state.List[0],color='deepskyblue',label='水位Z')
    ax.plot(st.session_state.List[1],color='r',label='出力N')
    ax.plot(st.session_state.List[2],color='orange',label='出流Q')
    ax.plot(st.session_state.List[3],color='lightgreen',label='弃水q')
    ax.legend()
    st.pyplot(fig)


