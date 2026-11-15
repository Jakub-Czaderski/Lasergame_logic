#!/usr/bin/env python3

import sys
import time
import redis
import tty
import termios
import random

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
globals()["my_name"] = "1"

while True:
    if r.get("game_active") == "true":
        break
    else:
        time.sleep(1.0)

owner = r.get(str(globals().get('my_name')) + "_gun_owner")
me = r.get(f"player_{owner}_artillery")
wait = float(r.get(me + "_cooldown"))
activate = float(r.get(me + "_chance_to_miss"))
print(owner)

while True:
    time.sleep(wait)
    try:
        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
    except Exception:
        pass 
    def get_fast_input(icon_number = 1):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        result = ""
        try:
            tty.setraw(sys.stdin.fileno())
            
            while len(result) < icon_number:
                char = sys.stdin.read(1)
                
                if char == '\x03':  
                    raise KeyboardInterrupt
                    
                result += char
                print(char, end="", flush=True) 
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        print()
        return result
    start = get_fast_input(1)

    if random.random() < activate:
        may_I = "no"
    else:
        may_I = "yes"

    if r.get("player_" + str(owner) + "_cheated") == "true":
        sys.exit()
    if r.get("game_active") != "true":
        sys.exit()

    if int(owner) < 10 and may_I == "yes":
        for _ in range(10):
            print(str(owner) * 20)
            time.sleep(0.02)
        r.incrby(f"player_{owner}_shots")
    elif int(owner) > 9 and may_I == "yes":
        for _ in range(10):
            print(str(owner) * 10)
            time.sleep(0.02)
        r.incrby(f"player_{owner}_shots")
