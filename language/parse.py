from string import digits

builtins = {'print': 'print',
            'sizeof': 'sizeof',
            'locate': 'locate'}

def compile(text):
    commands = []

    text = text.split(';')
    for cmd in text:
        cmd = cmd.strip()

        if cmd.split(' ')[0] == 'int':
            s = ''.join(cmd.split(' ')[1:]).split('=')
            commands.append('variables["'+s[0].strip()+'"] = memory.allocate(8)')

            if len(s) > 1:
                commands.append('variables["'+s[0].strip()+'"].set('+s[1]+')')
        elif cmd.split(' ')[0] == 'long':
            s = ''.join(cmd.split(' ')[1:]).split('=')
            commands.append('variables["' + s[0] + '"] = memory.allocate(16)')

            if len(s) > 1:
                commands.append('variables["' + s[0] + '"].set(' + s[1] + ')')

        elif cmd.split('.')[0] == 'py':
            commands.append(' '.join(cmd[0][3:] + cmd[1:]))

        else:
            args = cmd[cmd.find('(')+1:cmd.find(')')]
            nargs = []
            b = False
            for i in args.split(','):
                if not '"' in i:
                    for c in i:
                        if c not in digits + '.,(){}':
                            nargs.append('variables["' + i + '"].get()')
                            b = True
                            break
                    if b:
                        b = False
                        break
                    nargs.append(i)
                    break
                nargs.append('"' + i + '"')

            for f in builtins.keys():
                if f in cmd:
                    commands.append(builtins[f]+'(' + ','.join(nargs) + ')')

    return commands