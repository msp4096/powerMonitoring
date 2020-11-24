def pingNet():
    import sys
    import os

    devices = {
        'Router'      : {'IP': '192.168.0.1'   },
        'DoomAlpha'   : {'IP': '192.168.0.44' },
        "Nana's UBNT" : {'IP': '192.168.0.43'  },
        'Cameras'     : {'IP': '192.168.0.88'  },
        'HPprinter'   : {'IP': '192.168.0.112' },
	'Nana Pi'     : {'IP': '192.168.0.150' }
    }

    print('original dict')
    print(devices)

    for key in devices:

        if os.system("ping -c 1 -W 1 " + devices[key]['IP']) == 0:
            devices[key]['Status'] = 'up'
        else:
            devices[key]['Status'] = 'down'

    print('new dict')
    print(devices)

    return devices



if __name__ == "__main__":
    pingNet()
