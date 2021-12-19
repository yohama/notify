import argparse
import re
import subprocess
import time


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default='http://192.168.1.21:12380/cmd', help="Notificator's URL")
    parser.add_argument('--period', type=int, default=5, help="Time period of Notification [sec]")
    args = parser.parse_args()
    return args


def count_procs():
    ret = dict()
    proc = subprocess.Popen('tasklist', shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        w = re.split(' +', line.decode('shift_jis'))
        if w[0] in ret.keys():
            ret[w[0]] += 1
        else:
            ret[w[0]] = 1
    return ret


def post(url, data):
    proc = subprocess.Popen(f'curl --request POST --data {data} {url}', shell=False, stdout=subprocess.PIPE)
    for line in proc.stdout:
        print(line)


if __name__ == '__main__':
    args = parse()
    num_python_procs = count_procs()['python.exe']
    while True:
        prev_num_python_procs = num_python_procs
        num_python_procs = count_procs()['python.exe']
        if num_python_procs > prev_num_python_procs:
            post(url = args.url, data='cmd=start')
        if num_python_procs < prev_num_python_procs:
            post(url = args.url, data='cmd=done')
        if num_python_procs > 1 and num_python_procs == prev_num_python_procs:
            post(url = args.url, data='cmd=running')
        time.sleep(args.period)
        