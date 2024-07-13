# Importing the required module
from unqlite import UnQLite
import math
import re

# Initialize the database and data collection
db = UnQLite('sample.db')
data = db.collection('data')


def FindBusinessBasedOnCity(cityToSearch, saveLocation1, data):
    # Check for special characters in city name
    if not re.match("^[A-Za-z\s]+$", cityToSearch):
        print("Invalid city name provided.")  # Check for special characters in city name
        return  # Return if invalid city name

    results = []

    matching_entries = list(filter(lambda obj: obj['city'] == cityToSearch, data))
    if not matching_entries:
        print(f"No businesses found in {cityToSearch}.")
        return  # Return if no businesses found in city

    for entry in matching_entries:
        line = f"{entry['name']}${entry['full_address']}${entry['city']}${entry['state']}"
        results.append(line)  # Add business name to results

    try:
        with open(saveLocation1, 'w') as file:  # Write results to file
            file.write('\n'.join(results))
    except Exception as e:
        print(f"Error writing to file: {e}")  # Print error message if file write fails


def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, data):
    if not (isinstance(myLocation[0], (int, float)) and isinstance(myLocation[1], (int, float))):
        # Check if latitude and longitude are numbers (int or float)
        print("Invalid latitude or longitude provided.")
        return

    # Ensure provided categories exist in the data
    existing_categories = set([item for sublist in [entry['categories'] for entry in data] for item in sublist])
    # list of categories
    for category in categoriesToSearch:
        if category not in existing_categories:
            print(f"Category {category} does not exist.")
            # Ensure provided categories exist in the data
            return

    results = []

    for entry in data:
        if any(category in entry['categories'] for category in categoriesToSearch):
            # Check if business has any of the provided categories
            distance = calculate_distance(myLocation[0], myLocation[1], entry['latitude'], entry['longitude'])
            # Calculate distance between two points
            if distance <= maxDistance:
                results.append(entry['name'])  # Add business name to results

    try:
        with open(saveLocation2, 'w') as file:  # Write results to file
            file.write('\n'.join(results))
    except Exception as e:
        print(f"Error writing to file: {e}")  # Print error message if file write fails


def calculate_distance(latitude2, longitude2, latitude1, longitude1):
    earth_radius_miles = 3959  # Radius of the Earth in miles
    latitude1_rad = math.radians(latitude1)  # Convert latitude1 to radians
    latitude2_rad = math.radians(latitude2)  # Convert latitude2 to radians
    delta_latitude_rad = math.radians(latitude2 - latitude1)  # Delta latitude in radians
    delta_longitude_rad = math.radians(longitude2 - longitude1)  # Delta longitude in radians

    haversine_term = math.sin(delta_latitude_rad / 2) ** 2 + \
                     math.cos(latitude1_rad) * math.cos(latitude2_rad) * \
                     math.sin(delta_longitude_rad / 2) ** 2  # Haversine formula term

    arc_length = 2 * math.atan2(math.sqrt(haversine_term),
                                math.sqrt(1 - haversine_term))  # Arc length using the Haversine formula

    distance_miles = earth_radius_miles * arc_length  # Distance in miles

    return distance_miles  # Return distance in miles


true_results = [
    '3 Palms$7707 E McDowell Rd, Scottsdale, AZ 85257$Scottsdale$AZ',
    "Bob's Bike Shop$1608 N Miller Rd, Scottsdale, AZ 85257$Scottsdale$AZ",
    'Ronan & Tagart, PLC$8980 E Raintree Dr, Ste 120, Scottsdale, AZ 85260$Scottsdale$AZ',
    "Sangria's$7700 E McCormick Pkwy, Scottsdale, AZ 85258$Scottsdale$AZ",
    'Turf Direct$8350 E Evans Rd, Scottsdale, AZ 85260$Scottsdale$AZ'
]

try:
    FindBusinessBasedOnCity('Scottsdale', 'output_city.txt', data)
except NameError as e:
    print(
        'The FindBusinessBasedOnCity function is not defined! You must run the cell containing the function before running this evaluation cell.')
except TypeError as e:
    print(e)
    print("The FindBusinessBasedOnCity function is supposed to accept three arguments. Yours does not!")

try:
    opf = open('output_city.txt', 'r')
    lines = opf.readlines()
    opf.close()

    if len(lines) != 5:
        print("The FindBusinessBasedOnCity function does not find the correct number of results, should be 5.")

    lines = [line.strip() for line in lines]

    if sorted(lines) == sorted(true_results):
        print(
            "Correct! Your FindBusinessByCity function passes these test cases. This does not cover all possible test edge cases, however, so make sure that your function covers them before submitting!")

except FileNotFoundError as e:
    print("The FindBusinessBasedOnCity function does not write data to the correct location.")

true_results = ['Nothing Bundt Cakes', 'Olive Creations', 'P.croissants', 'The Seafood Market']
try:
    FindBusinessBasedOnLocation(['Food', 'Specialty Food'], [33.3482589, -111.9088346], 30, 'output_loc.txt', data)

except NameError as e:
    print(
    'The FindBusinessBasedOnLocation function is not defined! You must run the cell containing the function before running this evaluation cell.')
except TypeError as e:
    print("The FindBusinessBasedOnLocation function is supposed to accept five arguments. Yours does not!")
try:
    opf = open('output_loc.txt', 'r')
except FileNotFoundError as e:
    print("The FindBusinessBasedOnLocation function does not write data to the correct location.")
lines = opf.readlines()
if len(lines) != 4:
    print("The FindBusinessBasedOnLocation function does not find the correct number of results, should be only 4.")
lines = [line.strip() for line in lines]
if sorted(lines) == sorted(true_results):
    print(
        "Correct! Your FindBusinessBasedOnLocation function passes these test cases. This does not cover all possible edge cases, so make sure your function does before submitting.")
