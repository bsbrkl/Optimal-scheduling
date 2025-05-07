import pandas as pd
import numpy as np

def youhua(df,num,Np,low_h,start_h,end_h,q_low,years,b,n_max):
    # df = pd.read_excel("C:\\Users\\90384\\Desktop\\水电站\data_ty.xls", sheet_name=None)
    df1=df["泄流特性曲线"]
    df2=df['水位库容关系']
    df2["V"]=df2["V"]
    df3=df['天一调度图控制水位']
    df4=df["尾水流量关系"]
    df5=df["历史径流"]

    Z=[]
    Q=[]
    n=num+1
    Q_qishui=[]
    Z_list2=[0]*n
    Z_list1=[end_h]*n
    Z_list=[]
    Q_list=[]
    Z_list3=[]
    Q_qishui2=[]
    for i in range(n):
        Z_list.append([])
        Z_list3.append([])
    N_list1=[]
    N_list2=[]
    for i in range(n):
        N_list1.append([])
        N_list2.append([])
    for i in range(n):
        Q.append([])
        Q_list.append([])
        Q_qishui.append([])
        Q_qishui2.append([])
    def k_quzhi(h):
        if h<=60:
            return 8.5
        if 60<=h<=70:
            return 8.5
        if 70<=h<=80:
            return 8.5
        if 80<=h<=90:
            return 8.8
        if 90<=h<=100:
            return 9.1
        if 100<=h<=110:
            return 9.2
        if h>=110:
            return 9


    Nmax = 0
    Z_max = 0

    for j in range(years-1, -1, -1):
        for i in range(11, -1, -1):

            # if j==0 and i==0:
            #     break
            # if j==0 and i==1:
            #     break
            Q1 = df5.loc[j][i + 1]
            for m in range(len(Z_list2)):
                Z_list2[m] = (df3["1.5倍"][i] - low_h) / num * m + low_h
            for k in range(len(Z_list2)):
                Zt1 = Z_list2[k]
                if j==0 and i==0:
                    Zt1=start_h
                Q_max=0
                N_max = -1000000000000
                Nmax = 0
                Z_max = 0
                Q_qi_max=0
                Q_qi=0
                for a in range(len(Z_list1)):
                    Zt2 = Z_list1[a]
                    Vt1 = np.interp(Zt1, df2["Z"], df2['V'])
                    Vt2 = np.interp(Zt2, df2["Z"], df2['V'])
                    Q2 = Q1 - (Vt2 - Vt1) / (30.4 * 24 * 3600 / 100000000)

                    Z_low = np.interp(Q2, df4["Q"], df4["Z"])
                    H_loss = 2.08 * (Q2 / 4) ** 2 / 100000
                    Z_mean = (Zt1 + Zt2) / 2
                    H = Z_mean - Z_low - H_loss * 4

                    h = int(H)
                    K = k_quzhi(h)
                    N = K * Q2 * H / 1000
                    Q_qi = 0
                    if Q2 < q_low:
                        N = N - 100000000000


                    elif Q2 > 5 * np.interp((Zt1 + Zt2) / 2, df1["Z（m）"], df1["全开"]):
                        N = N - 100000000000


                    elif N < 0.75 * Np:
                        N = N - 100000000000

                    elif N < Np:
                        N = N + b * (N - Np)

                    elif N >= n_max:
                        N = n_max
                        Q_qi = Q2 - N / K / H * 1000


                    if N + sum(N_list1[a]) > N_max:
                        N_max = N + sum(N_list1[a])
                        Nmax = N
                        Z_max = Zt2
                        a_max = a
                        Q_max=Q2
                        Q_qi_max=Q_qi

                N_list = []
                N_list = list(N_list1[a_max])
                N_list.append(Nmax)
                N_list2[k] = N_list.copy()
                Z = []

                Z = list(Z_list3[a_max])
                Z.append(Z_max)
                Z_list[k] = Z.copy()

                Q_list1 = []
                Q_list1 = list(Q_list[a_max])
                Q_list1.append(Q_max)
                Q[k] = Q_list1.copy()

                Q_qishui1 = []
                Q_qishui1 = list(Q_qishui2[a_max])
                Q_qishui1.append(Q_qi_max)
                Q_qishui[k] = Q_qishui1.copy()

            Q_list=Q.copy()
            Q_qishui2=Q_qishui.copy()
            Z_list3 = Z_list.copy()
            Z_list1 = Z_list2.copy()
            N_list1 = N_list2.copy()
    return Z_list[0],N_list2[0],Q[0],Q_qishui[0]


# df_Z = pd.DataFrame(Z_list)
# df_N = pd.DataFrame(N_list2)
# df_Q = pd.DataFrame(Q)
# df_Q_qishui = pd.DataFrame(Q_qishui)
# df_Z.to_excel("z-output37.xlsx", index=False)
# df_N.to_excel("n-output37.xlsx", index=False)
# df_Q.to_excel("q-output37.xlsx", index=False)
# df_Q_qishui.to_excel("qi-output37.xlsx", index=False)



