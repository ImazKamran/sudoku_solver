# 🧠 AI-Powered Sudoku Solver & Generator

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Algorithm](https://img.shields.io/badge/AI%20Engine-CSP%20%2B%20MRV%20Backtracking-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

An intelligent, interactive Sudoku Solver and Procedural Puzzle Generator built in Python. The system formulates Sudoku as a **Constraint Satisfaction Problem (CSP)** and solves it using **Recursive Backtracking (Depth-First Search)** augmented by the **Minimum Remaining Values (MRV)** heuristic.

It provides a dual-interface delivery model:
1. **Interactive Web GUI (Streamlit)** with real-time backtrack animation, instant solving, live conflict validation, hints, and random puzzle generation.
2. **Terminal CLI** for lightweight, dependency-free command-line execution.

---

## 📑 Table of Contents

- [Key Features](#-key-features)
- [Algorithmic Architecture](#-algorithmic-architecture)
  - [1. Constraint Satisfaction Problem (CSP) Formulation](#1-constraint-satisfaction-problem-csp-formulation)
  - [2. Recursive Backtracking Search (DFS)](#2-recursive-backtracking-search-dfs)
  - [3. Minimum Remaining Values (MRV) Heuristic](#3-minimum-remaining-values-mrv-heuristic)
  - [4. Procedural Puzzle Generation](#4-procedural-puzzle-generation)
- [Project Structure](#-project-structure)
- [Installation & Requirements](#-installation--requirements)
- [How to Run](#-how-to-run)
  - [Streamlit Web Application](#1-streamlit-web-application)
  - [Terminal CLI](#2-terminal-cli)
- [Web Interface Highlights](#-web-interface-highlights)
- [Authors & Presentation](#-authors--presentation)

---

## ✨ Key Features

- **⚡ Blazing Fast Solving:** Solves complex, expert-grade 9x9 puzzles in milliseconds using heuristic search.
- **🎬 Real-Time Search Animation:** Watch the backtracking algorithm think in real time:
  - <span style="color: #28a745; font-weight: bold;">Green</span>: New candidate number assignment.
  - <span style="color: #dc3545; font-weight: bold;">Red</span>: Conflict hit; state backtracked/erased.
  - Configurable animation speed (5 ms to 200 ms per step).
- **🧩 Procedural Puzzle Generator:** Generates playable, symmetric puzzles across three difficulty tiers:
  - **Easy:** 35 cells cleared
  - **Medium:** 45 cells cleared
  - **Hard:** 55 cells cleared
- **💡 Intelligent Hint Engine:** Evaluates the board using MRV, isolates the most constrained cell, and reveals its correct assignment without spoiling the rest of the board.
- **🛡️ Live Conflict Validation:** As you type, rows, columns, and 3x3 sub-grids are checked concurrently, highlighting invalid cells with red warning borders.
- **🎮 Interactive Player Mode:** Solve puzzles yourself on the board; the app automatically validates completion and triggers celebration animations.
- **💻 Lightweight Terminal CLI:** Pure Python command-line interface with formatted ASCII grid output for headless or low-resource environments.

---

## 🔬 Algorithmic Architecture

### 1. Constraint Satisfaction Problem (CSP) Formulation

Sudoku is mathematically modeled as a CSP:
- **Variables:** 81 individual coordinates $X_{r, c}$ where $r, c \in \{0, \dots, 8\}$.
- **Domains:** For each empty cell, $D_{r, c} \subseteq \{1, 2, 3, 4, 5, 6, 7, 8, 9\}$.
- **Constraints:**
  - **Row Constraint:** All elements in row $r$ must be unique: $\text{AllDifferent}(X_{r, 0}, \dots, X_{r, 8})$.
  - **Column Constraint:** All elements in column $c$ must be unique: $\text{AllDifferent}(X_{0, c}, \dots, X_{8, c})$.
  - **Subgrid Constraint:** All elements in each $3 \times 3$ block must be unique: $\text{AllDifferent}(\{X_{r, c} \mid r \in B_r, c \in B_c\})$.

### 2. Recursive Backtracking Search (DFS)

The baseline engine uses a recursive depth-first search:
1. **Target Selection:** Scans the board for an unassigned coordinate $(r, c)$.
2. **Domain Permutation:** Sequentially tests values $v \in [1, 9]$.
3. **Validity Check:** Validates whether placing $v$ violates any row, column, or $3 \times 3$ block constraints.
4. **Recursive Step:** If valid, assigns $X_{r, c} \leftarrow v$ and recursively solves downstream cells.
5. **Backtrack:** If downstream branches encounter a contradiction, resets $X_{r, c} \leftarrow 0$ and tries the next candidate.

### 3. Minimum Remaining Values (MRV) Heuristic

Standard sequential backtracking searches cells in row-major order, which can cause significant thrashing on sparse, difficult boards. 

The **MRV Heuristic** ("Most Constrained Variable" principle) dynamically inspects all empty cells and chooses the cell with the fewest legal candidate choices:

$$\text{Cell}_{\text{MRV}} = \arg\min_{(r, c): X_{r, c} = 0} |\{v \in \{1 \dots 9\} \mid \text{is\_valid}(v, r, c)\}|$$

- **Early Failure Detection:** Surfaces conflicts near the root of the search tree instead of deep down branches.
- **Massive Pruning:** Reduces explored states by orders of magnitude, turning second-long searches into sub-10ms solutions.

### 4. Procedural Puzzle Generation

1. A complete valid Sudoku board is generated using randomized backtracking (`solve_randomized()`).
2. Digits are removed at random based on selected difficulty (35, 45, or 55 cells).
3. The resulting puzzle is displayed to the user for solving or interactive gameplay.

---

## 📂 Project Structure

```
sudoku_solver/
├── solver.py          # Core CSP engine: backtracking, MRV heuristic, generator, hints
├── app.py             # Streamlit web GUI, state management, animated visualizer
├── ui.py              # Terminal CLI user interface and formatted board renderer
├── main.py            # Entry point for terminal CLI execution
├── run_app.bat        # Windows 1-click launcher for Streamlit GUI
├── requirements.txt   # Python dependencies (Streamlit)
├── .gitignore         # Ignores bytecode, caches, documents, and environment files
└── README.md          # Comprehensive project documentation
```

---

## 🚀 Installation & Requirements

### Prerequisites
- **Python 3.8+** installed on your system.

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd sudoku_solver
   ```

2. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ How to Run

### 1. Streamlit Web Application

#### Option A: One-Click Launcher (Windows)
Double-click `run_app.bat` in the repository root.

#### Option B: Terminal Command
```bash
streamlit run app.py
```
*The web interface will automatically open in your browser at `http://localhost:8501`.*

### 2. Terminal CLI

To solve puzzles directly from your terminal:
```bash
python main.py
```
Follow the interactive prompts to enter each row as a string of 9 digits (use `0` for empty cells).

---

## 🎨 Web Interface Highlights

- **Custom Matrix Grid:** Implemented with tailored HTML/CSS table styling for high readability and thick $3 \times 3$ grid delineations.
- **Visual State Colors:**
  - **Light Gray:** Initial fixed puzzle digits.
  - **Soft Blue:** Solution digits filled by the solver.
  - **Soft Red:** Conflicting digits flagged by real-time validation.
  - **Green / Red Pulse:** Active cell assignment and backtracking during animated search.
- **Interactive Controls:**
  - **Solve Now:** Instant or animated solution.
  - **Get Hint:** Calculates the single most constrained cell and reveals its digit.
  - **Clear Grid:** Clears the board for manual entry.
  - **Reset Initial:** Restores the generated puzzle back to its starting state.

---

## 👥 Authors & Presentation

- **M. Imaz Kamran** (F2023266647)
- **M. Nafay** (F2023266392)

📊 **Presentation Slides:** [Google Slides Presentation](https://docs.google.com/presentation/d/1fu7lAw7n-d4EucPOG3sMehmYkgoAPcaXjDsZAmSiGJg/edit?usp=sharing)
