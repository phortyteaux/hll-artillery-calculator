"""********************************************************************************
* Welcome to the HLL Artillery Calculator!                                        *
* This program accepts a distance in meters and returns a value of mils to adjust *
* your artillery barrel to. Run with 'de', 'us', or 'ru' to set the appropriate   *
* calculation based on which faction you are playing.                             *
********************************************************************************"""

import sys
import math
import argparse
from typing import Callable
from numpy import array, diff
from numpy.typing import NDArray

## Globals
# Tuple of all possible user factions
factions: tuple[str, str, str] = ("us", "de", "ru")
# Currently selected user faction
faction: str

# Parser for launch arguments
parser = argparse.ArgumentParser(
	prog= "Hell Let Loose Artillery Calculator",
 	description = "This program accepts a distance in meters and returns a value of mils to adjust your barrel to."
)
parser.add_argument(
	"-f",
	"--faction",
	choices = factions,
	help = "The faction you are playing as",
	type = str,
	action="store",
	default=None
)

#Classes
class Point():
	"""
	Class for cartesian operations.
	Will need some functions to output Targets
	Ideally will also output HLL Map numbers.
	"""
	def __init__(self, x: float, y: float) -> None:
		self.x = x
		self.y = y
	
	def __str__(self) -> str:
		return f"{self.x}, {self.y}"
	
	def __add__(self, point: 'Point') -> 'Point':
		return Point(self.x + point.x, self.y + point.y)
	
	def __sub__(self, point: 'Point') -> 'Point':
		return Point(self.x - point.x, self.y - point.y)

class Target():

	def __init__(self, target_number: int | None = None, distance: float | None = None, angle: float | None = None):
		get_distance_string: str = "Distance to target"
		get_angle_string: str = "Angle to target"
		if isinstance(target_number, float):
			get_distance_string = f"{get_distance_string} {target_number}"
			get_angle_string = f"{get_angle_string} {target_number}"

		if distance == None:
			self.distance = float(input(f"{get_distance_string}?: "))
		elif isinstance(distance, float):
			self.distance = distance
		else:
			raise TypeError(
       			f"Argument 'distance' is not a Float or None.\n" 
                f"Given argument is of type {type(distance)}"
            )

		if angle == None:
			self.angle = float(input(f"{get_angle_string}?: "))
		elif isinstance(angle, float):
			self.angle = angle
		else:
			raise TypeError(
       			f"Argument 'angle' is not a Float or None.\n" 
                f"Given argument is of type {type(angle)}"
            )

	distance: float
	coordinates: Point # Will be used later for cartesian operations
	angle: float

	def get_mils(self) -> float:
		"""Converts the distance to the target to mils for in game use

		Args:
			distance (float): distance from the gun to the target

		Returns:
			float: the converted mils
		"""
		if faction in ("us", "de"):
			mils = (-0.237 * self.distance) + 1002
		else:
			mils = (-0.213 * self.distance) + 1141
		return round(mils)

#Decorators
def fire_mission_decorator(function: Callable):
	def wrapper():
		print("BEGIN FIRE MISSION\n")
		function()
		print("END FIRE MISSION\n")

	return wrapper

#Math
def calculate_angular_difference(first_target: Target, last_target: Target) -> float:
	return abs(first_target.angle - last_target.angle)

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
	angle_1 = math.radians(angle_1)
	unknown_angle: float = math.asin((side_2 * angle_1) / side_1)

	return math.degrees(unknown_angle)

def calculate_final_angle(angle_1: float, angle_2: float) -> float:
	final_angle: float = 180 - (angle_1 + angle_2)
	return final_angle

def calculate_average_difference(input_list: list[float]) -> float:
	input_array: NDArray = array(input_list, float)
	avg_diff_array: NDArray = diff(input_array)

	item_sum: float = 0
	for item in avg_diff_array:
		item_sum += item

	avg_diff: float = item_sum / len(avg_diff_array)

	return avg_diff

def calculate_special_isosceles_hypotenuse(side: float) -> float:
	hypotenuse: float = math.sqrt(2) * side
	return hypotenuse


#General functions
def print_welcome_message():
	print(
		"Welcome to the HLL Artillery Calculator!\n"
		"Enter a distance in meters to get the appropriate amount of mils to adjust your gun to.\n"
		"Enter a new faction to change the calculation.\n"
		"Enter 'fm' or 'fire mission' to begin calculations between two designated map points.\n"
		"Enter 'x' or 'X' to calculate a fire mission with an X pattern.\n"
		"Enter 'quit' to quit."
	)

def get_faction() -> str:
	user_choice: str = ""
	while check_faction(user_choice) is not True:
		user_choice = input(f"Please enter a faction from these options- {factions}: ").lower()

	return user_choice

def set_faction(new_faction: str | None) -> None:
    global faction
    #None is Falsy
    if not new_faction:
        new_faction = get_faction()
    if check_faction(new_faction):
        faction = new_faction
        print(f"Set Faction to {faction}")

def check_faction(faction: str) -> bool:
    if faction.lower() not in factions:
        print("Invalid faction!")
        return False
    else:
        return True

#C: This function is really messy. I feel like we should rework it with f strings.
#C: We should also reorganize the list input so its more rational.
#C: Upper row being target0, middle being 2, and bottom being 1 feels ugly to me.
def print_x_fire_mission(Targets: list[Target], angle: float):
	#C: Wrote this up as an alternative to the messiness of the original.
	"""
	#Get the length of the basic output string.
	line_segment_length:int = len(f"{round(Targets[0].get_mils(), 2)}, -{round(angle, 2)}")
	#Use that to create the size of whitespace we want.
	whitespace:str = " " * line_segment_length

	#We're outputting 2, 1, 2 targets on each line. So we can consider the block as being made of 3 parts.
	#By inputting the whitespace in the proper place, it'll space everything out nicely.
	print(
		f"{round(Targets[0].get_mils(), 2)}, -{round(angle, 2)}{whitespace}{round(Targets[0].get_mils(), 2)}, +{round(angle, 2)}\n"
		f"{whitespace}{round(Targets[2].get_mils(), 2)}\n"
		f"{round(Targets[1].get_mils(), 2)}, -{round(angle, 2)}{whitespace}{round(Targets[1].get_mils(), 2)}, +{round(angle, 2)}"
	)
	"""
	whitespace = " "
	num_spaces = len(
		f"{round(Targets[0].get_mils(), 2)}, -{round(angle, 2)}          {round(Targets[0].get_mils(), 2)}, +{round(angle, 2)}"
	)
	num_spaces = int(num_spaces / 2)
	num_spaces = int(num_spaces - (len(str(round(Targets[2].get_mils(), 2))) / 2))
	print(str(round(Targets[0].get_mils(), 2)) + ", -" + str(round(angle, 2)) + "          " + str(round(Targets[0].get_mils(), 2)) + ", +" + str(round(angle, 2)))
	print(num_spaces*whitespace + str(round(Targets[2].get_mils(), 2)))
	print(str(round(Targets[1].get_mils(), 2)) + ", -" + str(round(angle, 2)) + "          " + str(round(Targets[1].get_mils(), 2)) + ", +" + str(round(angle, 2)))

@fire_mission_decorator
def calculate_x_fire_mission() -> None:
	#C: Not sure why we're using 135 degrees here.
	#C: We can do it much easier with a square rather than a rectangle.
	#TODO: Talk to Max about converting this to square
	#TODO: Update to use Target class
	angle_B = 135
	fm_targets_list: list[Target] = []
	
	#C: Is the original target the center of the X?
	original_target: float = float(input("Distance to original target: ")) # c

	square_length: float = float(input("Length of target square: "))
	isosceles_side_length: float = square_length / 2.0

	line_to_new_target: float = calculate_special_isosceles_hypotenuse(isosceles_side_length) # a
	distance_to_new_target: float = law_of_cosines_side(original_target, line_to_new_target, angle_B) # b
	distance_to_bottom_target: float = distance_to_new_target - square_length

	angular_difference: float = law_of_cosines_angle(original_target, distance_to_new_target, line_to_new_target) # A

	for index, distance in enumerate([distance_to_new_target, distance_to_bottom_target, original_target]):
		fm_targets_list.append(Target(index+1, distance, angular_difference))

	print_x_fire_mission(fm_targets_list, angular_difference)

@fire_mission_decorator
def calculate_line_fire_mission() -> None:
	fm_start_target: Target = Target(1) # distance is c
	fm_end_target: Target = Target(2) # distance is b
	fm_targets_list: list[Target] = [fm_start_target]

	num_points = int(input("How many points along the line will we fire upon?: "))

	angular_difference = calculate_angular_difference(fm_start_target, fm_end_target) # A
	angular_step = angular_difference / num_points # A / num_points
	line_of_fire = law_of_cosines_side(fm_start_target.distance, fm_end_target.distance, angular_difference)
	distance_step = line_of_fire / num_points # a / num_points

	angle_B = (math.sin(math.radians(angular_difference)) * fm_end_target.distance) / line_of_fire # B
	angle_B = math.asin(angle_B)
	angle_B = math.degrees(angle_B)
	angle_B = 180 - angle_B

	# C: I think this does the same thing as the old one. Please review thoroughly.
	for point in range(1, num_points+1):
		if fm_start_target.angle > fm_end_target.angle:
			angle = fm_start_target.angle - angular_step*point
			if point == 1:
				angle_B = 180 - angle_B
		else:
			angle = fm_start_target.angle + angular_step*point
		
		distance = distance_step*point
		new_distance = law_of_cosines_side(distance, fm_start_target.distance, angle_B) #b2
		fm_targets_list.append(Target(point, new_distance, angle))
	
	for index, target in enumerate(fm_targets_list):
		print(f"\nTARGET {index+1}: mils={target.get_mils()}, angle={target.angle}\n")

	avg_diff_mils = calculate_average_difference([target.get_mils() for target in fm_targets_list])
	print("mil diff:", avg_diff_mils)

	avg_diff_angles = calculate_average_difference([target.angle for target in fm_targets_list])
	print("angle diff:", avg_diff_angles)

def process_user_numeric_input(user_input: float, target_list: list[Target]) -> Target:
    #Append the target to the list
	user_target: Target = Target(
			#Target number = the number of targets in the list+1
			len(target_list) + 1,
			#We know the given input is a digit, so this will always work
			float(user_input)
		)
	print(f"mils to target: {user_target.get_mils()}")
	return user_target

def process_user_text_input(user_input: str) -> None:
	user_input = user_input.lower()
	match user_input:
		
		case "quit":
			sys.exit(0)

		case input_faction if user_input in factions:
			set_faction(input_faction)

		case ["fm" | "fire mission"]:
			calculate_line_fire_mission()

		case "x":
			calculate_x_fire_mission()

		case _:
			print(f"{user_input} is not a supported option. Please try again.")

if __name__ == "__main__":
	print_welcome_message()
	#C: I think I can override/extend this with an Action class. Need to need more into it.
	args = parser.parse_args()
	set_faction(args.faction)
	
	user_input: float | str

	#C: Eventually I'd like to be able to save/load targets so the user can see a history
	user_target_list: list[Target] = []
	while True:
		print(f"Current faction: {faction}")
		user_input = input("Input distance to target(m): ")
		#If the user input is a digit
		if user_input.isdigit():
			user_input = float(user_input)
			user_target_list.append(process_user_numeric_input(user_input, user_target_list))

		elif user_input.isalpha():
			process_user_text_input(user_input)