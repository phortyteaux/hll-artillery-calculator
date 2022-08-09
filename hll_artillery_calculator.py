"""********************************************************************************
* Welcome to the HLL Artillery Calculator!                                        *
* This program accepts a distance in meters and returns a value of mils to adjust *
* your artillery barrel to. Run with 'de', 'us', or 'ru' to set the appropriate   *
* calculation based on which faction you are playing.                             *
********************************************************************************"""

import sys
import math

def print_welcome():
	print("Welcome to the HLL Artillery Calculator!")
	print("Enter a distance in meters to get the appropriate amount of mils to adjust your gun to.")
	print("Enter 'quit' to quit.")
	print("Enter a new faction to change the calculation.")

def us_de_calculate(distance):
	mils = (-0.237 * float(distance)) + 1002
	return round(mils)

def ru_calculate(distance):
	mils = (-0.213 * float(distance)) + 1141
	return round(mils)

def check_argv():
	if (len(sys.argv)-1) < 1:
		print("No command-line arguments found")
		faction = input("Please enter a faction (us, de, ru): ")
		while faction not in factions:
			print("Invalid faction!")
			faction = input("Please enter a faction (us, de, ru): ")
	else:
		if sys.argv[1] in factions:
			faction = sys.argv[1]
		else:
			while faction not in factions:
				print("Invalid faction!")
				faction = input("Please enter a faction (us, de, ru): ")
	return faction

def calculate_angular_difference(first, last):
	result = abs(first - last)
	return result

def calculate_fire_mission():
	fm_start = []
	fm_end = []
	print("")
	print("BEGIN FIRE MISSION")
	print("")
	num_points = int(input("How many points along the line will we fire upon?: "))
	fm_start.append(float(input("Angle to first target?: ")))
	fm_start.append(float(input("Distance to first target?: "))) # c
	fm_end.append(float(input("Angle to final target?: ")))
	fm_end.append(float(input("Distance to final target?: "))) # b

	angular_difference = calculate_angular_difference(fm_start[0], fm_end[0]) # A
	print("angular_difference:", angular_difference)
	#angular_difference = math.radians(angular_difference)
	angular_step = angular_difference / num_points # A / num_points
	print("A/4:", angular_step)
	angular_step = math.radians(angular_step)

	first_part = (fm_end[1] * fm_end[1]) + (fm_start[1] * fm_start[1])
	second_part = -2 * fm_end[1] * fm_start[1] * math.cos(math.radians(angular_difference))
	line_of_fire = first_part + second_part # a
	line_of_fire = math.sqrt(line_of_fire)
	print("a:", line_of_fire)
	distance_step = line_of_fire / num_points # a / num_points
	print("a/4:", distance_step)

	angle_B = (math.sin(math.radians(angular_difference)) * fm_end[1]) / line_of_fire # B
	angle_B = math.asin(angle_B)
	print("angle_B:", angle_B)
	#angle_B = math.radians(angle_B)

	distances = []
	i = 1
	for point in range(num_points):
		print("i:", i)
		new_distance = (math.sin(angle_B) * (distance_step*i)) / math.sin((angular_step*i)) # b2
		print("new_distance:", new_distance)
		distances.append(new_distance)
		i += 1


if __name__ == "__main__":
	factions = ("us", "de", "ru")
	faction = check_argv()
	print_welcome()
	distance = 0
	
	while True:
		distance = input("distance to target(m): ")
		if distance == "quit":
			sys.exit(0)

		if distance in factions:
			faction = distance
			print("Changed calulation to", faction)
			continue

		if distance == "fm" or distance == "fire mission":
			calculate_fire_mission()
			continue

		if faction == "us" or faction == "de":
			try:
				mils = us_de_calculate(distance)
				print("mils to target:", mils)
			except:
				print("Invalid selection!")
				continue
		elif faction == "ru":
			try:
				mils = ru_calculate(distance)
				print("mils to target:", mils)
			except:
				print("Invalid selection!")
				continue