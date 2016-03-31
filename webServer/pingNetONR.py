def pingNetONR():
    import sys
    import os

    devices = {
        'Test 3'        : {'IP': '192.168.0.1'   },
        'Test 2'        : {'IP': '192.168.0.105' },
        "Test 1"        : {'IP': '192.168.0.77'  },
        'Test 4'        : {'IP': '192.168.0.88'  },
        'Pier AP M5'    : {'IP': '10.4.1.10'     },
        'North Tx UBNT' : {'IP': '10.4.1.13'     },
        'South Tx UBNT' : {'IP': '10.4.1.12'     },
        'Pier AP M2'    : {'IP': '10.4.1.15'     },
        'North iBoot'   : {'IP': '10.4.1.132'    },
        'South iBoot'   : {'IP': '10.4.1.133'    },
        'North VSG'     : {'IP': '10.4.1.122'    },
        'South VSG'     : {'IP': '10.4.1.121'    },
        'North GPS Trig': {'IP': '10.4.1.81'     },
        'South GPS Trig': {'IP': '10.4.1.80'     },
        'NTP Server'    : {'IP': '10.4.1.51'     },
        'North PTU Ctrl': {'IP': '10.4.1.230'    },
        'South PTU Ctrl': {'IP': '10.4.1.231'    },
    }

    #print 'original dict'
    #print devices

    # fping module appears to do the below for loop quite a bit faster...suggest exploring that method
    #see http://fping.org/fping.1.html for more information

    for key in devices:
        #This sends out one ping and waits a maximum of 1 second for a reply
        if os.system("ping -c 1 -W 1 " + devices[key]['IP']) == 0:
            devices[key]['Status'] = 'up'
        else:
            devices[key]['Status'] = 'down'

    #print 'new dict'
    #print devices

    return devices



if __name__ == "__main__":
    pingNetONR()
