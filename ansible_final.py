import subprocess
student_id = "65070021"
router_name = "CSR1KV-Pod1-1"
def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', '-i','ansible/inventory', 'ansible/playbook.yml']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        return "ok"
    else:
        print(result)
        return False
