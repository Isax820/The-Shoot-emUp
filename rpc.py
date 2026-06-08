import time
from pypresence import Presence

client_id = "1513589426285051905"

def run_rpc():
    RPC = Presence(client_id)
    
    try:
        RPC.connect()
        RPC.update(state="v1.1", details="Dans l'espace")
        
        while True:
            time.sleep(15)

    except Exception as e:
        RPC.close()
        return False
    
    finally:
        RPC.close()