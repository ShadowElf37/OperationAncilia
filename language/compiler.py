import parse

cmds = ['import memory', 'from builtins import *', 'variables = {}', 'memory = memory.RAM(2**16)'] + parse.compile(open('sample.c').read())
print(cmds)
open('sample.py', 'w').write('\n'.join(cmds))

import sample