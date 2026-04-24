# Money Moves

## Overview
This Python script displays a live terminal dashboard that tracks your earnings and time progress throughout the workday. It shows your current clock time, a countdown to the end of your shift, money earned today, money earned this week, and progress bars for both the day and week. The display updates every second in-place with no flickering using ANSI escape codes. No external libraries required.

<img width="687" height="159" alt="Screenshot 2026-04-24 105402" src="https://github.com/user-attachments/assets/63c04058-0ed8-4d1b-a9a3-0a3aa2429c7f" />

---

## Dependencies
No external packages needed — this script uses only Python built-ins:
- `time`
- `datetime`

---

## Usage

1. Open the script and update the configuration at the top to match your schedule:

```python
HOURLY_RATE = 26.00
WORK_START = (8, 0)    # 8:00 AM
WORK_END = (16, 30)    # 4:30 PM
WORK_DAYS = [0, 1, 2, 3, 4]  # Monday–Friday
```
2. Run the script:
  MoneyMoves.py

3. The dashboard will launch in your terminal and update live every second.

## Notes
- No external dependencies — runs on any machine with Python 3 installed.
- Works on Windows, Mac, and Linux.
- Earnings are calculated based on time elapsed within your defined work hours only.
- Progress bars show percentage of the day and week completed.
