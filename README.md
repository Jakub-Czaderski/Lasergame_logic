# Lasergame_logic
The following handcoded files can be used as Laser Game/ Tag control software, althrough it is not adjusted for hardware yet and it is quite simple, but the logic works. I am 13 and wish if you would contact me over jakubczaderski.cinnamon@proton.me if you need hardware adjustment or something, I'll do what I can.

The Admin script is supposted to run on the main PC and communicates with the sub-scripts via redis. Settings and Profiles are saved via .json files. Functions I have created are the following:
  *User profiles.
  *Two game modes, involving a classic mode (rvival) and a life model with permanent death  and more guns.
  *More gun modes. Integrated but not balanced are a Minigun, the Classic gun and a Big gun. Entering the selection screen automatically changes the life profile. Disabled during classic mode.
  *Can but does not have to bind the team's name to the selected colour, so it does not have to be re-typed.
  *Can dispence guns at random.
The Sensor_1.py script is the Sensor script for Player one. To adjust for other players, change globals()["my_name"] to the sensor's name. By default, the Admin script gives each a number, but this can be changed easily.
The Gun_1.py script shares a lot with the Sensor script. It reacts to the anti-cheat measures set by the Sensor.s
