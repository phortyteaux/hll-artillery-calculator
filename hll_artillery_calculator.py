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

if sys.argv[1] != "us" and sys.argv[1] != "de" and sys.argv[1] != "ru":
	print("Invalid command line option! Please re-run with 'us', 'de', or 'ru' as the only additional argument")
	sys.exit(0)

distance = 0
print("Welcome to the HLL Artillery Calculator! Enter a distance in meters to get the appropriate amount of mils to adjust your gun to. Enter 'quit' to quit.")
while True:
	distance = input("distance to target(m): ")
	if distance == "quit":
		sys.exit(0)

	if sys.argv[1] == "us" or sys.argv[1] == "de":
		try:
			mils = us_de_calculate(distance)
			print("mils to target:", mils)
		except:
			continue
	elif sys.argv[1] == "ru":
		try:
			mils = ru_calculate(distance)
			print("mils to target:", mils)
		except:
			continue