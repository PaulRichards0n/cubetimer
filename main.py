import tkinter as tk
import time
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RubiksTimer:
    def __init__(self, master):
        self.master = master
        master.title("Rubik's Cube Timer")

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.times = []
        self.config = {}

        self.load_config()
        self.load_times()
        self.setup_ui()
        self.update_theme()

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"theme": "light"}

    def save_config(self):
        with open("config.json", "w") as f:
            json.dump(self.config, f)

    def load_times(self):
        try:
            with open("times.txt", "r") as f:
                for line in f:
                    time, timestamp = line.strip().split(",")
                    self.times.append((float(time), timestamp))
        except FileNotFoundError:
            pass

    def save_times(self):
        with open("times.txt", "w") as f:
            for time, timestamp in self.times:
                f.write(f"{time},{timestamp}\n")

    def setup_ui(self):
        self.timer_label = tk.Label(self.master, text="0.00", font=("Arial", 48))
        self.timer_label.pack(pady=20)

        self.best_time_label = tk.Label(self.master, text="Best Time: N/A", font=("Arial", 16))
        self.best_time_label.pack()

        self.times_listbox = tk.Listbox(self.master, width=50, height=10)
        self.times_listbox.pack(pady=10)

        # self.scrollbar = tk.Scrollbar(self.master)
        # self.times_listbox.config(yscrollcommand=self.scrollbar.set)
        # self.scrollbar.config(command=self.times_listbox.yview)
        # self.scrollbar.pack(side="right", fill="y")

        self.delete_selected_button = tk.Button(self.master, text="Delete Selected Time", command=self.delete_selected_time)
        self.delete_selected_button.pack()

        self.delete_all_button = tk.Button(self.master, text="Delete All Times", command=self.delete_all_times)
        self.delete_all_button.pack()

        self.theme_button = tk.Button(self.master, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        self.master.bind("<space>", self.toggle_timer)

        self.update_times_listbox()
        self.update_graph()

    def toggle_timer(self, event=None):
        if self.running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.running = True
        self.start_time = time.time()
        self.update_timer()

    def stop_timer(self):
        self.running = False
        self.elapsed_time = time.time() - self.start_time
        self.times.append((self.elapsed_time / 60, time.strftime("%Y-%m-%d %H:%M:%S")))
        self.save_times()
        self.update_times_listbox()
        self.update_graph()

    def update_timer(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = self.elapsed_time % 60
            self.timer_label.config(text="{:02d}:{:02.2f}".format(minutes, seconds))
            self.master.after(10, self.update_timer)
        else:
            minutes = int(self.elapsed_time // 60)
            seconds = self.elapsed_time % 60
            self.timer_label.config(text="{:02d}:{:02.2f}".format(minutes, seconds))

    def update_times_listbox(self):
        self.times_listbox.delete(0, tk.END)
        for time, timestamp in self.times:
            minutes = int(time // 1)
            seconds = (time % 1) * 60
            self.times_listbox.insert(tk.END, f"{minutes:02d}:{seconds:.2f} - {timestamp}")
        if self.times:
            best_time = min(t[0] for t in self.times)
            minutes = int(best_time // 1)
            seconds = (best_time % 1) * 60
            self.best_time_label.config(text=f"Best Time: {minutes:02d}:{seconds:.2f}")
        else:
            self.best_time_label.config(text="Best Time: N/A")

    def delete_selected_time(self):
        try:
            index = self.times_listbox.curselection()[0]
            del self.times[index]
            self.save_times()
            self.update_times_listbox()
            self.update_graph()
        except IndexError:
            pass

    def delete_all_times(self):
        self.times = []
        self.save_times()
        self.update_times_listbox()
        self.update_graph()

    def update_graph(self):
        self.ax.clear()
        if self.times:
            solve_times = [t[0] for t in self.times]
            self.ax.plot(solve_times, label="Solve Times", marker='o', linestyle='-')

            # Overall Average
            avg_time = sum(solve_times) / len(solve_times)
            self.ax.axhline(y=avg_time, color='green', linestyle='-', label=f"Average: {avg_time:.2f}")

            # Rolling Average of 5 (Ao5)
            if len(solve_times) >= 5:
                ao5 = [sum(solve_times[i:i+5]) / 5 for i in range(len(solve_times) - 4)]
                ao5_x = list(range(4, len(solve_times)))  # x values for Ao5
                self.ax.plot(ao5_x, ao5, color='red', linestyle='--', label="Ao5")

            self.ax.set_xlabel("Solve Number")
            self.ax.set_ylabel("Time (s)")
            self.ax.set_title("Solve Times Graph")
            self.ax.legend()
        else:
            self.ax.text(0.5, 0.5, "No solves yet", ha="center", va="center")
        self.canvas.draw()

    def toggle_theme(self):
        if self.config["theme"] == "light":
            self.config["theme"] = "dark"
        else:
            self.config["theme"] = "light"
        self.save_config()
        self.update_theme()

    def update_theme(self):
        bg_color = "white" if self.config["theme"] == "light" else "#333"
        fg_color = "black" if self.config["theme"] == "light" else "white"
        self.master.config(bg=bg_color)
        self.timer_label.config(bg=bg_color, fg=fg_color)
        self.best_time_label.config(bg=bg_color, fg=fg_color)
        self.times_listbox.config(bg=bg_color, fg=fg_color)
        self.delete_selected_button.config(bg=bg_color, fg=fg_color)
        self.delete_all_button.config(bg=bg_color, fg=fg_color)
        self.theme_button.config(bg=bg_color, fg=fg_color)
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)
        self.ax.tick_params(axis='x', colors=fg_color)
        self.ax.tick_params(axis='y', colors=fg_color)
        self.ax.title.set_color(fg_color)
        self.ax.xaxis.label.set_color(fg_color)
        self.ax.yaxis.label.set_color(fg_color)
        self.ax.legend(facecolor=bg_color, edgecolor=fg_color, labelcolor=fg_color)
        self.canvas.draw()

root = tk.Tk()
timer = RubiksTimer(root)
root.mainloop()