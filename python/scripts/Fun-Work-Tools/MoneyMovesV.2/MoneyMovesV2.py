import customtkinter as ctk
from datetime import datetime

# Config
HOURLY_RATE = 26.00
WORK_START  = (8, 0)
WORK_END    = (16, 30)
WORK_DAYS   = [0, 1, 2, 3, 4]

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Logic
def get_work_bounds(now):
    start = now.replace(hour=WORK_START[0], minute=WORK_START[1], second=0, microsecond=0)
    end   = now.replace(hour=WORK_END[0],   minute=WORK_END[1],   second=0, microsecond=0)
    return start, end

def get_time_remaining(now):
    _, end = get_work_bounds(now)
    if now >= end:
        return "00:00:00"
    remaining     = end - now
    total_seconds = int(remaining.total_seconds())
    h, r          = divmod(total_seconds, 3600)
    m, s          = divmod(r, 60)
    return f"{h:02}:{m:02}:{s:02}"

def get_money_earned(now):
    start, end = get_work_bounds(now)
    if now < start:
        return 0.0
    elapsed = min(now, end) - start
    return (elapsed.total_seconds() / 3600) * HOURLY_RATE

def get_week_earnings(now):
    weekday        = now.weekday()
    start, end     = get_work_bounds(now)
    day_seconds    = (end - start).total_seconds()
    completed_days = sum(1 for d in WORK_DAYS if d < weekday)
    seconds_done   = completed_days * day_seconds
    if weekday in WORK_DAYS:
        if now >= end:
            seconds_done += day_seconds
        elif now > start:
            seconds_done += (now - start).total_seconds()
    return (seconds_done / 3600) * HOURLY_RATE

def get_day_percent(now):
    start, end = get_work_bounds(now)
    total      = (end - start).total_seconds()
    if now <= start: return 0.0
    if now >= end:   return 100.0
    return ((now - start).total_seconds() / total) * 100

def get_week_percent(now):
    weekday            = now.weekday()
    start, end         = get_work_bounds(now)
    day_seconds        = (end - start).total_seconds()
    total_work_seconds = len(WORK_DAYS) * day_seconds
    completed_days     = sum(1 for d in WORK_DAYS if d < weekday)
    seconds_done       = completed_days * day_seconds
    if weekday in WORK_DAYS:
        if now >= end:
            seconds_done += day_seconds
        elif now > start:
            seconds_done += (now - start).total_seconds()
    return min((seconds_done / total_work_seconds) * 100, 100.0)

# App
class MoneyMovesApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Money Moves V.2")
        self.geometry("420x480")  # ← bumped height
        self.resizable(False, False)

        # Title
        ctk.CTkLabel(
            self, text="💰 Money Moves",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(24, 4))

        # Clock card
        clock_frame = self._make_card()
        self.clock_label = self._make_value_label(clock_frame, "--:--:-- --")
        self.clock_label.pack()
        self.remaining_label = ctk.CTkLabel(
            clock_frame, text="Remaining: --:--:--",
            font=ctk.CTkFont(size=13), text_color="gray70"
        )
        self.remaining_label.pack(pady=(2, 0))

        # Earnings card
        earn_frame = self._make_card()
        self._make_section_label(earn_frame, "EARNINGS").pack(anchor="center")  # ← centered
        row1 = ctk.CTkFrame(earn_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(6, 0))
        ctk.CTkLabel(row1, text="Today", font=ctk.CTkFont(size=13), text_color="gray70").pack(side="left")
        self.today_earn_label = self._make_value_label(row1, "$0.00", size=15)
        self.today_earn_label.pack(side="right")
        row2 = ctk.CTkFrame(earn_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(4, 0))
        ctk.CTkLabel(row2, text="This Week", font=ctk.CTkFont(size=13), text_color="gray70").pack(side="left")
        self.week_earn_label = self._make_value_label(row2, "$0.00", size=15)
        self.week_earn_label.pack(side="right")

        # Progress card
        prog_frame = self._make_card()
        self._make_section_label(prog_frame, "PROGRESS").pack(anchor="center")  # ← centered

        self._make_section_label(prog_frame, "Day", small=True).pack(anchor="center", pady=(8, 2))   # ← centered
        self.day_bar = self._make_bar(prog_frame)
        self.day_pct_label = self._make_pct_label(prog_frame)

        self._make_section_label(prog_frame, "Week", small=True).pack(anchor="center", pady=(10, 2)) # ← centered
        self.week_bar = self._make_bar(prog_frame)
        self.week_pct_label = self._make_pct_label(prog_frame)

        self._tick()

    # Helpers
    def _make_card(self):
        frame = ctk.CTkFrame(self, corner_radius=12)
        frame.pack(fill="x", padx=24, pady=6)
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=12)  # ← fill="both" + expand
        return inner

    def _make_value_label(self, parent, text, size=20):
        return ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=size, weight="bold")
        )

    def _make_section_label(self, parent, text, small=False):
        return ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=10 if small else 11, weight="bold"),
            text_color="gray50" if small else "gray60"
        )

    def _make_bar(self, parent):
        bar = ctk.CTkProgressBar(parent, height=14, corner_radius=6)
        bar.set(0)
        bar.pack(fill="x")
        return bar

    def _make_pct_label(self, parent):
        lbl = ctk.CTkLabel(parent, text="0%", font=ctk.CTkFont(size=11), text_color="gray60")
        lbl.pack(anchor="e")
        return lbl

    # Tick
    def _tick(self):
        now      = datetime.now()
        day_pct  = get_day_percent(now)
        week_pct = get_week_percent(now)

        self.clock_label.configure(text=now.strftime("%I:%M:%S %p"))
        self.remaining_label.configure(text=f"Remaining: {get_time_remaining(now)}")
        self.today_earn_label.configure(text=f"${get_money_earned(now):,.2f}")
        self.week_earn_label.configure(text=f"${get_week_earnings(now):,.2f}")
        self.day_bar.set(day_pct / 100)
        self.week_bar.set(week_pct / 100)
        self.day_pct_label.configure(text=f"{day_pct:.1f}%")
        self.week_pct_label.configure(text=f"{week_pct:.1f}%")

        self.after(1000, self._tick)

if __name__ == "__main__":
    app = MoneyMovesApp()
    app.mainloop()
