#!/bin/bash
#fuzzer_tester.sh

# This script is used to test the fuzzer.py script.
# It takes a program number as an argument and runs the fuzzer.py script
# with a specific PRNG seed and number of iterations.
# It then executes the program with the crashing input and checks for a crash.
# If a crash is detected, it writes the crashing input to a .crash file and
# the PRNG seed and number of iterations to a .txt file.
# If no crash is detected, it prints a message to the console.

# Jeremy Escobar, 11/20/2023
# CSE 543, Spring 2023
# Arizona State University

# Check if program number is provided
if [[ -z $1 ]]; then
    echo "Error: Provide a program number as an argument."
    exit 123
fi

# Assign specific number of iterations based on the program number
# becuase after testing these values crash the programs. 
declare -A iteration_mapping=(
    [1]=5000 [0]=5000 [2]=4286
    [3]=13000 [5]=13000 [9]=12000  
    [4]=25000  
    [6]=25000 [7]=2000 [8]=3500 
)

# Generate a random prng_seed value or use a mapped one
# because testing has shown these PRNG values crash the programs
case $1 in
    0)
        prng_seed=22209  # please run prog_0 in test_programs folder
        ;;
    1)
        prng_seed=42105  # please run prog_1 in test_programs folder
        ;;
    2)
        prng_seed=25920  # please run prog_2 in test_programs folder
        ;;
    3)  
        prng_seed=20506  # Use this seed for program 3 after throuough testing
        ;;
    4)  
        prng_seed=23656  # Use this seed for program 4 after throuough testing
        ;;
    5) 
        prng_seed=30324  # Use this seed for program 6 after throuough testing
        ;;
    6)
        prng_seed=33433  # Use this seed for program 6 after throuough testing
        ;;
    7)
        prng_seed=26625  # Use this seed for program 7 after throuough testing
        ;;
    8)
        prng_seed=32522  # Use this seed for program 8 after throuough testing
        ;;
    9)
        prng_seed=33515  # Use this seed for program 9 after throuough testing
        ;;
    *)
        prng_seed=$((10000 + $RANDOM % 1000000))  # Generate a random seed for all other programs
        ;;
esac

num_iterations=${iteration_mapping[$1]:-3500}  # Default to 3500 if not specified in the map

echo "Fuzzing Program_$1 with $num_iterations iterations."
echo "PRNG seed is: $prng_seed"

# Generate the crashing input using fuzzer
./fuzzer "$prng_seed" "$num_iterations" > temp_crash_input
crashing_input=$(cat temp_crash_input)

# uncomment the line below to use the python executable fuzzer instead
#crashing_input=$(./fuzzer "$prng_seed" "$num_iterations")

# Execute the program with the crashing input and capture the exit status
{ echo "$crashing_input" | ./prog_$1 > /dev/null 2>&1; } 2>/dev/null
status=$?

# Check for crash and output the appropriate files
if [[ $status -ne 0 ]]; then
    echo -e "\nProgram_$1 crashed successfully with exit code ($status)"

    # Write the crashing input to the .crash file
    echo "$crashing_input" > "./prog_$1.crash"
    #echo "Crashing input = $crashing_input"

    # Write the PRNG seed and number of iterations to the .txt file
    echo "$prng_seed" > "./prog_$1.txt"
    echo "$num_iterations" >> "./prog_$1.txt"

    echo "Crashing input written to prog_$1.crash"
    echo "Seed and iterations written to prog_$1.txt"
else
    echo -e "\nProgram ./prog_$1 completed without crashing."
fi