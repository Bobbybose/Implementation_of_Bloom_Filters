import sys
import random

def main():

    # Checking that the correct number of arguments was passed in
    if len(sys.argv) != 4:
        print("Invalid number of arguments")
        print("Program should be run in form 'python ./bloom_filter.py num_elements_to_encode num_bits_in_filter num_hashes'")
        return
    
    # Setting input parameters
    num_elements_to_encode = int(sys.argv[1])
    num_bits_in_filter = int(sys.argv[2])
    num_hashes = int(sys.argv[3])

    # Creating Bloom Filter
    bloom_filter = [0] * num_bits_in_filter

    # Generating set A elements to encode
    set_A_elements = [0] * num_elements_to_encode
    for index in range(num_elements_to_encode):
        set_A_elements[index] = random.randrange(1000000000)

    # Uncomment next line to check for duplicate element ids
    #check_id_dups(set_A_elements)

    # Creating hashes
    hashes = []
    for hash in range(num_hashes):
        hashes.append(random.randrange(1000000000))

    # Encoding set A elements into bloom filter
    encode_elements(set_A_elements, hashes, bloom_filter)

    # Checking number of set A elements in the filter
    num_elements_in_filter = lookup_elements(set_A_elements, hashes, bloom_filter)
    print("There are " + str(num_elements_in_filter) + " elements from set A in the filter.")

    # Generating set B elements
    set_B_elements = [0] * num_elements_to_encode
    for index in range(num_elements_to_encode):
        set_B_elements[index] = random.randrange(1000000000)

    # Uncomment next line to check for duplicate element ids
    #check_id_dups(set_B_elements)

    # Checking number of set B elements in the filter
    num_elements_in_filter = lookup_elements(set_B_elements, hashes, bloom_filter)
    print("There are " + str(num_elements_in_filter) + " elements from set B in the filter.")
# main()


# Inputs: Id of element to hash, number of bits in the bloom filter, hashes to use for multi-hashing
# Returns: Bloom filter bit positions where element encodes to
# Description: Folding hash function implementation based from https://www.herevego.com/hashing-python/
#   Split number into two (first four digits, and then rest of number)
#   Add two parts and then do num % num_table_entries
def hash_function(element_id, num_bits, hashes):
    # Obtaining hash ids
    multi_hashing_element_ids = []
    for hash in hashes:
        multi_hashing_element_ids.append(element_id^hash)
    
    # Obtaining bit positions element hashes to
    element_hash_bits = []
    for current_id in multi_hashing_element_ids:
        # Error if id isn't more than four digits long; correcting here
        if current_id < 10000:
            current_id += 10000
        split_id_sum = int(str(current_id)[:4]) + int(str(current_id)[4:])
        element_hash_bits.append(split_id_sum % num_bits)

    return element_hash_bits
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
        # Obtaining bits that element hashes to
        element_hash_bits = hash_function(element, len(bloom_filter), hashes)

        # Encoding element at each hashed bit
        for bit in element_hash_bits:
            bloom_filter[bit] = 1
# encode_elements()


# Given: Set of elements, hashes for multi-hashing, bloom filter to lookup in
# Returns: The number of elements in the set that are in the bloom filter
# Description: Return the number of elements in a set that are found in a given bloom filter
def lookup_elements(elements, hashes, bloom_filter):
    # Recording the number of elements present from the set
    num_elements_in_filter = 0
    for element in elements:
        # Obtaining bits that element hashes to
        element_hash_bits = hash_function(element, len(bloom_filter), hashes)

        # Checking if all bits that element hashes into are 1
        in_filter = True
        for bit in element_hash_bits:
            if bloom_filter[bit] != 1:
                in_filter = False
        
        # If element is present, increment counter
        if in_filter:
            num_elements_in_filter += 1

    return num_elements_in_filter
# lookup_elements()

main()