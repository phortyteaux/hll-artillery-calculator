"""********************************************************************************
* Welcome to the HLL Artillery Calculator!                                        *
* This program accepts a distance in meters and returns a value of mils to adjust *
* your artillery barrel to. Run with 'de', 'us', or 'ru' to set the appropriate   *
* calculation based on which faction you are playing.                             *
********************************************************************************"""

import sys

def us_de_calculate(distance):
	mils = (-0.237 * float(distance)) + 1002
	return round(mils)

def ru_calculate(distance):
	mils = (-0.213 * float(distance)) + 1141
	return round(mils)

factions = ("us", "de", "ru")
faction = ""

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

distance = 0
print("Welcome to the HLL Artillery Calculator!")
print("Enter a distance in meters to get the appropriate amount of mils to adjust your gun to.")
print("Enter 'quit' to quit.")
print("Enter a new faction to change the calculation.")
while True:
	distance = input("distance to target(m): ")
	if distance == "quit":
		sys.exit(0)

	if distance in factions:
		faction = distance
		print("Changed calulation to", faction)
		continue

	if faction == "us" or faction == "de":
		try:
			mils = us_de_calculate(distance)
			print("mils to target:", mils)
		except:
			continue
	elif faction == "ru":
		try:
			mils = ru_calculate(distance)
			print("mils to target:", mils)
		except:
			continue