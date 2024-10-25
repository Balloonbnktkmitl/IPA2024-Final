from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.181"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        for status in result:
            # print(status)
            interface_nm = status["interface"]
            status_int = status["status"]
            if "GigabitEthernet" in interface_nm:
                ans += f"{interface_nm} {status_int}, "
                if status_int == "up":
                    up += 1
                elif status_int == "down":
                    down += 1
                elif status_int == "administratively down":
                    admin_down += 1
        ans = ans.rstrip(", ") + f" -> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans
