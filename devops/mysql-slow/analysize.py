import pandas as pd
# import numpy as np
# import math
# from decimal import *
import datetime
import os
import re


class Analysize():
    def __init__(self):
        pass

    def generate(self, source_file, target_file):
        context = open(source_file).read()
        context = context.replace('\n', ' ').replace('\t', ' ').replace(
            '     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
        # context = context.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
        # print(context)
        result = re.findall(
            r"\# Query (\d+):.+?\# Count.+?\d+.+?(\d+).+?\# Exec time.+?\d+.+?\d+.+?(\d+[s|ms]).+?(\d+[s|ms]).+?(\d+[s|ms]).+?(\d+[s|ms]).+?(erpuser|misuser|wwwuser).+?((insert|update|select|delete|INSERT|UPDATE|SELECT|DELETE).+?)\\G", context, flags=re.DOTALL + re.MULTILINE)
        # print(result[4])

        header = ['QUERY ID', '执行次数', 'min', 'max',
                  'avg', '95%', '用户', '查询语句', '业务场景', '修复计划']
        df = pd.DataFrame(result)
        df = df[df[6].isin(['erpuser', 'misuser'])]
        df = df.iloc[:, 0:8]
        df[8] = ''
        df[9] = ''
        df = df.sort_values(7)
        df.to_csv(target_file, header=header, doublequote=True, index=False)
