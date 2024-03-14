import json
import hashlib



def calculate_sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

DATA_PATH = "./Market/data.json"

    
def is_has_user(username:str = ''):
    if username == '':
        return False
    
    
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
        
    if username in data:
        return True
    
    return False

def login_check(username:str = '', password:str = ''):
    if username == '' or password == '':
        return False
    
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    
    if username in data:
        if "password" in data[username]:
            if calculate_sha256(password) == data[username]["password"]:
                return True
            
    return False

def make_new_user(username:str = '', password:str = ''):
    if is_has_user(username):
        return False
    
    
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
        
    data[username] = {}
    data[username]["password"] = calculate_sha256(password)
    
    with open(DATA_PATH,"w") as f:
        json.dump(data, f)
    return True

def update_inventory(username, password, money, fish_inventory):
    try:
        if not login_check(username, password):
            return
        
        
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
            
        data[username]["money"] = money
        data[username]["fish_inventory"] = fish_inventory
        
        with open(DATA_PATH,"w") as f:
            json.dump(data, f)
    except:
        print("loi")

def get_inventory(username):
    if not is_has_user(username):
        return 0, {}

    with open(DATA_PATH, "r") as f:
        data = json.load(f)
        
    if "fish_inventory" in data[username] and "money" in data[username]:
        return data[username]["money"], data[username]["fish_inventory"]
    return 0, {}
    
    
    
    
    