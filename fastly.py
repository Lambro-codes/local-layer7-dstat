import asciichartpy, time, requests, os, json
from requests.exceptions import ConnectTimeout

global prev, url, offline, x, y
x = []
y = []

url = "https://rt.fastly.com/channel/demo/ts/1689630250"
try:
    prev = requests.get(url).text.split(" ")[9]
    offline = False
except:
    offline = True
    pass

print()

def update():
    global prev, url, offline, x, y

    while True:  
        try:
            req = requests.get(url, timeout=1.2)
            offline = False
        except:
            offline = True
            req = prev
            pass

        data = json.loads(req.text)
        timestamp = data['Timestamp']
        print(timestamp)
        
        max_recorded_item = max(data['Data'], key=lambda item: item['recorded'])
        matching_request = max_recorded_item['datacenter']['CMB']['requests']

        
        x.append(time.strftime('%H:%M:%S'))
        if len(x) == 80:
            x.pop(0)
            y.pop(0)
        y.append(matching_request)
        chart = asciichartpy.plot(y, {'height': 20, 'color': 'cyan'})
        if os.name == 'nt':
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW("Local Layer7 Dstat | v 0.1 | By Lambro")
            os.system("mode 100,30")
            os.system('cls')
        else:
            import sys
            sys.stdout.write("\x1b]2;Local Layer7 Dstat | v 0.1 | By Lambro\x07")
            os.system('printf "\\033[8;30;100t"')
            os.system('clear')
        if offline == True:
            print("\n", f"Host: FASTLY Not currently accessible.", "\n")
        else:
            print("\n", f"Requests per second of Fastly global network", "\n")
        print(chart)
        prev = req
        time.sleep(1)


update()
