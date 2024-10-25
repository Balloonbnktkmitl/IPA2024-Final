import subprocess
student_id = "65070021"
router_name = "CSR1KV-Pod1-1"
def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', 'ansible/playbook.yml']
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout
    if 'ok=2' in result:
        filename = f"show_run_{student_id}_{router_name}.txt"

        # สร้างและบันทึกไฟล์ที่ได้จากการรัน playbook ลงในไฟล์
        with open(filename, 'w') as file:
            file.write(result_output)  # บันทึกผลลัพธ์ลงไฟล์

        return filename
    else:
        return False
