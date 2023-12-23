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

class Target():
	def __init__(self, target_number: int, distance: float | None = None, angle: float | None = None):
		if distance == None:
			self.distance = float(input(f"Distance to target {target_number}?: "))
		else:
			self.distance = distance

		if angle == None:
			self.angle = float(input(f"Angle to target {target_number}?: "))
		else:
			self.angle = angle
		

	distance: float
	angle: float

def print_welcome():
	print(
"""Welcome to the HLL Artillery Calculator!
Enter a distance in meters to get the appropriate amount of mils to adjust your gun to.
Enter a new faction to change the calculation.
Enter 'fm' or 'fire mission' to begin calculations between two designated map points.
Enter 'x' or 'X' to calculate a fire mission with an X pattern.
Enter 'quit' to quit."""
)

def calculate_mils(distance: float) -> float:
	if faction in ("us", "de"):
		mils = (-0.237 * distance) + 1002
	else:
		mils = (-0.213 * distance) + 1141
	return round(mils)

def get_faction() -> str:
    user_choice: str = input(f"Please enter a faction from these options- {factions}: ").lower()
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

def calculate_average_difference(input_list: list[float]) -> float:
	avg_diff = array(input_list)
	avg_diff = diff(avg_diff)

	item_sum: float = 0
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
		distances[index] = calculate_mils(distance)

	print_x_fire_mission(distances, angular_difference)

	print_start_stop(False)

def calculate_fire_mission():
	fm_start: Target = Target(1) # distance is c
	fm_end: Target = Target(2) # distance is b
	fm_targets_list: list[Target] = [fm_start]

	print_start_stop(True)

	num_points = int(input("How many points along the line will we fire upon?: "))

	angular_difference = calculate_angular_difference(fm_start.angle, fm_end.angle) # A
	angular_step = angular_difference / num_points # A / num_points
	line_of_fire = law_of_cosines_side(fm_start.distance, fm_end.distance, angular_difference)
	distance_step = line_of_fire / num_points # a / num_points

	angle_B = (math.sin(math.radians(angular_difference)) * fm_end.distance) / line_of_fire # B
	angle_B = math.asin(angle_B)
	angle_B = math.degrees(angle_B)
	angle_B = 180 - angle_B

	# C: I think this does the same thing
	for point in range(1, num_points+1):
		if fm_start.angle > fm_end.angle:
			angle = fm_start.angle - angular_step*point
			if point == 1:
				angle_B = 180 - angle_B
		else:
			angle = fm_start.angle + angular_step*point
		
		distance = distance_step*point
		new_distance = law_of_cosines_side(distance, fm_start.distance, angle_B) #b2
		fm_targets_list.append(Target(point, new_distance, angle))
	
	mils_solutions = []
	for index, target in enumerate(fm_targets_list):
		mils: float = calculate_mils(target.distance)
		mils_solutions.append(mils)
		print(f"\nTARGET {index+1}: mils={mils}, angle={target.angle}\n")

	avg_diff_mils = calculate_average_difference(mils_solutions)
	print("mil diff:", avg_diff_mils)

	avg_diff_angles = calculate_average_difference([angle for target.angle in fm_targets_list])
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
			if faction in factions:
				print(f"mils to target: {calculate_mils(distance)}")
			else:
				print("Invalid selection!")

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