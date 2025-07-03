# Compiler

A Python-based compiler project implementing a lexer and parser for a custom language, using PLY (Python Lex-Yacc). This project demonstrates how to write a full-featured lexer and parser capable of handling declarations, function definitions, control statements, and more.

## Features

- Lexical analysis and parsing for a C-like custom language
- Handles variables, functions, types, control flows (if, else, for, etc.), and more
- Based on PLY (Python Lex-Yacc)

## Prerequisites

- **Python 3.6+**  
  Make sure Python is installed and available in your environment.

- **PLY package**  
  Install PLY via pip:

  ```bash
  pip install ply
  ```

## Installation

### Windows

1. **Clone the repository:**
    ```bash
    git clone https://github.com/HoomanMoradnia/Compiler.git
    cd Compiler
    ```

2. **Install dependencies:**
    ```bash
    pip install ply
    ```

3. **Run the compiler:**
    ```bash
    python Compiler.py
    ```

   You can modify the test input at the bottom of `Compiler.py` or adjust it to take input from a file.

---

### Linux

1. **Clone the repository:**
    ```bash
    git clone https://github.com/HoomanMoradnia/Compiler.git
    cd Compiler
    ```

2. **Install dependencies:**
    ```bash
    pip3 install ply
    ```

3. **Run the compiler:**
    ```bash
    python3 Compiler.py
    ```

   You can modify the test input at the bottom of `Compiler.py` or redirect input as needed.

---

## Usage

- The main file is `Compiler.py`. It contains both the lexer and parser logic.
- By default, running the script will process sample code defined in the `if __name__ == "__main__":` block at the end of `Compiler.py`.
- To parse your own code, you can replace the `test_input` variable in the script or refactor the file to accept external input.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Hooman Moradnia
