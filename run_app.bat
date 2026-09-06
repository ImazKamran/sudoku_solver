@echo off
echo ====================================================================
echo             AI-Powered Sudoku Solver ^& Generator Launcher
echo ====================================================================
echo.
echo [1/2] Verifying and installing dependencies...
pip install -r requirements.txt
echo.
echo [2/2] Starting the Streamlit Web GUI...
echo.
if exist app.py (
    streamlit run app.py
) else if exist sudoku_solver\app.py (
    streamlit run sudoku_solver\app.py
) else (
    echo [ERROR] app.py was not found!
)
pause
