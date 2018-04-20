from common import Common
import pandas as pd
import numpy as np
import math
from decimal import *
import datetime


class Requirement():
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def generate(self):
        # requirementId,requirementName,planStart,planEnd,actualStart,actualEnd,taskDifficulty,developer
        df_requirement = pd.read_csv('data_requirement.csv', header=0)

        df_requirement = df_requirement[((df_requirement.planStart >= self.start_date) & (
            df_requirement.planStart <= self.end_date)) | ((df_requirement.planEnd >= self.start_date) & (
            df_requirement.planEnd <= self.end_date))]

        # taskDifficultyCode,taskDifficultyEn,taskDifficultyDesc,taskDifficultyCoefficient
        df_dict_task_difficulty = pd.read_csv(
            'dict_task_difficulty.txt', header=0)
        df = pd.merge(df_requirement, df_dict_task_difficulty, how='inner',
                      left_on='taskDifficulty', right_on='taskDifficultyCode', sort=False)

        df_dict_env = pd.read_csv('dict_env.txt', header=0)
        df = pd.merge(df, df_dict_env, how='inner',
                      left_on='env', right_on='envCode', sort=False)

        series_requirement_result = []

        # bug_cols = ['requrementId', 'bugId', 'bugName', 'bugType', 'env',
        #         'reportDate', 'fixDate', 'fixDays', 'bugScore', 'belongTo', 'fixedBy', 'fixScore']
        df_bug = pd.read_csv('result_bug.csv', header=0)
        # print(df_bug)

        for indexs in df.index:
            dict_devloper = eval(df.loc[indexs, 'developer'])
            count_developer = len(dict_devloper)
            # date_plan_start = datetime.datetime.strptime(
            #     df.loc[indexs, 'planStart'], '%Y-%m-%d')
            # date_plan_end = datetime.datetime.strptime(
            #     df.loc[indexs, 'planEnd'], '%Y-%m-%d')
            # delta_plan = date_plan_end - date_plan_start
            for key, value in dict_devloper.items():
                developer_name = Common.find_developer(key)
                total_score = int(df.loc[indexs, 'planDelta']) * count_developer * \
                    df.loc[indexs, 'taskDifficultyCoefficient']
                init_score = float('%.2f' % (total_score * value))
                real_score = init_score
                if df.loc[indexs, 'planEnd'] < df.loc[indexs, 'actualEnd']:
                    real_score = 0
                df_bug_filter = df_bug[(df_bug['归属人'].astype('str') == developer_name) & (
                    df_bug['需求ID'] == df.loc[indexs, 'requirementId'])]
                # print(df_bug_filter.iloc[:,0].size)
                bug_count = df_bug_filter.iloc[:, 0].size
                bug_score = float('%.2f' % (df_bug_filter['BUG分值'].sum()))
                if math.isnan(bug_score):
                    bug_count = 0
                    bug_score = 0
                total = float('%.2f' % (real_score - bug_score))
                series_requirement_result.append(
                    [df.loc[indexs, 'requirementId'], df.loc[indexs, 'requirementName'], df.loc[indexs, 'planStart'], df.loc[indexs, 'planEnd'], df.loc[indexs, 'actualStart'], df.loc[indexs, 'actualEnd'], df.loc[indexs, 'taskDifficultyDesc'], total_score, developer_name, str(value * 100) + '%', init_score, real_score, bug_count, bug_score, total,df.loc[indexs, 'envDesc']])

        cols = ['需求ID', '需求名称', '计划开始日期', '计划结束日期', '实际开始日期', '实际结束日期',
                '难度', '初始总分值', '开发人员', '比重', '初始分值', '实际分值', 'BUG数', 'BUG分值', '小计','当前环境']
        # , 'BUG分值', '任务总分值'
        # print(series_requirement_result)
        df_requirement_result = pd.DataFrame(series_requirement_result,
                                             columns=cols)
        # print(df_requirement_result)
        df_requirement_result = df_requirement_result.sort_values(by="计划开始日期" , ascending=True)
        
        df_requirement_result.to_csv('result_requirement.csv', index=False)

    def generate_bug(self):
        # requireId,bugId,bugName,bugType,env,reportDate,fixDate,belongTo,fixedBy
        df_bug = pd.read_csv('data_bug.csv', header=0)
        df_bug = df_bug[((df_bug.reportDate >= self.start_date) & (
            df_bug.reportDate <= self.end_date)) | ((df_bug.fixDate >= self.start_date) & (
            df_bug.fixDate <= self.end_date))]
        # print(df_bug)
        df_bug['deltaFix'] = (pd.to_datetime(df_bug['fixDate']) - pd.to_datetime(df_bug['reportDate'])).dt.days
        df_requirement = pd.read_csv('data_requirement.csv', header=0)
        # print(df_requirement)
        df_requirement = df_requirement[((df_requirement.planStart >= self.start_date) & (
            df_requirement.planStart <= self.end_date)) | ((df_requirement.planEnd >= self.start_date) & (
            df_requirement.planEnd <= self.end_date))]
        # fixedDays,fixedCoefficient
        
        df_dict_bug_fixed_days = pd.read_csv(
            'dict_bug_fixed_days.txt',  header=0)

        df = pd.merge(df_bug, df_dict_bug_fixed_days, how='inner',
                      left_on='deltaFix', right_on='fixedDays', sort=False)

        # bugTypeCode,bugTypeEn,bugTypeDesc,bugTypeCoefficient
        df_dict_bug_type = pd.read_csv('dict_bug_type.txt', header=0)
        df = pd.merge(df, df_dict_bug_type, how='inner',
                      left_on='bugType', right_on='bugTypeCode', sort=False)

        # envCode,envDescEn,envDesc,envCoefficient
        df_dict_env = pd.read_csv('dict_env.txt', header=0)
        df = pd.merge(df, df_dict_env, how='inner',
                      left_on='env', right_on='envCode', sort=False)

        series_bug_result = []
        for indexs in df.index:
            bug_score = df.loc[indexs, 'envCoefficient'] * df.loc[indexs,
                                                                  'fixedCoefficient'] * df.loc[indexs, 'bugTypeCoefficient']
            fix_score = 0
            fix_coefficient = 1
            if df.loc[indexs, 'deltaFix']>0:
                fix_coefficient = 0.5
            if df.loc[indexs, 'belongTo'] is not df.loc[indexs, 'fixedBy']:
                fix_score = df.loc[indexs, 'envCoefficient'] * \
                    df.loc[indexs, 'bugTypeCoefficient'] * fix_coefficient
            series_bug_result.append(
                [df.loc[indexs, 'requirementId'], df.loc[indexs, 'bugId'], df.loc[indexs, 'bugName'], df.loc[indexs, 'bugTypeDesc'], df.loc[indexs, 'envDesc'], df.loc[indexs, 'reportDate'], df.loc[indexs, 'fixDate'], df.loc[indexs, 'fixedDays'], bug_score, Common.find_developer(df.loc[indexs, 'belongTo']), Common.find_developer(df.loc[indexs, 'fixedBy']), fix_score])

        cols = ['需求ID', 'BUG ID', 'BUG 名称', 'BUG 类型', '环境',
                '创建日期', '修复日期', '修复天数', 'BUG分值', '归属人', '修复人', '修复分值']

        df_bug_result = pd.DataFrame(series_bug_result,
                                     columns=cols)

        df_bug_result = df_bug_result.sort_values(by="创建日期" , ascending=True)

        # print(df_bug_result)
        df_bug_result.to_csv('result_bug.csv', index=False)
        # requireId,bugId,bugName,bugType,env,reportDate,fixDate,belongTo,fixedBy

    def generate_total_by_developer(self):
        # nameCode,developerName
        df_developer = pd.read_csv('dev_name.txt', header=0)

        df_requirement = pd.read_csv('result_requirement.csv', header=0)
        df_requirement = df_requirement[(df_requirement['计划开始日期'] >= self.start_date) & (
            df_requirement['计划开始日期'] <= self.end_date)]
        df_bug = pd.read_csv('result_bug.csv', header=0)

        series_developer_result = []
        for indexs in df_developer.index:
            developer_name = df_developer.loc[indexs, 'developerName']
            finish_task_count = df_requirement[df_requirement['开发人员']
                                               == developer_name].iloc[:, 0].size
            finish_task_delay_count = df_requirement[(df_requirement['开发人员'] == developer_name) & (
                df_requirement['实际结束日期'] > df_requirement['计划结束日期'])].iloc[:, 0].size
            finish_task_pre_count = df_requirement[(df_requirement['开发人员'] == developer_name) & (
                df_requirement['实际结束日期'] < df_requirement['计划结束日期'])].iloc[:, 0].size
            finish_task_due_count = finish_task_count - finish_task_delay_count
            task_score = df_requirement[df_requirement['开发人员']
                                        == developer_name]['实际分值'].sum()
            bug_count = df_bug[df_bug['归属人'] == developer_name].iloc[:, 0].size
            bug_score = df_bug[df_bug['归属人'] == developer_name]['BUG分值'].sum()
            bug_other_count = df_bug[(df_bug['修复人'] == developer_name) & (
                df_bug['修复分值'] > 0)].iloc[:, 0].size
            bug_other_score = df_bug[(df_bug['修复人'] == developer_name) & (
                df_bug['修复分值'] > 0)]['修复分值'].sum()
            if math.isnan(task_score):
                task_score = 0
            if math.isnan(bug_score):
                bug_score = 0
            if math.isnan(bug_other_score):
                bug_other_score = 0
            total = float('%.2f' %(task_score - bug_score + bug_other_score))
            finish_rate = "{:.00%}".format(0)
            if finish_task_count > 0:
                finish_rate = "{:.00%}".format(
                    finish_task_due_count / finish_task_count)
            series_developer_result.append(
                [self.start_date, self.end_date, df_developer.loc[indexs, 'developerName'], finish_task_count, finish_task_due_count, finish_task_pre_count, finish_task_delay_count, finish_rate,
                 task_score, bug_count, bug_score, bug_other_count, bug_other_score, total])

        cols = ['开始日期', '结束日期', '开发人员', '完成任务数', '按时任务数',
                '提前完成任务数', '延期任务数', '任务完成率', '任务总分值', 'BUG数', 'BUG总分值', '修复他人BUG数', '修复他人BUG分值', '合计']

        df_developer_result = pd.DataFrame(series_developer_result,
                                           columns=cols)
        df_developer_result = df_developer_result.sort_values(by="合计" , ascending=False)
        print(df_developer_result)
        df_developer_result.to_csv('result_total_{0}_{1}.csv'.format(
            self.start_date, self.end_date), index=False)
