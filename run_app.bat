@echo off
echo ====================================================================
echo             AI-Powered Sudoku Solver ^& Generator Launcher
echo ====================================================================
echo.
echo [1/2] Verifying and installing Streamlit...
pip install streamlit
echo.
echo [2/2] Starting the Streamlit Web/Mobile GUI...
echo.
streamlit run sudoku_solver/app.py
pause
