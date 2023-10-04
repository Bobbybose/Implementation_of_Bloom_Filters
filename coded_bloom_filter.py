import sys
import random
import math

def main():

    # Checking that the correct number of arguments was passed in
    if len(sys.argv) != 6:
        print("Invalid number of arguments")
        print("Program should be run in form 'python ./coded_bloom_filter.py num_sets num_elements_per_set num_filters num_bits_per_filter num_hashes'")
        return
    
    # Setting input parameters
    num_sets = int(sys.argv[1])
    num_elements_per_set = int(sys.argv[2])
    num_filters = int(sys.argv[3])
    num_bits_per_filter = int(sys.argv[4])
    num_hashes = int(sys.argv[5])

    # Creating bloom filters
    bloom_filters = []
    for filter_num in range(num_filters):
        bloom_filter = [0] * num_bits_per_filter
        bloom_filters.append(bloom_filter)

    # Generating sets of elements
    sets = []
    for set_num in range(num_sets):
        set = [0] * num_elements_per_set
        for element in range(num_elements_per_set):
            set[element] = random.randrange(1000000000)
        sets.append(set)

    # Uncomment next four lines to check for duplicate element ids between all sets
    mega_set = []
    for set in sets:
        mega_set += set
    check_id_dups(mega_set)

    # Codes for the sets
    set_codes = get_set_codes(num_sets)

    # Creating hashes
    hashes = []
    for hash in range(num_hashes):
        hashes.append(random.randrange(1000000000))

    # Encoding elements in all sets
    encode_elements(sets, set_codes, hashes, bloom_filters)

    # Looking up all elements
    elements_correctly_found = 0
    # For each set
    for set_num in range(num_sets):
        # Obtaining current sets' code
        set_code = set_codes[set_num]

        # Checking each element
        for element in sets[set_num]:
            # Reconstructed code for element
            calculated_code = ''
            # Checking if element is present in each bloom filter
            for bloom_filter in bloom_filters:
                # If element is present, record a 1 in the reconstructed code
                if lookup_element(element, hashes, bloom_filter):
                    calculated_code += '1'
                # If element is not present, record a 0 in the reconstructed code
                else:
                    calculated_code += '0'
            if calculated_code == set_code:
                elements_correctly_found += 1

    print("There are " + str(elements_correctly_found) + " elements whose lookup results are correct.")
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


# Inputs: Elements to encode, hashes to use for multi-hashing, bloom filters to encode in
# Returns: None
# Description: Encodes all elements into the bloom filters using a given number of hashes per element and the mapping algorithm
def encode_elements(sets, set_codes, hashes, bloom_filters):
    # For each set
    for set_num in range(len(sets)):
        # Obtaining set code
        set_code = set_codes[set_num]

        # For each element in the set
        for element in sets[set_num]:
            # Obtaining bit positions element hashes to
            element_hash_bits = hash_function(element, len(bloom_filters[0]), hashes)
            # Checking which filters to encode into
            for code_index in range(len(set_code)):
                # If the current bit is 1, encode into the associated filter
                if set_code[code_index] == '1':
                    # Encoding at each hashed position
                    for bit in element_hash_bits:
                        bloom_filters[code_index][bit] = 1
# encode_elements()


# Given: Element to lookup, hashes for multi-hashing, bloom filter to lookup in
# Returns: Boolean representing whether element is in filter or not
# Description: Return whether the element is in the given bloom filter
def lookup_element(element, hashes, bloom_filter):
    # Obtaining bits that element hashes to
    element_hash_bits = hash_function(element, len(bloom_filter), hashes)
    # Checking if all bits that element hashes into are 1
    for bit in element_hash_bits:
        if bloom_filter[bit] != 1:
            return False
    
    return True
# lookup_elements()


# Given: Number of sets
# Returns: Set codes for the number of sets given
# Description: Creates the set codes for the sets of elements, based off of the number of sets
def get_set_codes(num_sets):
    # Calculating the number of bits for the code
    num_bits = math.ceil(math.log(num_sets+1, 2))
    set_codes = []
    
    # Creating code for each set
    for set_num in range(1, num_sets+1):
        set_code = ''

        # Tracking current set number in order to modify as we build the bit string
        curr_count = set_num

        # Going through each bit in the code
        for bit_pos in range(num_bits):
            # If the set number is bigger than 2^(bit position), then the bit should be marked as 1
            if (curr_count != 0) and (curr_count >= (2**(num_bits-bit_pos-1))):
                set_code += '1'
                # Subtracting out the part of the set number that the current bit represents
                curr_count -= 2**(num_bits-bit_pos-1)
            else:
                set_code += '0'

        set_codes.append(set_code)  
            
    return set_codes        
# get_set_codes()


main()