"""********************************************************************************
* Welcome to the HLL Artillery Calculator!                                        *
* This program accepts a distance in meters and returns a value of mils to adjust *
* your artillery barrel to. Run with 'de', 'us', or 'ru' to set the appropriate   *
* calculation based on which faction you are playing.                             *
********************************************************************************"""

import sys
import math
from numpy import array, diff

#Globals
factions: tuple[str, str, str] = ("us", "de", "ru")
faction: str

def print_welcome():
	print(
"""Welcome to the HLL Artillery Calculator!
Enter a distance in meters to get the appropriate amount of mils to adjust your gun to.
Enter a new faction to change the calculation.
Enter 'fm' or 'fire mission' to begin calculations between two designated map points.
Enter 'x' or 'X' to calculate a fire mission with an X pattern.
Enter 'quit' to quit."""
)

def us_de_calculate(distance: float) -> float:
	mils = (-0.237 * distance) + 1002
	return round(mils)

def ru_calculate(distance: float) -> float:
	mils = (-0.213 * distance) + 1141
	return round(mils)

def get_faction() -> str:
    user_choice: str = input("Please enter a faction (us, de, ru): ").lower()
    return user_choice

def check_faction(faction: str) -> bool:
    if faction not in factions:
        print("Invalid faction!")
        return False
    else:
        return True

def get_faction_from_argv():
	if (len(sys.argv)-1) < 1:
		print("No command-line arguments found")
		faction = get_faction()
		while check_faction(faction) == False:
			faction = get_faction()
	else:
		if sys.argv[1] in factions:
			faction = sys.argv[1]
		else:
			while check_faction(faction) == False:
				faction = get_faction()
	return faction

def calculate_angular_difference(first: float, last:float) -> float:
	result = abs(first - last)
	return result

def law_of_cosines_side(side_1: float, side_2: float, angle: float) -> float:
	rad_angle = math.radians(angle)
	unknown_side_squared = side_1 ** 2 + side_2 ** 2 - 2 * side_1 * side_2 * math.cos(rad_angle)
	unknown_side = math.sqrt(unknown_side_squared)

	return unknown_side

def law_of_cosines_angle(side_1: float, side_2: float, side_3: float) -> float:
	#unknown_angle = math.acos((side_1**2) + (side_2**2) - (side_3**2) / (2*side_1*side_2))
	numerator: float = side_1**2 + side_2**2 - side_3**2
	denominator: float = 2 * side_1 * side_2
	unknown_angle: float = numerator / denominator
	unknown_angle = math.acos(unknown_angle)
	
	return math.degrees(unknown_angle)

def law_of_sines(side_1: float, side_2: float, angle_1: float) -> float:
	# side_1 == b # side_2 == c # angle_1 == B
	angle_1: float = math.radians(angle_1)
	unknown_angle: float = math.asin((side_2 * angle_1) / side_1)

	return math.degrees(unknown_angle)

def calculate_final_angle(angle_1: float, angle_2: float) -> float:
	final_angle: float = 180 - (angle_1 + angle_2)
	return final_angle

def calculate_average_difference(input_list: list[float]):
	avg_diff = array(input_list)
	avg_diff = diff(avg_diff)

	item_sum = 0
	for item in avg_diff:
		item_sum += item

	avg_diff = item_sum / len(avg_diff)

	return avg_diff

#C: Is this really required?
def print_start_stop(mission_start: bool = True):
	if mission_start:
		print("BEGIN FIRE MISSION\n")
	else:
		print("END FIRE MISSION\n")

def calculate_special_isosceles_hypotenuse(side: float) -> float:
	hypotenuse: float = math.sqrt(2) * side
	return hypotenuse

#C: This function is really messy. I feel like we should rework it with f strings.
def print_x_fire_mission(distances: list[float], angle: float):
	whitespace = " "
	num_spaces = len(str(round(distances[0], 2)) + ", -" + str(round(angle, 2)) + "          " + str(round(distances[0], 2)) + ", +" + str(round(angle, 2)))
	num_spaces = int(num_spaces / 2)
	num_spaces = int(num_spaces - (len(str(round(distances[2], 2))) / 2))
	print("")
	print(str(round(distances[0], 2)) + ", -" + str(round(angle, 2)) + "          " + str(round(distances[0], 2)) + ", +" + str(round(angle, 2)))
	print(num_spaces*whitespace + str(round(distances[2], 2)))
	print(str(round(distances[1], 2)) + ", -" + str(round(angle, 2)) + "          " + str(round(distances[1], 2)) + ", +" + str(round(angle, 2)))

def calculate_x_fire_mission():
	angle_B = 135
	distances: list[float] = []
	print_start_stop(True)
	original_target: float = float(input("Distance to original target: ")) # c

	square_length: float = float(input("Length of target square: "))
	isosceles_side_length: float = square_length / 2.0

	line_to_new_target: float = calculate_special_isosceles_hypotenuse(isosceles_side_length) # a
	distance_to_new_target: float = law_of_cosines_side(original_target, line_to_new_target, angle_B) # b

	angular_difference: float = law_of_cosines_angle(original_target, distance_to_new_target, line_to_new_target) # A

	distance_to_bottom_target: float = distance_to_new_target - square_length
	distances.append(distance_to_new_target)
	distances.append(distance_to_bottom_target)
	distances.append(original_target)

	for index, distance in enumerate(distances):
		if faction == "us" or faction == "de":
			distances[index] = us_de_calculate(distance)
		elif faction == "ru":
			distances[index] = ru_calculate(distance)

	print_x_fire_mission(distances, angular_difference)

	print_start_stop(False)

def calculate_fire_mission():
	fm_start = []
	fm_end = []
	
	print_start_stop(True)

	num_points = int(input("How many points along the line will we fire upon?: "))
	fm_start.append(float(input("Angle to first target?: ")))
	fm_start.append(float(input("Distance to first target?: "))) # c
	fm_end.append(float(input("Angle to final target?: ")))
	fm_end.append(float(input("Distance to final target?: "))) # b

	angular_difference = calculate_angular_difference(fm_start[0], fm_end[0]) # A
	angular_step = angular_difference / num_points # A / num_points
	line_of_fire = law_of_cosines_side(fm_start[1], fm_end[1], angular_difference)
	distance_step = line_of_fire / num_points # a / num_points

	angle_B = (math.sin(math.radians(angular_difference)) * fm_end[1]) / line_of_fire # B
	angle_B = math.asin(angle_B)
	angle_B = math.degrees(angle_B)
	angle_B = 180 - angle_B

	distances = []
	angles = []
	i = 1
	for point in range(num_points):
		if fm_start[0] > fm_end[0]:
			angle = fm_start[0] - angular_step*i
			if i == 1:
				angle_B = 180 - angle_B
		else:
			angle = fm_start[0] + angular_step*i
		
		distance = distance_step*i
		new_distance = law_of_cosines_side(distance, fm_start[1], angle_B) #b2
		distances.append(new_distance)
		angles.append(angle)
		i += 1

	distances.insert(0, fm_start[1])
	angles.insert(0, fm_start[0])
	
	print("")
	solutions = []
	i = 0
	for i in range(len(distances)):
		if faction == "us" or faction == "de":
			mils = us_de_calculate(distances[i])
			solutions.append(mils)
			print("TARGET", str(i+1) + ":", "mils:", mils, "angle:", angles[i])
		elif faction == "ru":
			mils = ru_calculate(distances[i])
			solutions.append(mils)
			print("TARGET", str(i+1) + ":", "mils:", mils, "angle:", angles[i])

	print("")
	avg_diff_mils = calculate_average_difference(solutions)
	print("mil diff:", avg_diff_mils)

	avg_diff_angles = calculate_average_difference(angles)	
	print("angle diff:", avg_diff_angles)

	print_start_stop(False)

if __name__ == "__main__":
	print_welcome()
	faction = get_faction_from_argv()
	
	user_input: float | str = 0
	
	while True:
		user_input = input("distance to target(m): ")
		if user_input.isdigit():
			distance = float(user_input)
			if faction == "us" or faction == "de":
				try:
					mils = us_de_calculate(distance)
					print("mils to target: {mils}")
				except:
					print("Invalid selection!")
			elif faction == "ru":
				try:
					mils = ru_calculate(distance)
					print("mils to target: {mils}")
				except:
					print("Invalid selection!")
			continue

		elif user_input.isalpha():
			user_input = str(user_input)
			if user_input == "quit":
				sys.exit(0)

			if user_input.lower() in factions:
				faction = user_input.lower()
				print(f"Changed calculation to {faction}")

			elif user_input.lower() == "fm" or user_input.lower() == "fire mission":
				calculate_fire_mission()

			elif user_input.lower() == "x":
				calculate_x_fire_mission()

			continue