import sys
import random

def main():

    # Checking that the correct number of arguments was passed in
    if len(sys.argv) != 6:
        print("Invalid number of arguments")
        print("Program should be run in form 'python ./bloom_filter.py num_elements_to_encode num_elements_to_remove num_elements_to_add num_counters_in_filter num_hashes'")
        return
    
    # Setting input parameters
    num_elements_to_encode = int(sys.argv[1])
    num_elements_to_remove = int(sys.argv[2])
    num_elements_to_add = int(sys.argv[3])
    num_counters_in_filter = int(sys.argv[4])
    num_hashes = int(sys.argv[5])

    # Creating Bloom Filter
    bloom_filter = [0] * num_counters_in_filter

    # Generating set A elements to encode
    set_A_elements = [0] * num_elements_to_encode
    for index in range(num_elements_to_encode):
        set_A_elements[index] = random.randrange(10000000)

    # Uncomment next line to check for duplicate element ids
    #check_id_dups(set_A_elements)

    # Creating hashes
    hashes = []
    for hash in range(num_hashes):
        hashes.append(random.randrange(10000000))

    # Encoding set A elements into bloom filter
    encode_elements(set_A_elements, hashes, bloom_filter)
    
    # Removing 500 elements from set A from the bloom filter
    remove_elements(set_A_elements[0:num_elements_to_remove], hashes, bloom_filter)

    # Generating more elements to encode
    additional_elements = [0] * num_elements_to_add
    for index in range(num_elements_to_add):
        additional_elements[index] = random.randrange(10000000)

    # Uncomment next line to check for duplicate element ids
    #check_id_dups(additional_elements)

    # Encoding set B elements into bloom filter
    encode_elements(additional_elements, hashes, bloom_filter)
    
    # Checking number of set A elements in the filter
    num_elements_in_filter = lookup_elements(set_A_elements, hashes, bloom_filter)
    print("There are " + str(num_elements_in_filter) + " elements from set A in the filter.")
# main()


# Inputs: Id of element to hash, number of bits in the bloom filter, hashes to use for multi-hashing
# Returns: Bloom filter counters that element encodes to
# Description: Folding hash function implementation based from https://www.herevego.com/hashing-python/
#   Split number into two (first four digits, and then rest of number)
#   Add two parts and then do num % num_table_entries
def hash_function(element_id, num_bits, hashes):
    # Obtaining hash ids
    multi_hashing_element_ids = []
    for hash in hashes:
        multi_hashing_element_ids.append(element_id^hash)
        
    # Obtaining counters element hashes to
    element_hash_counters = []
    for current_id in multi_hashing_element_ids:
        # Error if id isn't more than four digits long; correcting here
        if current_id < 10000:
            current_id += 10000
        split_id_sum = int(str(current_id)[:4]) + int(str(current_id)[4:])
        element_hash_counters.append(split_id_sum % num_bits)

    return element_hash_counters
# hash_function()


# Givens: List of element ids
# Returns: None
# Description: Checks for duplicate element ids in a list [For testing purposes]
def check_id_dups(elements):
    duplicate_ids = []
    dup = 0
    for element in elements:
        for element2 in elements:
            if element == element2:
                if element != 0:   # Important if checking for duplicates in bloom filter
                    dup += 1
        if dup > 1:             # dup will be 1 if there are no duplicates (1 count of element id)
            if duplicate_ids.count(element) == 0:
                duplicate_ids.append(element)
                print("Duplicate id " + str(element) + " found with " + str(dup) + " counts")
        dup = -1
# check_id_dups()


# Inputs: Elements to encode, hashes to use for multi-hashing, bloom filter to encode in
# Returns: None
# Description: Encodes all elements into the bloom filter using a given number of hashes per element
def encode_elements(elements, hashes, bloom_filter):
    for element in elements:
        # Obtaining counters that element hashes to
        element_hash_counters = hash_function(element, len(bloom_filter), hashes)

        # Incrementing each counter element hashes to
        for counter in element_hash_counters:
            bloom_filter[counter] += 1
# encode_elements()


# Inputs: Elements to remove, hashes to use for multi-hashing, bloom filter to remove from
# Returns: None
# Description: Removes all elements from a bloom filter using a given number of hashes per element
def remove_elements(elements, hashes, bloom_filter):
    for element in elements:
        element_hash_counters = hash_function(element, len(bloom_filter), hashes)

        for counter in element_hash_counters:
            bloom_filter[counter] -= 1
# remove_elements()


# Given: Set of elements, hashes for multi-hashing, bloom filter to lookup in
# Returns: The number of elements in the set that are in the bloom filter
# Description: Return the number of elements in a set that are found in a given bloom filter
def lookup_elements(elements, hashes, bloom_filter):
    # Recording the number of elements present from the set
    num_elements_in_filter = 0
    for element in elements:
        # Obtaining counters that element hashes to
        element_hash_counters = hash_function(element, len(bloom_filter), hashes)

        # Checking that all counters element hashes to are > 0
        in_filter = True
        for counter in element_hash_counters:
            if bloom_filter[counter] == 0:
                in_filter = False
        
        # If element is present, increment counter
        if in_filter:
            num_elements_in_filter += 1

    return num_elements_in_filter
# lookup_elements()

main()