import customtkinter as ctk
import ctypes
from ctypes import wintypes

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dota2 - map reminder")
        self.root.geometry("400x70")
        self.root.attributes("-topmost", True)  # Always on top
        ctk.set_appearance_mode("dark")  # Dark mode
        ctk.set_default_color_theme("dark-blue")  # Optional theme

    def make_window_topmost(self):
        HWND_TOPMOST = -1
        SWP_NOACTIVATE = 0x0010
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001

        hwnd = ctypes.windll.user32.FindWindowW(None, self.root.title())
        if hwnd:
            ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                              SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)
        else:
            print("Failed to find window handle.")


        # Initial time values
        self.minutes = 0
        self.seconds = 0
        self.running = False

        # Label to display the time
        self.time_label = ctk.CTkLabel(root, text="00:00", font=('Arial', 28), text_color="white")
        self.time_label.grid(column=1, row=0, pady=5)

        # Start/Edit button
        self.start_button = ctk.CTkButton(root, text="Start", width=50, height=30, command=self.toggle_timer)
        self.start_button.grid(column=0, row=0, padx=10)

        # Edit inputs for minutes and seconds
        self.minute_entry = ctk.CTkEntry(root, width=30, font=('Arial', 14))
        self.second_entry = ctk.CTkEntry(root, width=30, font=('Arial', 14))
        self.minute_entry.insert(0, "0")
        self.second_entry.insert(0, "0")
        ctk.CTkLabel(root, text="Minutes:", font=('Arial', 12)).grid(row=0, column=2, padx=5)
        self.minute_entry.grid(row=0, column=3, padx=5)
        ctk.CTkLabel(root, text="Seconds:", font=('Arial', 12)).grid(row=0, column=4, padx=5)
        self.second_entry.grid(row=0, column=5, padx=5)

        self.minute_entry.configure(state="disabled")
        self.second_entry.configure(state="disabled")

        # Reminder label
        self.reminder_label = ctk.CTkLabel(root, text="", font=('Arial', 12), text_color="red")
        self.reminder_label.grid(row=0, column=2, padx=5)

    def toggle_timer(self):
        if not self.running:
            # Start timer
            self.running = True
            self.start_button.configure(text="Edit")
            self.update_timer()
        else:
            # Switch to edit mode
            self.running = False
            self.start_button.configure(text="Start")
            self.edit_mode()

    def edit_mode(self):
        self.minute_entry.configure(state="normal")
        self.second_entry.configure(state="normal")
        self.minute_entry.delete(0, ctk.END)
        self.second_entry.delete(0, ctk.END)
        self.minute_entry.insert(0, str(self.minutes))
        self.second_entry.insert(0, str(self.seconds))
        self.set_time_button = ctk.CTkButton(root, width=25, text="Set Time", command=self.set_time)
        self.set_time_button.grid(row=0, column=6)


    def set_time(self):
        # Update timer with user input
        try:
            self.minutes = int(self.minute_entry.get())
            self.seconds = int(self.second_entry.get())
            self.update_time_label()
            self.reminder_label.forget()
            self.toggle_timer()
        except ValueError:
            pass  # Ignore invalid input

    def update_timer(self):
        if self.running:
            self.seconds += 1
            if self.seconds >= 60:
                self.seconds = 0
                self.minutes += 1
            self.update_time_label()
            self.reminder_stacks()  # Call stack reminder logic
            self.root.after(1000, self.update_timer)

    def update_time_label(self):
        self.time_label.configure(text=f"{self.minutes:02}:{self.seconds:02}")

    def reminder_stacks(self):
        # Logic to check if seconds are between 40 and 51
        if 40 <= self.seconds <= 52:
            self.reminder_label.configure(text="Prepare to stack!")
        elif self.seconds == 53 or self.seconds == 54:
            self.reminder_label.configure(text="Stack now!")
        else:
            self.reminder_label.configure(text="")


# Initialize the application
root = ctk.CTk()
app = TimerApp(root)

# Call make_window_topmost after the window is created
root.after(100, app.make_window_topmost)  # Ensures the window stays on top

# Start the main event loop
root.mainloop()

