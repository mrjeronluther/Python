import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import subprocess
import threading
import os
import json
import time
import ctypes
import logging
import psutil  # You must: pip install psutil
from pathlib import Path
from queue import Queue, Empty
from dataclasses import dataclass

# --- CONFIG ---
THEME_BG = "#0d1117"
THEME_FG = "#58a6ff"
CONSOLE_BG = "#010409"

@dataclass
class Task:
    id: int
    name: str
    command: str = None
    func: callable = None  # For Python-native "Deep Cleaning"
    smart_heal: bool = False

class LinuxStyleOptimizer:
    """The Engine: Handles Linux-style stripping and Windows repairs."""
    
    # Processes that are 100% safe to kill to reduce lag
    BLOAT_PROCESSES = [
        "msedge.exe", "msedgewebview2.exe", "onedrive.exe", "cortana.exe",
        "teams.exe", "discord.exe", "spotify.exe", "skype.exe", 
        "microsoftedgeupdate.exe", "compattelrunner.exe", "powerpnt.exe"
    ]

    # Services that cause background disk/CPU lag
    LAGGY_SERVICES = [
        "SysMain",     # Previously Superfetch (Causes high disk usage on SSDs)
        "DiagTrack",   # Telemetry / Connected User Experiences
        "WSearch",     # Windows Search indexing (CPU heavy)
        "MapsBroker",  # Downloaded Maps Manager
        "XblAuthManager" # Xbox Live (If you don't game)
    ]

    def __init__(self, msg_queue):
        self.msg_queue = msg_queue
        self._stop_event = threading.Event()

    def log(self, text, type="INFO"):
        self.msg_queue.put(("OUTPUT", f"[{type}] {text}"))

    def kill_non_essentials(self):
        """Kills processes on the hit-list to mimic Linux minimalism."""
        self.log("Entering 'Minimalist Mode' - Terminating background bloat...", "STRIP")
        count = 0
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                if name in self.BLOAT_PROCESSES:
                    proc.kill()
                    count += 1
                    self.log(f"Killed: {name}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.log(f"Cleanup complete. Removed {count} background 'Lag-Generators'.")

    def stop_lag_services(self):
        """Disables Windows services that 'chat' in the background."""
        self.log("Disabling Telemetry & High-IO Services...", "STRIP")
        for service in self.LAGGY_SERVICES:
            # We use 'stop' to kill it now and 'config start= disabled' to keep it dead
            subprocess.run(f"net stop {service} /y", shell=True, capture_output=True)
            subprocess.run(f"sc config {service} start=disabled", shell=True, capture_output=True)
            self.log(f"Service Deactivated: {service}")

    def run_cmd(self, cmd):
        """Run system commands and stream to GUI."""
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in iter(process.stdout.readline, ""):
            if self._stop_event.is_set(): break
            if line.strip(): self.log(line.strip())
        process.wait()
        return process.returncode == 0

class EnterpriseApp(tk.Tk):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.title("Windows-to-Linux Performance Engine v4.0")
        self.geometry("850x650")
        self.configure(bg=THEME_BG)
        
        self.msg_queue = Queue()
        self.engine = LinuxStyleOptimizer(self.msg_queue)
        self._build_ui()
        self.after(100, self._process_queue)

    def _build_ui(self):
        tk.Label(self, text="MAINTENANCE TOOL", font=("Consolas", 14, "bold"), 
                 bg=THEME_BG, fg=THEME_FG).pack(pady=20)
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=700, mode="determinate")
        self.progress.pack(pady=10)

        self.console = scrolledtext.ScrolledText(self, width=100, height=22, bg=CONSOLE_BG, 
                                                 fg="#abb2bf", font=("Consolas", 9))
        self.console.pack(pady=10, padx=20)

        btn_frame = tk.Frame(self, bg=THEME_BG)
        btn_frame.pack(pady=20)

        self.btn_run = tk.Button(btn_frame, text="RUN DEBLOAT & REPAIR", command=self._start, 
                                bg="#238636", fg="white", width=25, font=("Segoe UI", 10, "bold"))
        self.btn_run.grid(row=0, column=0, padx=10)

    def _start(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showerror("Error", "You MUST run this as Administrator to stop system services.")
            return
        self.btn_run.config(state=tk.DISABLED)
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        total = len(self.tasks)
        for i, task in enumerate(self.tasks):
            self.msg_queue.put(("OUTPUT", f"\n>>> TASK {i+1}/{total}: {task.name}"))
            
            if task.func:
                task.func()
            elif task.command:
                self.engine.run_cmd(task.command)
            
            self.msg_queue.put(("PROGRESS", ((i+1)/total)*100))
        
        self.msg_queue.put(("DONE", None))

    def _process_queue(self):
        try:
            while True:
                msg_type, data = self.msg_queue.get_nowait()
                if msg_type == "OUTPUT":
                    self.console.insert(tk.END, data + "\n")
                    self.console.see(tk.END)
                elif msg_type == "PROGRESS":
                    self.progress["value"] = data
                elif msg_type == "DONE":
                    messagebox.showinfo("Complete", "Your system is now optimized and 'Linux-Lean'.")
                    self.btn_run.config(state=tk.NORMAL)
        except Empty:
            pass
        self.after(100, self._process_queue)

if __name__ == "__main__":
    # Create the specialized task engine
    # Initialize UI first to get engine reference
    q = Queue()
    e = LinuxStyleOptimizer(q)

    # DEFINE THE ENGINE TASKS (THE FULL WORKFLOW)
    system_tasks = [
        Task(0, "Process Strip-down", func=e.kill_non_essentials),
        Task(1, "Service Optimization", func=e.stop_lag_services),
        Task(2, "Flush Network DNS", "ipconfig /flushdns"),
        Task(3, "Deep Temp Purge", f'del /q /s /f "%TEMP%\\*"'),
        Task(4, "System Integrity (SFC)", "sfc /scannow"),
        Task(5, "Image Health (DISM)", "Dism /Online /Cleanup-Image /RestoreHealth"),
        Task(6, "Reset Update Cache", "net stop wuauserv & rd /s /q %systemroot%\\SoftwareDistribution & net start wuauserv"),
        Task(7, "Component Store Reset", "Dism /Online /Cleanup-Image /StartComponentCleanup /ResetBase"),
        Task(8, "TRIM/Defrag SSD/HDD", "defrag c: /o /u")
    ]

    app = EnterpriseApp(system_tasks)
    
    # DPI Scaling fix
    try: ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    
    app.mainloop()
