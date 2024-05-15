import os
import ctypes
import sys
import pickle
import psutil
import platform
from sklearn.ensemble import RandomForestClassifier
import pyre_check  

class WindowsSystem:
    @staticmethod
    def restart_computer():
        os.system("shutdown /r /t 1")

    @staticmethod
    def shutdown_computer():
        os.system("shutdown /s /t 1")

    @staticmethod
    def check_disk_space():
        os.system("wmic logicaldisk get size,freespace,caption")

    @staticmethod
    def list_directory():
        os.system("dir")

    @staticmethod
    def ip_config():
        os.system("ipconfig /all")

class Agent:
    def __init__(self):
        self.model = None
        self.last_action = None

    def train_model(self, data, labels):
        self.model = RandomForestClassifier()
        self.model.fit(data, labels)

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.model, f)

    def scan_system_state(self):
        system_info = {
            "platform": platform.platform(),
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }
        return system_info

    def analyze_data(self, data):
        return sum(data) / len(data)

    def make_decision(self, system_state):
        if system_state["cpu_usage"] > 80 or system_state["memory_usage"] > 80:
            return "Check_Directories"
        else:
            return "Do_Nothing"

    def interact_with_environment(self, decision):
        if decision == "Check_Directories":
            WindowsSystem.list_directory()
            self.last_action = "Check_Directories"
            return 0.5
        elif decision == "Do_Nothing":
            self.last_action = "Do_Nothing"
            return -1

    def get_reward(self, system_state):
        if self.last_action == "Check_Directories" and malicious_software_found(system_state):
            return 5
        elif self.last_action == "Check_Directories" and not malicious_software_found(system_state):
            return 200
        else:
            return 0

    def scan_file_for_malware(self, file_path):
        result = pyre_check.scan_file(file_path)
        if result['malicious']:
            print(f"Файл {file_path} обнаружен как вредоносный.")
            print("Результаты сканирования:", result)
            return True
        else:
            print(f"Файл {file_path} не обнаружен как вредоносный.")
            return False

    def scan_all_files(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                self.scan_file_for_malware(file_path)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def malicious_software_found(system_state):
    # Здесь мы просто проверяем, нашел ли агент вредоносное ПО в процессе сканирования директорий
    return False  # Замените на соответствующую проверку

if is_admin():
    actions = WindowsSystem()

    agent = Agent()
    data = [...]  
    labels = [...]  
    agent.train_model(data, labels)

    model_filename = "agent_model.pkl"
    agent.save_model(model_filename)
    print(f"Model saved in {model_filename}")

    while True:
        system_state = agent.scan_system_state()
        decision = agent.make_decision(system_state)
        reward = agent.interact_with_environment(decision)
        reward += agent.get_reward(system_state)
        print(f"Reward: {reward}")

        agent.scan_all_files("C:/")  # Замените на путь к корневой директории вашей системы

else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
