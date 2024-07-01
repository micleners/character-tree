import requests
from bs4 import BeautifulSoup
import random
import pyperclip
import json

# Define the URL
url = "https://dmnes.org/names"

# Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements with class 'index_letter'
index_letters = soup.find_all(class_='index_letter')

# Extract names from anchor elements within 'index_letter'
names = []
for letter in index_letters:
    anchors = letter.find_all('a')
    for anchor in anchors:
        name = anchor.get_text()
        if ' ' not in name:
            names.append(name)

# Ensure unique names
names = list(set(names))

# Generate a list of 300 random unique names
random_names = random.sample(names, min(300, len(names)))

# Define possible attributes
sexes = ['male', 'female', 'non-binary']
races = ['human', 'elf', 'dwarf', 'halfling']

# Helper function to generate random age
def generate_age():
    return random.randint(1, 100)

# Helper function to generate random sex
def generate_sex():
    return random.choices(sexes, weights=[4, 4, 1])[0]

# Helper function to generate random race
def generate_race():
    return random.choices(races, weights=[11, 1, 1, 1])[0]

# Create a list of villagers with attributes
villagers = []
for name in random_names:
    villager = {
        "name": name,
        "age": generate_age(),
        "sex": generate_sex(),
        "race": generate_race(),
        "relationships": []  # Placeholder for relationships
    }
    villagers.append(villager)


villagers_json = json.dumps(villagers, indent=4)

# Copy the villagers list to clipboard
pyperclip.copy(villagers_json)

# Save the output to a file
with open("basic-characters.json", "w") as file:
    file.write(villagers_json)
