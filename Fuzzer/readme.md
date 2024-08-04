### README Overview

**Project Title:** Fuzz, Them All - A Dumb Mutative Fuzzer

**Author:** Jeremy Escobar  
**School of Computing and Augmented Intelligence, Arizona State University**  

---

#### **Abstract**
This project explores the development and application of a dumb mutative fuzzer designed to uncover vulnerabilities in binary programs. The fuzzer was implemented in Python, focusing on introducing controlled mutations in seed input to detect crashes and other anomalous behaviors in target programs. This work emphasizes deterministic output generation for effective debugging and analysis.

---

#### **Directory Structure**

- **`/src`**  
  Contains the source code for the fuzzer implementation. The main Python script reads the seed file, applies mutations, and outputs the modified data for fuzz testing.

- **`/programs`**  
  Includes the binary programs that were subjected to fuzz testing. These programs were used to validate the fuzzer's effectiveness in detecting vulnerabilities.

---

#### **Project Breakdown**

1. **Introduction**
   - **Objective:** The primary goal was to create a dumb mutative fuzzer capable of introducing random mutations into seed inputs and testing binary programs for vulnerabilities such as crashes or segmentation faults.
   - **Approach:** The fuzzer operates by applying a predefined probability of mutation to each byte of the input, with the capability to extend inputs to test for buffer overflows. The output is deterministic, ensuring consistent results for debugging.

2. **Fuzzer Implementation**
   - **Mutation Logic:** The fuzzer modifies the input data based on a 13% mutation probability, as specified in the project guidelines. Each byte of the input has a chance to be altered, mimicking real-world data corruption scenarios.
   - **Input Extension:** Every 500 iterations, the fuzzer appends additional characters to the input, simulating buffer overflow attacks to test the program's resilience.
   - **Deterministic Output:** The fuzzer generates consistent outputs given the same initial seed and conditions, which is crucial for reproducing and analyzing crashes.
   - **Non-Interference:** The fuzzer maintains a clean test input stream by outputting only mutated data to stdout, while diagnostic information is sent to stderr.

3. **Testing and Analysis**
   - The fuzzer was tested on a set of programs (`prog_0` through `prog_9`), and the conditions leading to crashes were documented. This data was used to analyze the vulnerabilities and improve the fuzzer's mutation strategies.

4. **Conclusion**
   - The project provided a deep dive into fuzz testing and highlighted the importance of controlled mutations and seed selection in uncovering program vulnerabilities. Future enhancements could include smarter mutation strategies and optimization for performance.

---

#### **References**
1. T. Green, "10 top fuzzing tools: Finding the weirdest application errors," CSO Online, 06-Apr-2022. [Online]. Available: https://www.csoonline.com/article/568135/9-top-fuzzing-tools-finding-the-weirdest-application-errors.html [Accessed: 12-Nov-2023].
2. "Fuzzing," OWASP Foundation. [Online]. Available: https://owasp.org/www-community/Fuzzing [Accessed: 16-Nov-2023]. 

---

