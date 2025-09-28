# 🐄 Moo Language

**Moo** is a modern, AI-first programming language inspired by Python’s readability and optimized for machine learning, data science, and high-performance computation. Built from the ground up, Moo is designed to make AI development simple, fast, and intuitive.

---

## 🚀 Features

### Core Language Features

- **Python-like syntax** with indentation-based blocks
- **Immutable by default** with explicit `mut` keyword for mutable variables
- **Keyword-only arguments** in functions by default
- **Pattern matching** for clean control flow
- **First-class types**: integers, floats, decimals, strings, booleans, `None`
- **Advanced numeric types**: built-in support for precise decimals and rational numbers
- **Simplified truthiness rules**: only `false`, `0`, empty collections, and `None` are falsey

### Concurrency & Performance

- True multi-threading (no GIL)
- Built-in `async/await` for asynchronous programming
- Parallel collections and loops
- LLVM-backed compilation for JIT and AOT performance
- Gradual typing (dynamic and optional static types)

### AI-First Features

- **Tensors as first-class types** with slicing, broadcasting, and reshaping
- **Automatic differentiation** built into the language
- Unified numeric backend: CPU/GPU/TPU support
- Zero-copy tensor operations between CPU and GPU
- **DataFrames as a core type** with typed columns
- Streaming datasets with sharding and caching
- Native serialization: Parquet, Arrow, HDF5, JSONL
- Built-in training loops, loss functions, and optimizers
- Experiment tracking (`moolog`) and visualization tools (`mooplot`)
- Multi-GPU and distributed training support

### Developer Experience

- Readable, math-friendly syntax suitable for AI/ML
- Auto-reproducible experiments (seeds, deterministic algorithms)
- Strong tooling and ecosystem:

  - Formatter (`moofmt`)
  - Type checker (`mootype`)
  - Debugger and profiler integrated with LLVM
  - Package manager (`moopkg`) and virtual environment system

---

## 🔹 Example Syntax

### Variables

```moo
let x = 42
mut y = 3.14
let name: string = "Moo"
```

### Functions

```moo
fn add(a: int, b: int) -> int:
    return a + b

async fn fetch_data(url: string) -> string:
    let response = await http.get(url)
    return response.text
```

### Control Flow

```moo
if x > 10:
    print("big")
elif x == 10:
    print("equal")
else:
    print("small")
```

### Pattern Matching

```moo
match x:
    case 0:
        print("zero")
    case 1 | 2:
        print("one or two")
    case _:
        print("something else")
```

### Collections

```moo
let nums = [1, 2, 3, 4]
let user = { "id": 123, "name": "Alice" }

for n in nums:
    print(n)
```

### AI/Tensor Example

```moo
let a: tensor[2, 2] = [[1, 2], [3, 4]]
let b: tensor[2, 2] = [[5, 6], [7, 8]]

let c = a @ b         # matrix multiply
let d = a .* b        # element-wise multiply

fn forward(x: tensor, w: tensor, b: tensor) -> tensor:
    return (x @ w) + b

train(model, data, device="gpu", epochs=10)
```

---

## ⚙️ Getting Started

### Prerequisites

- Rust >= 1.70
- Cargo (Rust package manager)

### Setup

```bash
git clone https://github.com/yourusername/moo_lang.git
cd moo_lang
cargo build
cargo run
```

This will run a simple demo lexer on sample Moo code.

---

## 📂 Project Structure

```
moo_lang/
├── Cargo.toml          # Project metadata and dependencies
├── README.md           # This file
├── src/
│   ├── main.rs         # Entry point
│   └── lexer.rs        # Tokenizer module
└── target/             # Build artifacts
```

---

## 📝 Roadmap

1. **Phase 0 — Foundations**

   - Lexer and parser prototype
   - REPL and Hello World

2. **Phase 1 — Core Features**

   - Functions, pattern matching, control flow
   - Type system, standard library

3. **Phase 2 — Concurrency & Performance**

   - Async/await, multi-threading, LLVM JIT
   - Gradual typing

4. **Phase 3 — AI-First Core**

   - Tensors, automatic differentiation, unified numeric backend
   - DataFrames, streaming datasets, serialization

5. **Phase 4 — AI Developer Experience**

   - Training loops, optimizers, experiment logging, visualization
   - Multi-GPU / distributed support

6. **Phase 5 — Ecosystem**

   - Package manager, tooling, documentation
   - Open-source release v1.0

---

## 💡 Philosophy

- Readable, math-first syntax
- One obvious way to do it
- Built for AI and high-performance computing from day one
- Reproducibility and safety as core principles
- No “glue language” — everything is first-class in the runtime
