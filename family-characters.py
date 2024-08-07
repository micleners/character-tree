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

# Extract names from anchor elements within 'index_letter', excluding names with spaces
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
def generate_age(min_age=1, max_age=100):
    return random.randint(min_age, max_age)

# Helper function to generate random sex
def generate_sex():
    return random.choices(sexes, weights=[4, 4, 1])[0]

# Helper function to generate random race
def generate_race():
    return random.choices(races, weights=[7, 1, 1, 1])[0]

# Helper function to find or create a person
def find_or_create_person(villagers, name):
    for villager in villagers:
        if villager['name'] == name:
            return villager
    new_villager = {
        "name": name,
        "age": generate_age(),
        "sex": generate_sex(),
        "race": generate_race(),
        "relationships": []
    }
    villagers.append(new_villager)
    return new_villager

# Create a list of villagers with attributes
villagers = []
for name in random_names:
    villager = {
        "name": name,
        "age": generate_age(),
        "sex": generate_sex(),
        "race": generate_race(),
        "relationships": []
    }
    villagers.append(villager)

# Add relationships
def add_relationships(villagers):
    family_units = []

    # Create family units
    for _ in range(50):  # Create 50 family units
        parents = []
        children = []

        # Create parents
        parent1 = random.choice(villagers)
        parent2_candidates = [v for v in villagers if abs(v['age'] - parent1['age']) <= 20 and v != parent1]
        if not parent2_candidates:
            continue  # Skip if no suitable parent2 found
        parent2 = random.choice(parent2_candidates)
        parents.append(parent1)
        parents.append(parent2)

        # Ensure parents are married
        parent1['relationships'].append({"relation": "spouse", "name": parent2['name']})
        parent2['relationships'].append({"relation": "spouse", "name": parent1['name']})

        # Create children
        for _ in range(random.randint(1, 5)):  # Each family can have 1 to 5 children
            child = find_or_create_person(villagers, random.choice(random_names))
            child_age_max = min(parent1['age'], parent2['age']) - 18
            if child_age_max < 1:
                continue  # Skip if no valid age range for children
            child['age'] = generate_age(1, child_age_max)
            if child['age'] >= min(parent1['age'], parent2['age']):
                child['age'] = generate_age(1, child_age_max)
            child['relationships'].append({"relation": "parent", "name": parent1['name']})
            child['relationships'].append({"relation": "parent", "name": parent2['name']})
            parent1['relationships'].append({"relation": "child", "name": child['name']})
            parent2['relationships'].append({"relation": "child", "name": child['name']})
            children.append(child)

        family_units.append({"parents": parents, "children": children})

    # Create extended families (grandparents, aunts, uncles, cousins)
    for family in family_units:
        parents = family['parents']
        children = family['children']

        for parent in parents:
            # Create grandparents
            if random.random() > 0.5:  # 50% chance to have grandparents
                grandparent = find_or_create_person(villagers, random.choice(random_names))
                grandparent['age'] = parent['age'] + random.randint(20, 40)
                grandparent['relationships'].append({"relation": "child", "name": parent['name']})
                parent['relationships'].append({"relation": "parent", "name": grandparent['name']})
                for child in children:
                    child['relationships'].append({"relation": "grandparent", "name": grandparent['name']})
                    grandparent['relationships'].append({"relation": "grandchild", "name": child['name']})

            # Create aunts and uncles (siblings of parents)
            if random.random() > 0.5:  # 50% chance to have aunts/uncles
                sibling = find_or_create_person(villagers, random.choice(random_names))
                sibling['age'] = parent['age'] + random.randint(-20, 20)
                sibling['relationships'].append({"relation": "sibling", "name": parent['name']})
                parent['relationships'].append({"relation": "sibling", "name": sibling['name']})
                for child in children:
                    child['relationships'].append({"relation": "aunt/uncle", "name": sibling['name']})
                    sibling['relationships'].append({"relation": "niece/nephew", "name": child['name']})

    return villagers

# Add relationships
def add_relationships(villagers):
    family_units = []

    # Create family units
    for _ in range(50):  # Create 50 family units
        parents = []
        children = []

        # Create parents
        parent1 = random.choice(villagers)
        parent2_candidates = [v for v in villagers if abs(v['age'] - parent1['age']) <= 20 and v != parent1]
        if not parent2_candidates:
            continue  # Skip if no suitable parent2 found
        parent2 = random.choice(parent2_candidates)
        parents.append(parent1)
        parents.append(parent2)

        # Ensure parents are married
        parent1['relationships'].append({"relation": "spouse", "name": parent2['name']})
        parent2['relationships'].append({"relation": "spouse", "name": parent1['name']})

        # Create children
        for _ in range(random.randint(1, 5)):  # Each family can have 1 to 5 children
            child = find_or_create_person(villagers, random.choice(random_names))
            child_age_max = min(parent1['age'], parent2['age']) - 18
            if child_age_max < 1:
                continue  # Skip if no valid age range for children
            child['age'] = generate_age(1, child_age_max)
            if child['age'] >= min(parent1['age'], parent2['age']):
                child['age'] = generate_age(1, child_age_max)
            child['relationships'].append({"relation": "parent", "name": parent1['name']})
            child['relationships'].append({"relation": "parent", "name": parent2['name']})
            parent1['relationships'].append({"relation": "child", "name": child['name']})
            parent2['relationships'].append({"relation": "child", "name": child['name']})
            children.append(child)

        family_units.append({"parents": parents, "children": children})

    # Create extended families (grandparents, aunts, uncles, cousins)
    for family in family_units:
        parents = family['parents']
        children = family['children']

        for parent in parents:
            # Create grandparents
            if random.random() > 0.5:  # 50% chance to have grandparents
                grandparent = find_or_create_person(villagers, random.choice(random_names))
                grandparent['age'] = parent['age'] + random.randint(20, 40)
                grandparent['relationships'].append({"relation": "child", "name": parent['name']})
                parent['relationships'].append({"relation": "parent", "name": grandparent['name']})
                for child in children:
                    child['relationships'].append({"relation": "grandparent", "name": grandparent['name']})
                    grandparent['relationships'].append({"relation": "grandchild", "name": child['name']})

            # Create aunts and uncles (siblings of parents)
            if random.random() > 0.5:  # 50% chance to have aunts/uncles
                sibling = find_or_create_person(villagers, random.choice(random_names))
                sibling['age'] = parent['age'] + random.randint(-20, 20)
                sibling['relationships'].append({"relation": "sibling", "name": parent['name']})
                parent['relationships'].append({"relation": "sibling", "name": sibling['name']})
                for child in children:
                    child['relationships'].append({"relation": "aunt/uncle", "name": sibling['name']})
                    sibling['relationships'].append({"relation": "niece/nephew", "name": child['name']})

    return villagers

villagers = add_relationships(villagers)

villagers_json = json.dumps(villagers, indent=4)

# Copy the villagers list to clipboard
pyperclip.copy(villagers_json)

# Save the output to a file
with open("family-characters.json", "w") as file:
    file.write(villagers_json)
