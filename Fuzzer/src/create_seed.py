#!/usr/bin/python3

""" Jeremy Escobar, CSE 543, Fall 2023, 11/20/2023 """


def create_seed():
    """ 
    Create a seed file for the fuzzer to read from and be  
    used for prog_3-9 to crash the programs with the fuzzer 
    """
    seed_creation = b'eeee \x00bbbbbbbbbbbbbbbbbbbb\x10\x00\x00\x00EEEEEEEEEEEEEEEEEEEE'

    with open('seed', 'wb') as f:  # wb = write binary
        f.write(seed_creation)     # Write the seed to the file


if __name__ == "__main__":
    create_seed()  # Execute the seed creation
    print("Seed file created successfully.")
