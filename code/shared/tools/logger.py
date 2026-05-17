def log_error(message: str):
    print(f"[ERROR] {message}")

def log_success(message: str):
    print(f"[SUCCESS] {message}")

def log_warning(message: str):
    pass

def log_info(message: str):
    pass

def log_debug(message: str):
    pass

def log_connection(message: str):
    print(f"[+] {message}")

def log_disconnect(message: str):
    print(f"[-] {message}")
