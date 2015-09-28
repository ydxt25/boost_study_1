#!/usr/bin/env python
import os
import re
import sys
import json
import daemon
import signal
import exceptions

def usage(appName):
    print(appName + ' iqpath args')

class Factory(object):
    @staticmethod
    def createPlugin(root, pluginName):
        try:
            module = __import__(pluginName)
            constructor = getattr(module, pluginName)
            if constructor is not None:
                return constructor()
        except exceptions.Exception, e:
            print('create plugin exception:' + str(e))
            return None

    @staticmethod
    def findPlugins(pattern):
        if pattern is None:
            return (None,{})

        [root, fileNames] = os.path.split(pattern)
        if not os.path.exists(root):
            print(pattern + ' is not a valid path')
            return (root,[])

        rePattern = re.compile(fileNames)
        allFiles = os.listdir(root)

        files = []
        for f in allFiles:
            fileName, ext = os.path.splitext(f)
            if ext == '.py' and rePattern.match(fileName):
                files.append(fileName)
        return (root,files)

    @staticmethod
    def createCheckeres(pattern):
        checker = []
        root,plugins = Factory.findPlugins(pattern)
        if 0 != len(plugins):
            sys.path.append(root)
            for plugin in plugins:
                newChecker = Factory.createPlugin(root, plugin)
                if newChecker is not None:
                    checker.append(newChecker)

        return checker

def getAppIdInfo(executale):
    exeDir = executale
    exePath = executale
    if os.path.isfile(exePath):
        exeDir = os.path.dirname(exeDir)
    else:
        exePath = os.path.join(exePath, 'production')
    confPath = os.path.join(exeDir, 'conf/Diplomat.json')
    if not os.path.isfile(confPath):
        print("can't open file " + confPath + " for read")
        sys.exit(1)
    try:
        confFile = open(confPath, 'r')
        confObject = json.load(confFile)
        confFile.close()
    except Exception, ex:
        print(confPath + ' not a valid json file')
        sys.exit(1)
    if not confObject.has_key("APPID"):
        print("can't find node APPID in configure file " + confPath)
        sys.exit(1)
    iqId = confObject['APPID']
    return (exeDir,exePath,iqId)


if __name__ == '__main__':
    scriptPath, startIQName = os.path.split(os.path.abspath(sys.argv[0]))
    if len(sys.argv) <= 2:
        usage(sys.argv[0])
        sys.exit(1)

    executale = sys.argv[1]
    exeDir,exePath,iqId = getAppIdInfo(executale)
    pidFileName = '/tmp/iq2_%d.pid' % iqId
    try:
        pidFile = open(pidFileName, 'r')
        daemon.checkPID(pidFileName)
    except Exception, ex:
        pass

    try:
        chechers = Factory.createCheckeres(scriptPath + '/.+Checker')
        for checker in chechers:
            if checker.check(exeDir, sys.argv):
                sys.exit(1)

        daemon.daemonize(pidFileName)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        os.chdir(exeDir)

        stdin = os.open('stdin.txt',os.O_RDONLY | os.O_CREAT)
        stdout = os.open('stdout.txt',os.O_RDWR | os.O_CREAT)
        stderr = os.open('stderr.txt',os.O_RDWR | os.O_CREAT)

        os.dup2(stdin,0)
        os.dup2(stdout,1)
        os.dup2(stderr,2)

        os.close(stdin)
        os.close(stdout)
        os.close(stderr)

        sys.stdin = open('stdin.txt','r')
        sys.stdout = open('stdout.txt','w')
        sys.stderr = open('stderr.txt','w')

        os.umask(0)
        sys.stdout.flush()

        args = [exePath] + sys.argv[2:]
        os.execv(exePath, args)
    except Exception, ex:
        if os.path.exists(pidFileName):
            os.remove(pidFileName)

