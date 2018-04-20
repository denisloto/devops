
from analysize import Analysize
from time import ctime
import os
import re


analysize = Analysize()
fold_data = 'data/'
fold_result = 'result/'
re_log = 'mysql-slow-digest-(\d+\-\d+\-\d+)--\d+.log'
fs = os.listdir(fold_data)
for f in fs:
    list_re = re.findall(re_log, f)
    # print(list_re)
    if len(list_re) == 1 and not os.path.exists(fold_result + list_re[0] + '-result.csv'):
        print('[%s] Starting generate -> %s' %
              (ctime(), fold_result + list_re[0]))
        analysize.generate(fold_data + f, fold_result + list_re[0] + '.csv')
        print('[%s] End generate -> %s' % (ctime(), fold_result + list_re[0]))
