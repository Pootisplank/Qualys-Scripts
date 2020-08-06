
import json
from time import sleep
import datetime

import ssllabsscanner

grades = ''
current_time = datetime.datetime.now().strftime('%b-%d-%y-%H:%M:%S')

with open('hosts.txt', 'r') as file:
    for host in file:
        data = ssllabsscanner.resultsFromCache(host.strip())
        
        if 'errors' in data:
            print(data['errors'])
            break;
        
        if data['status'] == 'IN_PROGRESS':
            while(data['status'] != 'READY'):
                data = ssllabsscanner.resultsFromCache(host.strip())
        
        if data['status'] == 'DNS':
            data = ssllabsscanner.newScan(host.strip())
            
        grades += host.strip() + ' ' + data['endpoints'][0]['grade'] + '\n'

print(grades, file=open('grades.txt', 'w'))