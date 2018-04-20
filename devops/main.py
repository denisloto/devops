
from requirement import Requirement
from time import ctime

requirement = Requirement('2018-03-01','2018-04-30')
print('[%s] Starting generate -> %s' %
      (ctime(), 'bug'))
requirement.generate_bug()
print('[%s] End generate -> %s' %
      (ctime(), 'bug'))

print('[%s] Starting generate -> %s' %
      (ctime(), 'requirement'))
requirement.generate()
print('[%s] End generate -> %s' %
      (ctime(), 'requirement'))

print('[%s] Starting generate -> %s' %
      (ctime(), 'total'))
requirement.generate_total_by_developer()
print('[%s] End generate -> %s' %
      (ctime(), 'total'))




