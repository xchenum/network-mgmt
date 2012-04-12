import pexpect
import os
import sys
import re

def execute_on_arista_switch(user, pw, ip, cmds):
    
    if re.match(r"\d+\.\d+\.\d+\.\d+", ip) is None:
        raise NameError( "%s is not an IP" % (ip) )

    if re.match(r"^\S+$", user) is None:
        raise NameError( "%s is not a valid username" % (user) )

    child = pexpect.spawn('ssh %s@%s' % (user, ip))

    tmp_file = "/tmp/%s_info_push" % (ip)
    fout = file(tmp_file, 'w')
    child.logfile = fout

    index = child.expect(['yes', 'assword'])
    if (index == 0):
        child.sendline("yes")
        child.expect('assword')
    child.sendline(pw)

    child.expect(">")
    child.sendline("")
    child.sendline("")
    child.sendline("")
    child.sendline("")

    child.sendline("enable")
    child.expect("#")

    for x in cmds:
        child.sendline(x)
        child.expect("#")

    child.sendline("write")
    child.sendline("quit")

    child.terminate()
    fout.close()

    res = []
    for line in open(tmp_file).readlines():
        res.append(line.strip())
        if line.find(">enable") != -1:
            res = []
    os.system("rm %s" % (tmp_file))
    return res

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "usage: python %s <user> <pass> <ip> <cmd_list_file_name>" % (sys.argv[0])
        sys.exit(1)

    cmds = [x.strip() for x in open(sys.argv[4]).readlines()]
    res = execute_on_arista_switch(sys.argv[1], sys.argv[2], sys.argv[3], cmds)

    for line in res:
        print line
    
