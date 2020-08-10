#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import math


# In[14]:


def datalist(df):
    df.dropna(axis=1,how = 'all', inplace = True) # 去除空列，合并数据
    df.dropna(axis=0,how = 'all', inplace = True) # 去除空行
    a = np.sort(df.columns)
    b = np.sort([ '客户数', '响应数','占比（%）'])
    c = np.sort(['预测概率', '实际值'])
    
    # 判断数据输入类型 蓝底数据
    # if len(df.columns) == 3:
    if all(x1 == x2 for (x1, x2) in zip(a, b)): # 手动测试True，但是在此处被判定为False
        # 初始化
        cn = [] # customer number 客户数
        rn = [] # response number 响应数
        rr = [] # response ratio, 响应率
        crr = [] # cumulative rr， 累计响应率
        lift = [] # 提升度

        for i in np.arange(len(df)): # 计算 响应率 和 累计响应率
            k = df.iloc[i][['客户数','响应数']] # 获取单次遍历数据
            cn.append(k[0]) # 储存数据
            rn.append(k[1]) 
            rr.append(round(k[1]/k[0],3)) 
            crr.append(round(sum(rn)/sum(cn),3)) # 保留三位小数，即百分比形势下保留一位小数

        for i in crr: # 计算 提升度
            lift.append(round(i/crr[-1],1))

        # 数据储存
        df1 = df.copy()
        df1['响应率'] = rr
        df1['累计响应率'] = crr
        df1['提升度'] = lift

    # 判断为 黄底数据
    # elif len(df.columns) == 2:
    elif all(x1 == x2 for (x1, x2) in zip(a, c)):
        df1 = pd.DataFrame(columns=[ '占比（%）', '客户数', '响应数', '响应率', '累计响应率', '提升度'])  # 新建空dataframe
        ratio = np.arange(0.05,1.01,0.05)

                # 初始化
        cn = [] # customer number 客户数
        rn = [] # response number 响应数
        rr = [] # response ratio, 响应率
        crr = [] # cumulative rr， 累计响应率
        lift = [] # 提升度

        # 数据分组 与 蓝底绿底数据计算
        # 每一组中数据数量 = 总数据数量的5%向上取整，这样最后一组在数量上可能会少一些，但是不影响整体计算。
        for i in range(0,len(df),math.ceil(len(df)*0.05)):
            b = df.实际值[i:i + math.ceil(len(df)*0.05)]
            k1 = len(b)
            k2 = list(b).count(1)
            cn.append(k1)
            rn.append(k2)
            rr.append(round(k2/k1,3))
            crr.append(round(sum(rn)/sum(cn),3))

        for i in crr: # 计算 提升度
            lift.append(round(i/crr[-1],1))

        # 数据储存
        df1['占比（%）'] = ratio
        df1['客户数'] = cn
        df1['响应数'] = rn
        df1['响应率'] = rr
        df1['累计响应率'] = crr
        df1['提升度'] = lift    

    else:
        return print('\033[31m错误：文件数据有误')
        
    return df1.to_excel('lift.xlsx',index = False)


# In[15]:


# 举例用黄色数据获取另外六列
if __name__ == '__main__':
    df = pd.read_excel(r'C:/Users/46656/Desktop/Python/PWC/lift.xlsx')
    df.iloc[0:20,0:4]
    # df = df[['实际值','预测概率']]
    datalist(df)


# In[13]:





# In[ ]:




