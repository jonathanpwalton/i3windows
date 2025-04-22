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

```py
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
```