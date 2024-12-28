import sys
import psutil

def kill(procname):
    for proc in psutil.process_iter(["pid", "cmdline"]):
        print(proc.name())
        if proc.name()[:len(procname)] == procname:
            target_pid = proc.pid
            p = psutil.Process(target_pid)
            if len(p.children) > 0:
                print(proc.info)

            # 指定したPIDとその子プロセスを含めてTerminate
            # 子のプロセスTerminate
            pid_list = [pc.pid for pc in p.children(recursive=True)]
            for pid in pid_list:
                psutil.Process(pid).terminate()
                print("terminate 子プロセス　{}".format(target_pid))

            # 親のプロセスTerminate
            try:
                p.terminate()
            finally:
                print("terminate 親プロセス　{}".format(target_pid))

            return
        
if __name__ == '__main__':
    kill("watchProcess.exe")