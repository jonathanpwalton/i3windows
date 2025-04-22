# i3windows

![preview](https://github.com/jonathanpwalton/i3windows/raw/main/example.png)

Polybar plugin to display windows in active i3 workspace

## Requirements

* i3
* polybar

## Quick Start

Clone the repository

```sh
mkdir -p ~/.config/polybar/scripts
cd ~/.config/polybar/scripts
git clone https://github.com/jonathanpwalton/i3windows.git
```

Add the module to polybar's ```config.ini```

```
modules-left = i3windows

[module/i3windows]
type = custom/script
exec = ~/.config/polybar/scripts/i3windows/i3windows.py 2> /dev/null
tail = true
```

Customize the module if desired in ```~/.config/polybar/scripts/i3windows/i3windows.py```

```
options = {
	'source': 'HDMI-0',
	'window': {
		'title': {
			'limit': 20,
			'source': 'class'
		},
		'color': {
			True: '#FFFFFF',
			False: '#777777'
		},
		'count': 8
	},
	'separator': {
		'color': '#777777',
		'value': ' \u00b7 '
	}
}
```