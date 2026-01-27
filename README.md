# LEG-16 Compiler

A multi-stage compiler for a simple programming language that targets the LEG-16 (16-bit) architecture. This compiler demonstrates the fundamental phases of compilation: lexical analysis, parsing, semantic analysis, and intermediate representation generation.

## 📋 Table of Contents

- [Overview](#overview)
- [Language Features](#language-features)
- [Project Structure](#project-structure)
- [Compiler Pipeline](#compiler-pipeline)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Architecture Details](#architecture-details)
- [Contributing](#contributing)

## 🎯 Overview

The LEG-16 compiler is an educational compiler project that transforms a simple high-level language into an intermediate representation suitable for a 16-bit target architecture. The compiler implements classical compilation phases and provides detailed logging for understanding the compilation process.

**Key Features:**
- ✅ Lexical analysis with regex-based tokenization
- ✅ Recursive descent parser with AST generation
- ✅ Semantic analysis with symbol table management
- ✅ IR (Intermediate Representation) generation
- ✅ ISA definition for LEG-16 architecture
- ✅ Comprehensive error handling and logging

## 🚀 Language Features

The source language supports the following constructs:

### Variable Declarations
```
var x = 10;
var y = 20;
```

### Binary Operations
- **Addition**: `+`
- **Subtraction**: `-`
- **Modulo**: `%`

```
var result = a + b;
var diff = x - y;
var remainder = a % b;
```

### Print Statements
```
print result
```

### Comments
```
// This is a comment
var x = 5;  // inline comment
```

## 📁 Project Structure

```
leg-16-compiler/
├── ast_leg.py          # Abstract Syntax Tree node definitions
├── lexer.py            # Lexical analyzer (tokenizer)
├── parser.py           # Recursive descent parser
├── symbol_table.py     # Symbol table and semantic analyzer
├── main.py             # Main entry point and example usage
├── backend/
│   └── isa.py          # LEG-16 Instruction Set Architecture
└── ir/
    ├── __init__.py     # IR module initialization
    ├── builder.py      # IR builder (AST to IR translator)
    ├── instructions.py # IR instruction definitions
    ├── program.py      # IR program container
    └── values.py       # IR value types (temps, constants, slots)
```

## 🔄 Compiler Pipeline

The compilation process consists of the following stages:

### 1. **Lexical Analysis** (`lexer.py`)
Converts source code into a stream of tokens.

**Supported Tokens:**
- Keywords: `var`, `print`
- Operators: `=`, `+`, `-`, `%`
- Literals: Numbers (`\d+`)
- Identifiers: `[a-zA-Z_]\w*`
- Delimiters: `;`
- Comments: `//`

**Example:**
```python
lexer = Lexer(source_code)
tokens = lexer.tokenize()
```

### 2. **Syntax Analysis** (`parser.py`)
Parses tokens into an Abstract Syntax Tree (AST).

**AST Node Types:**
- `Program`: Root node containing statements
- `VarDecl`: Variable declaration statement
- `Print`: Print statement
- `BinaryOp`: Binary operation expression
- `VarRef`: Variable reference
- `Number`: Integer literal

**Example:**
```python
parser = Parser(tokens)
ast = parser.parse_program()
```

### 3. **Semantic Analysis** (`symbol_table.py`)
Validates the program and builds a symbol table.

**Features:**
- Variable declaration tracking
- Scope management
- Memory slot allocation
- Undefined variable detection
- Duplicate declaration prevention

**Example:**
```python
analyzer = SemanticAnalyzer()
analyzer.visit(ast)
symbol_table = analyzer.table
```

### 4. **IR Generation** (`ir/builder.py`)
Transforms the AST into a linear intermediate representation.

**IR Instructions:**
- `ConstIRInstruction`: Load constant into temporary
- `LoadIRInstruction`: Load variable from memory slot
- `StoreIRInstruction`: Store temporary to memory slot
- `BinOpIRInstruction`: Binary operation
- `PrintIRInstruction`: Print value

**Example:**
```python
builder = IRBuilder(symbol_table=symbol_table)
ir_program = builder.build_program(ast)
```

## 💻 Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses Python standard library)

### Setup
```bash
# Clone the repository
git clone git@github.com:tikh-iv/leg-16-compiler.git
cd leg-16-compiler

# Run the compiler
python main.py
```

## 📖 Usage

### Basic Usage

Edit `main.py` to include your source code:

```python
from lexer import Lexer
from parser import Parser
from symbol_table import SemanticAnalyzer
from ir.builder import IRBuilder

# Your source code
code = """
var a = 10;
var b = 20;
var c = a + b;
print c
"""

# Compilation pipeline
lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse_program()

analyzer = SemanticAnalyzer()
analyzer.visit(ast)

builder = IRBuilder(symbol_table=analyzer.table)
ir_program = builder.build_program(ast)

# View the results
print(ir_program)
```

### Logging

The compiler uses Python's logging module for detailed debugging. Configure logging level in `main.py`:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change to INFO, WARNING, or ERROR
    format='%(levelname)s:%(name)s:%(message)s'
)
```

## 📝 Example

### Source Code
```
var a = 10;
var b = 16;
var c = a % b;
print c
var aaa = b;
var ccc = 777;
var bbb = aaa % ccc;
```

### Compilation Output

**Tokens:**
```
VAR      | var
IDENT    | a
ASSIGN   | =
NUMBER   | 10
SEMI     | ;
...
```

**AST:**
```
Program([
    VarDecl(a, Number(10)),
    VarDecl(b, Number(16)),
    VarDecl(c, BinaryOp(VarRef(a), %, VarRef(b))),
    Print(VarRef(c)),
    ...
])
```

**Symbol Table:**
```
{
    'a': Symbol(name='a', slot=0),
    'b': Symbol(name='b', slot=1),
    'c': Symbol(name='c', slot=2),
    ...
}
```

**IR Instructions:**
```
ConstIRInstruction(src=Const(10), dst=t0)
StoreIRInstruction(src=t0, dst=Slot[0](a))
ConstIRInstruction(src=Const(16), dst=t1)
StoreIRInstruction(src=t1, dst=Slot[1](b))
LoadIRInstruction(dst=t2, src=Slot[0](a))
LoadIRInstruction(dst=t3, src=Slot[1](b))
BinOpIRInstruction(left=t2, op=%, right=t3, dst=t4)
StoreIRInstruction(src=t4, dst=Slot[2](c))
LoadIRInstruction(dst=t5, src=Slot[2](c))
PrintIRInstruction(value=t5)
...
```

## 🏗️ Architecture Details

### LEG-16 ISA

The target architecture is a 16-bit processor with the following characteristics:

#### Registers
- **R0-R5**: General-purpose registers
- **MAR**: Memory Address Register
- **IO**: I/O Register

#### Instruction Types
- **CALC_REG**: Register-based calculations
- **CALC_IMM**: Immediate value calculations
- **MEM_LOAD**: Memory load operations
- **MEM_STOR**: Memory store operations
- **BRANCH**: Conditional and unconditional branches
- **CALL_RET**: Function call and return

#### ALU Operations
Addition, Subtraction, AND, OR, NOT, XOR, Shifts (SHL/SHR), Multiplication, Division, Rotation (ROL/ROR), and more.

#### Memory Operations
- **PUSH**: Push to stack
- **POP**: Pop from stack
- **STOR**: Store to memory
- **LOAD**: Load from memory

## 🛠️ Development

### Adding New Features

1. **Add a new operator**: Update `lexer.py`, `parser.py`, and `ir/builder.py`
2. **Add a new statement type**: Update `ast_leg.py`, `parser.py`, `symbol_table.py`, and `ir/builder.py`
3. **Extend IR**: Add new instruction types in `ir/instructions.py`

### Running Tests

Currently, the project uses example code in `main.py` for testing. To test different programs:

```python
code = """
// Your test code here
var x = 42;
print x
"""
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more operators (multiplication, division, comparison)
- [ ] Implement control flow (if/else, while loops)
- [ ] Add function definitions and calls
- [ ] Implement code generation from IR to LEG-16 assembly
- [ ] Add type system
- [ ] Write comprehensive test suite
- [ ] Add error recovery in parser
- [ ] Implement optimization passes

## 📄 License

This project is an educational compiler implementation. Check the repository for license details.

## 👤 Author

Ivan Tikhonov ([@tikh-iv](https://github.com/tikh-iv))

---

**Note**: This compiler is currently in the IR generation phase. The next step would be to implement the backend code generator that translates IR instructions to LEG-16 assembly code.
