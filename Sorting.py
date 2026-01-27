# This code generates a list of random names and sorts them alphabetically afterwards. 
# It logs the steps in a separate log file.
# The names should be generated using the vscode-faker extension.

import random
import string
import logging
import faker

# Set up logging
logging.basicConfig(filename='sorting.log', level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()
# Initialize Faker
fake = faker.Faker()

def generate_random_names(num_names):
    names = [fake.name() for _ in range(num_names)]
    logger.info(f'Generated names: {names}')
    return names

def sort_names(names):
    sorted_names = sorted(names)
    logger.info(f'Sorted names: {sorted_names}')
    return sorted_names

if __name__ == "__main__":
    num_names = 10  # You can change this number to generate more or fewer names
    names = generate_random_names(num_names)
    sorted_names = sort_names(names)
    print("Unsorted Names:")
    print(names)
    print("\nSorted Names:")
    print(sorted_names)
