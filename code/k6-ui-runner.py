import tkinter as tk
import subprocess
import threading
from tkinter import messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("K6 UI Runner")
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self, text="URL")
        self.url_label.grid(row=0, column=0)
        
        self.url_entry = tk.Entry(self)
        self.url_entry.grid(row=0, column=1)

        self.duration_label = tk.Label(self, text="Number of durations")
        self.duration_label.grid(row=1, column=0)

        self.duration_entry = tk.Entry(self)
        self.duration_entry.grid(row=1, column=1)

        self.generate_button = tk.Button(self, text="Generate Fields", command=self.generate_fields)
        self.generate_button.grid(row=2, column=0)

        self.run_button = tk.Button(self, text="RUN", fg="red", command=self.run_test)
        self.run_button.grid(row=2, column=1)

        self.field_frame = tk.Frame(self)
        self.field_frame.grid(row=3, column=0, columnspan=2)

        self.output_text = tk.Text(self)
        self.output_text.grid(row=4, column=0, columnspan=2)

    def generate_fields(self):
        for widget in self.field_frame.winfo_children():
            widget.destroy()

        try:
            num_durations = int(self.duration_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Number of durations should be an integer")
            return

        self.durations = []
        self.targets = []

        for i in range(num_durations):
            duration_label = tk.Label(self.field_frame, text=f"Duration {i+1} (s)")
            duration_label.grid(row=i, column=0)

            duration_entry = tk.Entry(self.field_frame)
            duration_entry.grid(row=i, column=1)
            self.durations.append(duration_entry)

            target_label = tk.Label(self.field_frame, text=f"Target {i+1}")
            target_label.grid(row=i, column=2)

            target_entry = tk.Entry(self.field_frame)
            target_entry.grid(row=i, column=3)
            self.targets.append(target_entry)

    def run_test(self):
        self.output_text.delete(1.0, tk.END)
        thread = threading.Thread(target=self.run_k6, daemon=True)
        thread.start()
        self.after(100, self.check_output)

    def run_k6(self):
        url = self.url_entry.get()
        durations = [entry.get() for entry in self.durations]
        targets = [entry.get() for entry in self.targets]

        stages = ','.join([f"{{ duration: '{duration}s', target: {target} }}" for duration, target in zip(durations, targets)])

        script = f"""
import http from 'k6/http';
import {{ check, sleep }} from 'k6';

export const options = {{
    stages: [
    {stages}
    ],
}};

export default function () {{
    const res = http.get('{url}');
    check(res, {{ 'status was 200': (r) => r.status == 200 }});
    sleep(1);
}}
"""
        with open('test.js', 'w') as file:
            file.write(script)

        self.process = subprocess.Popen(['k6', 'run', 'test.js'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    def check_output(self):
        output = self.process.stdout.readline()
        if output:
            self.output_text.insert(tk.END, output)

        if self.process.poll() is None:
            self.after(100, self.check_output)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
