#coding=utf-8
import pandas as pd
import xlsxwriter
import openpyxl
import numpy as np


data = pd.read_excel('/Users/yangfeng/Desktop/excel.xlsx',index_col=None,
                     dtype={'date':np.str}, date_parser=lambda x: pd.to_datetime(x, format='YYYY-mm'))
output_file='/Users/yangfeng/Desktop/output_excel.xlsx'
data['date_l'] = data['date']
area = list(set(data['date_l']))
print(area)
writer = pd.ExcelWriter(output_file)
for country in list(area):
    df = data[data['date'] == country]
    df.to_excel(writer, sheet_name= country ,index=False)
writer.save()