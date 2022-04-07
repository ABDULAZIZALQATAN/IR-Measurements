import subprocess
import sys

def get_current_python_version():
    ver = sys.version.split(' ',1)[0]
    ver = ver.split('.',2)
    ver = ver[0] + '.' + ver[1]
    return ver

def runBashCmd(cmd):
    bashCmd = 'bash -c \"%s\" ' % cmd
    result = subprocess.getoutput(bashCmd)
    return result

def runBashFile (path , file , sh_file):
    # We Must have windows version and linux version ~/anserini
    # Remove /r from the File to Run
    cmd = r"cd %s && cat %s | tr -d '\r' > %s && sh %s" % \
          (path,file,sh_file,sh_file)
    runBashCmd(cmd)

def runPythonBashCmd(cmd):
    ver = get_current_python_version()
    cmd = 'python%s %s' % (ver,cmd)
    return runBashCmd(cmd)