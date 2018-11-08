import subprocess
import time
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('-cd', '--COMMAND',
		default='python crawl_blogs_medium.py', help='python command to run')
parser.add_argument('-to', '--TIMEOUT',
		default=18000, help='time out to restart') # default is 5 hours

args = parser.parse_args()
COMMAND = str(args.COMMAND)
TIMEOUT = float(args.TIMEOUT)

print COMMAND
print TIMEOUT

while True:
	p = subprocess.Popen(COMMAND, shell=True)
	time.sleep(TIMEOUT)
	print 'restart after ' + str(TIMEOUT) + ' seconds\n'
	p.kill()
