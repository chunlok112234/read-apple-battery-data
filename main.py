import os
import json
from colorama import Fore
from datetime import datetime as dt
import matplotlib as mat
import matplotlib.pyplot as plt 

data_floder = "./analytics-data"
filename_ls = os.listdir(data_floder)
date_fmt = "%Y-%m-%d"
device_json: dict = json.loads(open("device.json").read())
designed_capacity = None
opt: dict|str|None = device_json
date_list = []
cycle_list = []
health_list = []

while 1:
    for index, ele in enumerate(opt.keys()):
        print(f"{Fore.BLUE}{index+1}.{Fore.RESET} {Fore.YELLOW}{ele}{Fore.RESET}")
    choice = input(f"{Fore.GREEN}Type your choice:{Fore.RESET} ")
    opt = opt.get(choice.strip())
    if opt == None:
        print(f"{Fore.RED}Invaild choice{Fore.RESET}")
        exit()
    elif isinstance(opt, dict):
        pass
    elif isinstance(opt, str):
        break
designed_capacity = float(opt)

for filename in filename_ls:
    real_stem = filename.split(".")[0]
    datetime_obj = dt.strptime(real_stem, "Analytics-%Y-%m-%d-%H%M%S")
    fp = open(f"{data_floder}/{filename}", "r")
    content_ls = fp.read().split("\n")
    for content in content_ls:
        content_obj: dict = json.loads(content)
        message: dict|None = content_obj.get("message")
        if message:
            last_value_NominalChargeCapacity = message.get("last_value_NominalChargeCapacity")
            last_value_CycleCount = message.get("last_value_CycleCount")
            if last_value_NominalChargeCapacity and last_value_CycleCount:
                health_percentage = (last_value_NominalChargeCapacity * 100 )/designed_capacity
                print(f"""{'='*20}
{Fore.CYAN}Date:{Fore.RESET} {Fore.GREEN}{datetime_obj.strftime(date_fmt)}{Fore.RESET}
{Fore.CYAN}Cycle:{Fore.RESET} {Fore.GREEN}{last_value_CycleCount} times{Fore.RESET}
{Fore.CYAN}Capacity:{Fore.RESET} {Fore.GREEN if health_percentage > 80 else Fore.YELLOW}{last_value_NominalChargeCapacity} mAh{Fore.RESET}
{Fore.CYAN}Health:{Fore.RESET} {Fore.GREEN if health_percentage > 80 else Fore.YELLOW}{health_percentage:.2f}%{Fore.RESET}
{'='*20}""")
                date_list.append(datetime_obj)
                cycle_list.append(last_value_CycleCount)
                health_list.append(health_percentage)
                break
        if content_obj.get("_marker") == "<end-of-file>":
            print(f"No battery data is found on {datetime_obj.strftime(date_fmt)}")

# print(date_list,cycle_list, health_list )
            

fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

ax1.plot(date_list, cycle_list, 'g', marker='s')
ax2.plot(date_list, health_list, 'b', marker='o')

ax1.set_xlabel('date')
ax1.set_ylabel('cycle', color='g')
ax2.set_ylabel('health (%)', color='b')

fig.gca().set_aspect(2)
plt.show()
plt.savefig("dest.jpg")
