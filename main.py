import ftplib, telnetlib, time, ipaddress
from router_template import template


host = '192.168.88.1'
user = 'admin'
password = ''
port = '23'  # port for telnet connection

while True:
    try:
        wanip = ipaddress.ip_address(input("Set WAN IP address\nif WAN IP address is unknown, please enter 1.1.1.1:  "))
        break
    except ValueError:
        print('Wrong value')
subnet = int(input("Set local subnet: "))
while not int(0 < subnet < 255):
    print('Wrong value!')
    subnet = int(input("Set local subnet: "))
identity = input("Set router identity: ")
d = {'subnet': subnet, 'wanip': wanip, 'identity': identity}
filename = identity + '.rsc'

with open(filename, 'w') as f:
    f.write(template.render(d))

while True:
    try:  # ftp connection
        print('Connecting to router...')
        ftpcon = ftplib.FTP(host, user, password)
        f = open(filename, 'rb')
        send = ftpcon.storbinary('STOR ' + filename, f)
        print('ok')
        print('Sending configuration to device...')
        ftpcon.close()
        break
    except WindowsError:
        print('FTP connection was failed')
        input('Check connection to the router and press Enter')

try:  # telnet connection
    command1 = 'system reset-configuration no-defaults=yes skip-backup=yes run-after-reset=' + filename
    command2 = 'yes'
    tn = telnetlib.Telnet(host, port)
    tn.read_until(b"Login: ")
    tn.write(user.encode('UTF-8') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('UTF-8') + b"\n")
    tn.read_until(b'>')
    tn.write(command1.encode('UTF-8') + b"\r\n")
    time.sleep(2)
    tn.write(command2.encode('UTF-8') + b"\r\n")
    print('********************************************\n'
          'The router will be restarted and configured!\n'
          'Please wait for signal\n'
          '********************************************')
    input('Press Enter to exit')
except WindowsError:
    print('Telnet connection was failed')
