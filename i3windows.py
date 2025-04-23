#!/usr/bin/env -S python3 -u
'''
i3windows, a polybar plugin to display windows in active i3 workspace
Copyright (C) 2025 Jonathan Walton

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import json, subprocess
from typing import Any
from queue import Queue
from threading import Thread
from itertools import chain

if __name__ == '__main__':
	options = {
		'source': 'HDMI-0',       # the display to use for this module
		'window': {
			'title': {
				'limit': 20,          # the maximum width of titles
				'source': 'class'     # how titles should be shown, one of [class | title]
			},
			'color': {
				True: '#FFFFFF',      # the foreground color of focused window titles
				False: '#777777'      # the foreground color of unfocused window titles
			},
			'count': 8              # the maximum number of window titles to display
		},
		'separator': {
			'color': '#777777',     # the foreground color of the separator string
			'value': ' \u00b7 '     # the value of the separator string
		}
	}

	separator = '%{F' + options['separator']['color'] + '}' + options['separator']['value'] + '%{F-}'
	window_label = lambda label: label if len(label) <= options['window']['title']['limit'] else label[:options['window']['title']['limit']] + '\u2026'
	window_title = lambda window: '%{F' + options['window']['color'][window['focused']] + '}' + window_label(window['window_properties'][options['window']['title']['source']].lower()) + '%{F-}'

	with subprocess.Popen(['i3-msg', '-m', '-t', 'subscribe', '["workspace", "window"]'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as listener:
		started = False
		queue = Queue()
		Thread(target = lambda p, q: [q.put(l) for l in p], args = (listener.stdout, queue), daemon = True).start()

		while True:
			try:
				if started: queue.get()
				else: started = True

				focused = [node for node in json.loads(capture('i3-msg', '-t', 'get_workspaces')) if node['focused'] is True][0]
				displays = json.loads(capture('i3-msg', '-t', 'get_tree'))['nodes']
				display = [node for node in displays if node['name'] == options['source']][0]['nodes']
				workspaces = [node for node in display if node['name'] == 'content'][0]['nodes']
				workspace = [node for node in workspaces if node['id'] == focused['id']][0]['nodes']
				windows = chain.from_iterable(top['nodes'] for top in workspace)
				titles: list[str] = [window_title(window) for window in windows]

				if (len(titles) > options['window']['count']):
					diff = len(titles) - options['window']['count']
					titles = titles[:options['window']['count']]

					flag = False
					for name in titles:
						if name.startswith('%{F' + options['window']['color'][True] + '}'):
							flag = True
							break

					if flag: titles.append('%{F' + options['window']['color'][False] + '}' + f'(+{diff})' + '%{F-}')
					else: titles.append('%{F' + options['window']['color'][True] + '}' + f'(+{diff})' + '%{F-}')

				print(separator.join(titles))
			except:
				print('')