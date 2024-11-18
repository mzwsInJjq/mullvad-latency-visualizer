import json
import subprocess
import requests

# Fetch the relay list
url = 'https://api.mullvad.net/app/v1/relays'
response = requests.get(url)
json_data = response.json()

relays = json_data['wireguard']['relays']

# Filter and transform the data
us_and_ca_relays = {}
for relay in relays:
    if relay['hostname'].startswith('us') or relay['hostname'].startswith('ca'):
        us_and_ca_relays[relay['hostname']] = relay['ipv4_addr_in']

with open('us_ca_relays.csv', 'w') as f:
    f.write("hostname,ipv4_addr_in,avg_ping\n")

# Ping every server
for hostname, ipv4_addr_in in us_and_ca_relays.items():
    def ping_server(ip):
        try:
            output = subprocess.check_output(['ping', '-n', '4', ip], universal_newlines=True)
            lines = output.split('\n')
            times = [float(line.split('time=')[1].split('ms')[0]) for line in lines if 'time=' in line]
            if times:
                avg_time = sum(times) / len(times)
                return avg_time
            else:
                return None
        except subprocess.CalledProcessError:
            return None

    avg_ping = ping_server(ipv4_addr_in)
    if avg_ping is not None:
        print(f'{hostname}, {ipv4_addr_in}, {avg_ping:.2f}')
        print(f'{hostname},{ipv4_addr_in},{avg_ping:.2f}', file=open('us_ca_relays.csv', 'a'))
    else:
        print(f'{hostname}, {ipv4_addr_in}, Failed')
        print(f'{hostname},{ipv4_addr_in},Failed', file=open('us_ca_relays.csv', 'a'))