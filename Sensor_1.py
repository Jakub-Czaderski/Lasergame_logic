#!/usr/bin/env python3

import sys
import time
import redis
import os
import tty
import termios
import atexit

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
globals()["my_identity"] = 1
def anti_cheater():
    if globals().get("my_number") != None and globals().get("died") == "no":
        r.set(f"player_{globals().get('my_number')}_cheated", "true")
        r.set(f"someone_cheated", "true")
    elif globals().get("my_number") != None and globals().get("died") == "yes":
        r.decrby(f"player{globals().get('my_number')}_counter", globals().get("death_penalty"))
atexit.register(anti_cheater)

while True:
    if r.get("data_in") == "true":
        break
    else:
        time.sleep(1.0)

globals()["my_number"] = r.get(str(globals().get('my_identity')) + "_owner")
globals()["life_model"] = r.get("life_model")
globals()["died"] == "no"
globals()["death_penalty"] = r.get("death_penalty")

pass_error = "False"
FF_value = float(r.get("ff_penalty"))
Hit_value = float(r.get("hit_points"))
getting_hit_value = float(r.get("hit_penalty"))
invincibility_frames_1 = float(r.get("invincibility_frames_1"))
invincibility_frames_2 = float(r.get("invincibility_frames_2"))
invincibility_frames_3 = float(r.get("invincibility_frames_3"))
Playercount = int(r.get("Playercount"))
Game_mode = r.get("game_mode")
if Playercount < int(globals().get('my_number')):
    sys.exit(0)

player_personal_counter = r.hget(f"player_{globals().get('my_number')}", f"player_{globals().get('my_number')}_counter")
player_team_counter = r.hget(f"player_{globals().get('my_number')}", f"player_{globals().get('my_number')}_team_counter")

while True:
    if r.get("game_active") == "true":
        break
    else:
        time.sleep(1.0)
print("Begin!")

CORE_SYSTEM_STATE = set(globals().keys())

while True:

    if Game_mode == "1":
        if int(r.get(f"Lifes_{globals()['my_number']}")) <= 0:
            sys.exit()
    try:
        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
    except Exception:
        pass 
    def get_fast_input(icon_number):
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

    spd = get_fast_input(20)
    for i in range(1, Playercount + 2):
        if i == Playercount + 1:
            pass_error = "True"
            break
        elif i < 10: 
            if spd == str(f"{i}") * 20:
                universal_hset = "player_" + f"{i}"
                spd_team_counter = r.hget(universal_hset, "player_" + f"{i}" + "_team_counter")
                spd_personal_counter = r.hget(universal_hset, "player_" + f"{i}" + "_counter")
                spd_gun = r.get("player_" + f"{i}" + "_artillery")
                spd_damage = r.get(spd_gun + "_damage")
                break
        elif i > 9:
            if spd == str(f"{i}") * 10:
                universal_hset = "player_" + f"{i}"
                spd_team_counter = r.hget(universal_hset, "player_" + f"{i}" + "_team_counter")
                spd_personal_counter = r.hget(universal_hset, "player_" + f"{i}" + "_counter")
                spd_gun = r.get("player_" + f"{i}" + "_artillery")
                spd_damage = r.get(spd_gun + "_damage")
                break

    if i == int(globals().get('my_number')):
        print("Invalid input")
    elif pass_error == "False":
        if spd_team_counter == player_team_counter:
            print("Friendly_Fire!")
            r.incrbyfloat(spd_team_counter, FF_value)
            r.incrbyfloat(spd_personal_counter, FF_value)
            r.incr(f"player_{globals().get('my_number')}_ffires")
        else:
            print("You got hit!")
            r.incrbyfloat(spd_team_counter, Hit_value)
            r.incrbyfloat(spd_personal_counter, Hit_value)
        if Game_mode == "2":
            r.incr("Kills_" + f"{i}")
        r.incrbyfloat(player_team_counter, getting_hit_value)
        r.incrbyfloat(player_personal_counter, getting_hit_value)
        if Game_mode == "1":
            r.decrby(f"Lifes_{globals()['my_number']}", spd_damage)
            if int(r.get(f"Lifes_{globals()['my_number']}")) <= 0:
                r.incr(f"Kills_" + f"{i}")
                globals()["died"] == "yes"
                sys.exit()
        r.incr(f"player_{i}_gothits")
    pass_error = "False"

    current_state = set(globals().keys())
    protected = {
        'CORE_SYSTEM_STATE', 'clutter_variables', 'var'}
   
    
    clutter_variables = current_state - CORE_SYSTEM_STATE - protected
    for var in clutter_variables:
        del globals()[var]
    if Game_mode == "2":
        time.sleep(float(invincibility_frames_2))
    elif Game_mode == "1" and globals().get("life_model") == "1":
        time.sleep(float(invincibility_frames_1))
    elif Game_mode == "1" and globals().get("life_model") == "2":
        time.sleep(float(invincibility_frames_3))
