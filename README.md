# Rubik's Cube Timer

A feature-rich Rubik's Cube solving timer application built with Python and Tkinter. Track your solving times, view statistics, and monitor your progress with an interactive graph.

## Features

- Clean, modern interface with light and dark themes
- Real-time timer display
- Best time tracking
- Interactive solve time graph showing:
  - Individual solve times
  - Overall average
  - Rolling average of 5 solves (Ao5)
- Complete solve history with timestamps
- Ability to delete individual times or all times
- Theme toggle (Light/Dark mode)

## Requirements

- Python 3.x
- Required Python packages:
  - tkinter
  - matplotlib

## Installation

1. Ensure Python 3.x is installed on your system
2. Install required packages:
   ```bash
   pip install matplotlib
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## How to Use

1. **Starting/Stopping the Timer**
   - Press the SPACEBAR to start the timer
   - Press the SPACEBAR again to stop the timer
   - Your time will be automatically saved and displayed in the list

2. **Managing Times**
   - Select a time from the list and click "Delete Selected Time" to remove it
   - Use "Delete All Times" to clear your entire history
   - Times are automatically saved to `times.txt`

3. **Viewing Statistics**
   - Your best time is displayed prominently below the timer
   - The graph shows your progress over time
   - Blue line shows individual solve times
   - Green line shows overall average
   - Red dashed line shows rolling average of last 5 solves (Ao5)

4. **Customizing Appearance**
   - Click "Toggle Theme" to switch between light and dark modes
   - Theme preference is saved in `config.json`

## Files

- `main.py` - The main application file
- `times.txt` - Stores your solve times and timestamps
- `config.json` - Stores your theme preference

## Tips

- Keep the spacebar pressed until you're ready to start your solve
- Release the spacebar to start timing
- Press the spacebar once you've completed the solve to stop the timer
- The graph automatically updates to show your progress
- Use the scrollbar to view your complete solving history
