from elevate import elevate
from subprocess import *
import time
import datetime
import sys

'''
Prerequisite --
Please use pip to install the module "elevate"

Usage --
Open the console like cmd.exe or PowerShell console, type below command:
python removeDevice.py <device pid>

Setup repeat cycle --
Find out the variable "REPEAT" in the script and modify the number and save

Make sure only one device PID is allowed

'''

def rem_dev():
    print(f"Select the HID device {device_pid} and remove it\n")
    rem_pshell = f"$vars = Get-PnpDevice  -Status OK |Select-Object -Property Instanceid|findstr {device_pid}; foreach($var in $vars) {{$var=$var.Trim(); Write-Output $var ; pnputil /remove-device $var}}"
    run(["powershell", rem_pshell])

def scan_sys():
    run(["powershell", "pnputil /scan-devices"])
    
def get_dev():
    find_pshell = f'Get-PnpDevice  -Status OK |Select-Object -Property Instanceid|findstr {device_pid}'
    print("List all HID")
    device_find = Popen(["powershell", find_pshell], shell=True)
    device_find.communicate(timeout=2)
    #time.sleep(5)

##-- Test if the user input exactly one PID number --##
if len(sys.argv) > 2:
    #print(len(sys.argv))
    print("Please input only one device PID number!\n")
    print("Usage: python.exe removeDevice.py <device pid>\nExample: python.exe removeDevice.py 2108\n")
    exit()
elif len(sys.argv) < 2 :
    print("Please input at exact one device PID number!\n")
    print("Usage: python.exe removeDevice.py <device pid>\nExample: python.exe removeDevice.py 2108\n")
    exit()
else:
    device_pid = sys.argv[1].strip()
    type(device_pid)
##-----------------------------------------------------


##------   Recording test start time -----##
nowaday = datetime.date.today()
nowatime = datetime.datetime.now().strftime("%H-%M-%S")
time_start =f'{nowaday}_{nowatime}'
start_time = f"Test start at {nowaday} {nowatime}\n"

filename = f'hidunplug_{time_start}.log'
with open(filename, 'w') as f:
        f.write(start_time)
        f.close()

##------  Setup some variables and elevated the user's privilege ----##
REPEAT = 1
fail_count = 0
success_count = 0
print("Elevated the privilege to Admin. level and do sth...\n")
elevate()

##-- Start n round HID/USB unplug test --##
for i in range(REPEAT):    
    print("##----------Removing the device----------##\n")
    rem_dev()
    if get_dev() != None:
        fail_count += 1
    else:
        success_count += 1
    time.sleep(5)
    print("Restore removed device\n")
    scan_sys()
    time.sleep(5)
    
##----------- End of the test -------------##
test_end_time = datetime.datetime.now().strftime("%H:%M:%S")
with open(filename, 'a') as f:
    f.write(f"After stress test for {REPEAT} times,\nRemoving failure count is: {fail_count}\nSuccessful removing count is: {success_count}\n")
    f.write(f'Test end time: {nowaday} {test_end_time}\n')
    f.close()


    