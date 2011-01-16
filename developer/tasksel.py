#!/usr/bin/env python

import sys, os, platform
assert os.path.exists('/usr/bin/tasksel')
version = platform.dist()[2] # lucid
output_file_path = os.path.dirname(os.path.abspath(__file__))+'/../ailurus/support/tasksel_%s'%version
output_file = open(output_file_path, 'w')
output = os.popen('tasksel --list-tasks').read()
task_names = []
for line in output.splitlines():
    assert line.startswith('i') or line.startswith('u')
    items = line.split() # '\t' is in line
    state = items[0]
    task_name = items[1]
    assert state == 'i' or state == 'u'
    assert ' ' not in task_name
    task_names.append(task_name)

task_names.remove('manual') # "manual" task means "Manual package selection"

for task_name in task_names:
    output = os.popen('tasksel --task-packages '+task_name).read()
    assert '\n' in output, task_name
    output = output.replace('\n', ' ')
    print >>output_file, task_name
    print >>output_file, output