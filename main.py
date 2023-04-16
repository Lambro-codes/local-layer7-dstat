import asciichartpy, time, requests, os
from requests.exceptions import ConnectTimeout

global prev, url, offline, x, y
x = []
y = []

url = input("Enter your nginx stub url>> ")
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
            req = requests.get(url, timeout=1.2).text.split(" ")[9]
            offline = False
        except:
            offline = True
            req = prev
            pass
        
        x.append(time.strftime('%H:%M:%S'))
        if len(x) == 80:
            x.pop(0)
            y.pop(0)
        y.append(int(req) - int(prev))
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
            print("\n", f"Host: {url} Not currently accessible.", "\n")
        else:
            print("\n", f"Requests per second of {url}", "\n")
        print(chart)
        prev = req
        time.sleep(1)


update()
