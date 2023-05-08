import threading
import os
import re
import subprocess
import shlex
import time

def print_time(threadName):
    print(f"{threadName}: {time.ctime(time.time())}")

sentinel = 0

class screenshotThread (threading.Thread):
    def __init__(self, threadId, threadName, screenshotCount):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.threadName = threadName
        self.screenshotCount = screenshotCount
    def run(self):
        while self.screenshotCount:
            if sentinel:
                self.threadName.exit()
            # print_time(self.threadName)
            scrotFileName = f"scrot-{self.threadName}-{self.screenshotCount}.png"
            res2 = subprocess.run(['sudo','scrot','-u','-b','-d','1',scrotFileName])
            self.screenshotCount -= 1


class commandThread (threading.Thread):
    def __init__(self, threadId, threadName, command):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.threadName = threadName
        self.command = command
    def run(self):
        # print_time(self.threadName)
        commandArgs = shlex.shlex(self.command, punctuation_chars=True)
        print(f"{myPrompt} {repr(self.command)}")
        res4 = subprocess.run(commandArgs, stdout=True)


# Prompt Colors
green = '\033[01;32m'
blue = '\033[01;34m'
white = '\033[00m'

# Build Prompt
promptDir = os.getcwd()
promptDir = re.sub(r"^/home/user","~",promptDir)
myPrompt = f"{green}user@debian02{white}:{blue}{promptDir}{white}$"

commands = [
    ('id', 'sudo id'),
    ('hostname', 'sudo hostname'),
    ('ip-address', 'sudo ip a'),
    ('nmap-tcp-all','sudo nmap -v --stats-every 180 -Pn -sS scanme.nmap.org -oA nmap-tcp-all'),
    ('nmap-udp-all', 'sudo nmap -v --stats-every 180 -Pn -sU scanme.nmap.org -oA nmap-udp-all')
    ]

threadId=1
commandId=1
for (screenshotName, command) in commands:
    try:
#        print_time("     Starting Threads")
        screenshotThread1 = screenshotThread(threadId, screenshotName + "-begin", 5)
        commandThread1 = commandThread(threadId+1, "commandThread-"+str(commandId), command)
        screenshotThread1.start()
        commandThread1.start()
        screenshotThread1.join()
        commandThread1.join()
#        print_time("     End Threads")

        screenshotThread2 = screenshotThread(threadId+2, screenshotName + "-end", 2)
        screenshotThread2.start()
        screenshotThread2.join()

        commandId += 1
        threadId += 3
    except Exception as e:
        print(e)
        exit(2)
