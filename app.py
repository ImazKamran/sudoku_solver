import streamlit as st
import time
import copy
from solver import SudokuSolver

st.set_page_config(
    page_title="AI Sudoku Solver & Generator",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Styling headings and cards */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .stButton>button {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,123,255,0.15);
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,123,255,0.25);
    }

    /* Text inputs styled like Sudoku cells */
    .stTextInput input {
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        height: 48px;
        border-radius: 6px !important;
        border: 2px solid #ddd !important;
        background-color: #fafafa;
        color: #111;
        transition: all 0.15s ease-in-out;
    }
    .stTextInput input:focus {
        border-color: #007bff !important;
        background-color: #fff;
        box-shadow: 0 0 8px rgba(0,123,255,0.25) !important;
    }

    /* Hide label padding */
    .stTextInput label {
        display: none !important;
    }

    /* Highlight containers */
    .info-card {
        background-color: var(--secondary-background-color, #f8f9fa);
        color: var(--text-color, #212529);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin-bottom: 15px;
    }
    .info-card h4 {
        color: var(--text-color, #212529);
        margin-top: 0;
        margin-bottom: 8px;
    }
    .info-card p, .info-card li {
        color: var(--text-color, #212529);
        margin-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)

if "board" not in st.session_state:
    st.session_state.board = [[0]*9 for _ in range(9)]
if "initial_board" not in st.session_state:
    st.session_state.initial_board = [[0]*9 for _ in range(9)]
if "solved_flag" not in st.session_state:
    st.session_state.solved_flag = False
if "solve_acknowledged" not in st.session_state:
    st.session_state.solve_acknowledged = False
if "solve_message" not in st.session_state:
    st.session_state.solve_message = None
if "hint_error" not in st.session_state:
    st.session_state.hint_error = None

def sync_board_to_widgets(board):
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            st.session_state[f"grid_input_{r}_{c}"] = str(val) if val != 0 else ""

for r in range(9):
    for c in range(9):
        key = f"grid_input_{r}_{c}"
        if key not in st.session_state:
            val = st.session_state.board[r][c]
            st.session_state[key] = str(val) if val != 0 else ""


def generate_puzzle_callback():
    solver = SudokuSolver()
    diff = st.session_state.difficulty_selection
    solver.generate_puzzle(diff)

    st.session_state.board = solver.get_board()
    st.session_state.initial_board = [row[:] for row in st.session_state.board]
    st.session_state.solved_flag = False
    st.session_state.solve_acknowledged = False
    st.session_state.solve_message = None
    sync_board_to_widgets(st.session_state.board)

def clear_grid_callback():
    empty_board = [[0]*9 for _ in range(9)]
    st.session_state.board = empty_board
    st.session_state.initial_board = empty_board
    st.session_state.solved_flag = False
    st.session_state.solve_acknowledged = False
    st.session_state.solve_message = None
    st.session_state.hint_error = None
    sync_board_to_widgets(empty_board)

def reset_initial_callback():
    st.session_state.board = [row[:] for row in st.session_state.initial_board]
    st.session_state.solved_flag = False
    st.session_state.solve_acknowledged = False
    st.session_state.solve_message = None
    st.session_state.hint_error = None
    sync_board_to_widgets(st.session_state.board)

def get_hint_callback():
    solver = SudokuSolver()
    solver.set_board(st.session_state.board)
    hint_pos, err_msg = solver.get_hint()
    if err_msg:
        st.session_state.hint_error = err_msg
    else:
        r, c, val = hint_pos
        st.session_state.board[r][c] = val
        st.session_state[f"grid_input_{r}_{c}"] = str(val)
        st.session_state.hint_error = None


def render_board_html(board, active_cell=None, highlight_type="assign", initial_board=None):
    html = """
    <style>
        .sudoku-table {
            border-collapse: collapse;
            margin: 15px auto;
            font-family: 'Outfit', sans-serif;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-radius: 10px;
            overflow: hidden;
        }
        .sudoku-cell {
            width: 44px;
            height: 44px;
            text-align: center;
            font-size: 22px;
            font-weight: 700;
            border: 1px solid #e0e0e0;
            transition: all 0.1s ease;
        }
        /* Thick borders for 3x3 subgrids */
        .sudoku-cell.border-right {
            border-right: 3px solid #333 !important;
        }
        .sudoku-cell.border-bottom {
            border-bottom: 3px solid #333 !important;
        }
        .sudoku-cell.border-left {
            border-left: 3px solid #333 !important;
        }
        .sudoku-cell.border-top {
            border-top: 3px solid #333 !important;
        }
        .empty-cell {
            color: transparent;
            background-color: #ffffff;
        }
        .given-cell {
            color: #111111;
            background-color: #f0f2f5;
        }
        .solved-cell {
            color: #0066cc;
            background-color: #e6f3ff;
            animation: fadeIn 0.3s;
        }
        .active-assign {
            background-color: #28a745 !important;
            color: white !important;
            transform: scale(1.05);
            z-index: 10;
        }
        .active-backtrack {
            background-color: #dc3545 !important;
            color: white !important;
            transform: scale(1.05);
            z-index: 10;
        }
        @keyframes fadeIn {
            from { opacity: 0.5; }
            to { opacity: 1.0; }
        }
    </style>
    <table class="sudoku-table">
    """
    for r in range(9):
        html += "<tr>"
        for c in range(9):
            val = board[r][c]
            classes = ["sudoku-cell"]

            if r == 0:
                classes.append("border-top")
            elif r % 3 == 2:
                classes.append("border-bottom")

            if c == 0:
                classes.append("border-left")
            elif c % 3 == 2:
                classes.append("border-right")

            if active_cell and active_cell == (r, c):
                if highlight_type == "assign":
                    classes.append("active-assign")
                else:
                    classes.append("active-backtrack")

            if val == 0:
                html += f'<td class="{" ".join(classes)} empty-cell">.</td>'
            else:
                if initial_board and initial_board[r][c] != 0:
                    classes.append("given-cell")
                else:
                    classes.append("solved-cell")
                html += f'<td class="{" ".join(classes)}">{val}</td>'
        html += "</tr>"
    html += "</table>"
    return html

def make_visualizer_callback(placeholder, initial_board, speed_ms):
    def callback(board, row, col, val, action):
        html = render_board_html(board, active_cell=(row, col), highlight_type=action, initial_board=initial_board)
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(speed_ms / 1000.0)
    return callback

st.markdown("""
<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px; text-align: center; color: white;">
    <h1 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 32px; font-weight: 700;">🧠 AI Sudoku Solver & Generator</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 16px;">Low-Level Constraint Satisfaction Engine with Visual Backtracking</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### ⚙️ AI Engine Settings")
algo = st.sidebar.selectbox(
    "Select Solving Heuristic",
    ["Heuristic (MRV)", "Standard Backtracking (Sequential)"],
    key="algo_selection",
    help="MRV (Minimum Remaining Values) solves puzzles much faster by focusing on the cell with the fewest possible choices first."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎮 Puzzle Generator")
difficulty = st.sidebar.selectbox("Choose Difficulty", ["Easy", "Medium", "Hard"], key="difficulty_selection")
st.sidebar.button("Generate Random Puzzle", on_click=generate_puzzle_callback)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⏱️ Visualizer Settings")
speed_mode = st.sidebar.radio(
    "Solving Method",
    ["Fast Solve (Instant)", "Step-by-step Animation"]
)
anim_speed = 50
if speed_mode == "Step-by-step Animation":
    anim_speed = st.sidebar.slider("Step Speed (ms)", 5, 200, 40, step=5)

tab1, tab2 = st.tabs(["🎮 Play & Solve", "📚 How it Works"])

with tab1:
    if st.session_state.solved_flag:
        st.markdown("### 🎉 Sudoku Solved Successfully!")
        if not st.session_state.solve_acknowledged:
            st.balloons()
            st.toast("Sudoku solved successfully! 🎉", icon="✅")
            st.session_state.solve_acknowledged = True
        if st.session_state.solve_message:
            st.success(st.session_state.solve_message)

        st.markdown(render_board_html(st.session_state.board, initial_board=st.session_state.initial_board), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        act_col1, act_col2 = st.columns(2)
        with act_col1:
            st.button("🧹 Clear Grid & Play Again", on_click=clear_grid_callback)
        with act_col2:
            st.button("🔄 Reset Initial Puzzle", on_click=reset_initial_callback)

    else:
        st.markdown("##### Complete or edit the grid below. Fill digits 1-9 (leave blank for empty cells).")

        for r in range(9):
            if r == 3 or r == 6:
                st.markdown('<div style="height: 6px;"></div>', unsafe_allow_html=True)

            cols = st.columns(9)
            for c in range(9):
                cols[c].text_input(
                    f"r{r}c{c}",
                    key=f"grid_input_{r}_{c}",
                    label_visibility="collapsed"
                )

                val_str = st.session_state[f"grid_input_{r}_{c}"]
                if val_str.isdigit() and 1 <= int(val_str) <= 9:
                    st.session_state.board[r][c] = int(val_str)
                else:
                    st.session_state.board[r][c] = 0

        invalid_cells = []
        solver = SudokuSolver()
        solver.set_board(st.session_state.board)
        for r in range(9):
            for c in range(9):
                val = st.session_state.board[r][c]
                if val != 0:
                    solver.board[r][c] = 0
                    if not solver.is_valid(val, (r, c)):
                        invalid_cells.append((r, c))
                    solver.board[r][c] = val

        if invalid_cells:
            css_rules = []
            for r, c in invalid_cells:
                css_rules.append(f"""
                .st-key-grid_input_{r}_{c} input {{
                    border-color: #dc3545 !important;
                    background-color: #fce8e6 !important;
                    color: #dc3545 !important;
                }}
                """)
            st.markdown(f"<style>{''.join(css_rules)}</style>", unsafe_allow_html=True)

        if not st.session_state.solved_flag:
            board_is_full = all(cell != 0 for row in st.session_state.board for cell in row)
            if board_is_full:
                solver = SudokuSolver()
                solver.set_board(st.session_state.board)
                if solver.is_board_valid():
                    st.session_state.solved_flag = True
                    st.session_state.solve_message = "Congratulations! You successfully solved the Sudoku puzzle yourself! 🏆"
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        act_col1, act_col2, act_col3, act_col4 = st.columns(4)

        with act_col1:
            if st.button("🚀 Solve Now"):
                solver = SudokuSolver()
                solver.set_board(st.session_state.board)
                if not solver.is_board_valid():
                    st.error("Invalid Board: Conflicting digits present in rows, columns, or 3x3 grids.")
                else:
                    st.session_state.initial_board = [row[:] for row in st.session_state.board]
                    st.session_state.solve_acknowledged = False

                    if speed_mode == "Step-by-step Animation":
                        st.info("Animating backtrack search in real time...")
                        visual_placeholder = st.empty()

                        start_time = time.time()
                        callback = make_visualizer_callback(visual_placeholder, st.session_state.initial_board, anim_speed)
                        solved = solver.solve(use_mrv=(algo == "Heuristic (MRV)"), callback=callback)
                        end_time = time.time()

                        if solved:
                            st.session_state.board = solver.get_board()
                            st.session_state.solved_flag = True
                            st.session_state.solve_message = f"Solved in {end_time - start_time:.4f}s | Search Steps: {solver.steps}"
                            st.rerun()
                        else:
                            st.error("No solution exists for this Sudoku.")
                    else:
                        start_time = time.time()
                        solved = solver.solve(use_mrv=(algo == "Heuristic (MRV)"))
                        end_time = time.time()

                        if solved:
                            st.session_state.board = solver.get_board()
                            st.session_state.solved_flag = True
                            st.session_state.solve_message = f"Solved in {end_time - start_time:.4f}s | Search Steps: {solver.steps}"
                            st.rerun()
                        else:
                            st.error("No solution exists for this Sudoku.")

        with act_col2:
            st.button("💡 Get Hint", on_click=get_hint_callback)
            if st.session_state.hint_error:
                st.warning(st.session_state.hint_error)
                st.session_state.hint_error = None

        with act_col3:
            st.button("🧹 Clear Grid", on_click=clear_grid_callback)

        with act_col4:
            st.button("🔄 Reset Initial", on_click=reset_initial_callback)

with tab2:
    st.markdown("### 📚 How It Works: Heuristics & Backtracking")
    st.write("This application demonstrates essential Artificial Intelligence concepts in a beginner-friendly way. Here is an explanation of the core algorithms:")

    st.markdown("""
    <div class="info-card">
        <h4>1. Backtracking Search (Depth-First Search)</h4>
        <p>The solver fills in empty cells recursively. When it places a digit, it checks if the board remains valid according to Sudoku rules. If it hits a dead end (no valid digits can be placed in a cell), it retreats (backtracks) by wiping the cell and tries the next number in the previous cell.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h4>2. MRV Heuristic (Minimum Remaining Values)</h4>
        <p>In standard backtracking, the solver scans cells sequentially (row-by-row). With the <b>MRV Heuristic</b>, the solver evaluates which empty cell has the <i>fewest possible remaining choices</i> (1-9) and solves that cell first. This reduces backtracking steps dramatically, solving hard boards in milliseconds instead of seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h4>3. Real-Time Search Animation</h4>
        <p>The step-by-step solver visualizes how backtracking searches for the solution:</p>
        <ul>
            <li><span style="color: #28a745; font-weight: bold;">Green cells</span> show the algorithm making a new number assignment.</li>
            <li><span style="color: #dc3545; font-weight: bold;">Red cells</span> show the algorithm hitting a conflict, erasing its path, and backtracking.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
