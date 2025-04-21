#!/usr/bin/env -S python3 -u

import json, subprocess, time, os, sys
from typing import Any
from pprint import pprint
from queue import Queue
from threading import Thread

def capture(*args: str, **kwargs: Any) -> str:
	return subprocess.check_output(args, **kwargs)

if __name__ == '__main__':
	OUTPUT = 'HDMI-0'

	with subprocess.Popen(['i3-msg', '-m', '-t', 'subscribe', '["workspace", "window"]'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as listener:
		queue = Queue()
		thread = Thread(target = lambda p, q: [q.put(l) for l in p], args = (listener.stdout, queue), daemon = True).start()

		started = False
		while True:
			try:
				if started: queue.get()
				else:	started = True
				focused = [node for node in json.loads(capture('i3-msg', '-t', 'get_workspaces')) if node['focused'] is True][0]
				displays = json.loads(capture('i3-msg', '-t', 'get_tree'))['nodes']
				display = [node for node in displays if node['name'] == OUTPUT][0]['nodes']
				workspaces = [node for node in display if node['name'] == 'content'][0]['nodes']
				workspace = [node for node in workspaces if node['id'] == focused['id']][0]['nodes'][0]['nodes']
				print(' %{F#777}\u00b7 '.join([
					('%{F#fff}' if window['focused'] else '%{F#777}') +
					window['window_properties']['class'].lower() +
					'%{F-}'
					for window in workspace
				]))
			except:
				print('')