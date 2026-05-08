# Windows-to-Linux Performance Engine v4.0

The **Windows-to-Linux Performance Engine** is a specialized desktop utility designed to transform the behavior of a standard Windows operating system into a high-performance, "lean" environment similar to Linux. By stripping away background bloat and repairing deep system errors, it maximizes hardware speed for power users.

## 📌 Introduction
Modern Windows environments often suffer from "lag-generators"—background processes and services that consume high disk and CPU resources. This engine utilizes a hardcoded "Hit-list" to terminate non-essential software and deactivates telemetry-heavy services, while simultaneously running structural repairs on the core operating system image.

---

## 🛠 Tech Stack
*   **Primary Language:** Python 3.x
*   **Interface Library:** [Tkinter](https://docs.python.org/3/library/tkinter.html) (Standard GUI Tool)
*   **Resource Management:** [psutil](https://pypi.org/project/psutil/) (System and Process Utilities)
*   **Command Execution:** Subprocess (Direct communication with the Windows Command Line)
*   **Security & Elevation:** Ctypes (Admin Rights verification)
*   **Workflow Logic:** Multi-threading (Prevents the interface from freezing during heavy system tasks)

---

## ✨ Core Features
*   **Minimalist Mode:** Detects and kills non-essential background bloat such as OneDrive, Cortana, Teams, and Microsoft Edge web-viewers.
*   **Lag-Service Deactivation:** Automatically stops and disables resource-heavy services like Windows Search Indexing and SysMain (formerly Superfetch).
*   **System Integrity Guard:** Runs hardcoded `sfc /scannow` logic to detect and repair corrupted system files.
*   **Image Health Rebuilder:** Executes `DISM` commands to repair the hidden Windows component store using online resources.
*   **Cache & Temp Purge:** Flushes DNS network records and executes a recursive purge of the system Temporary directories.
*   **Automated Storage TRIM:** Performs drive-specific optimization (TRIM for SSDs or Defrag for HDDs) to maintain data read/write speeds.

---

## ⚙️ Installation Instructions

### 1. Requirements
Before running the application, ensure you have Python installed on your system.

### 2. Manual Dependency Setup
This tool requires one external module for monitoring the system process list. Open your Command Prompt (CMD) and type:
```bash
pip install psutil
```

### 3. Execution (Mandatory Step)
Because this engine modifies system services and hardware schedules, it must be granted **Administrator** permissions:
1.  Navigate to your folder.
2.  Right-click your script file (`main.py` or the built `.exe`).
3.  Select **"Run as Administrator"**.

---

## 🔄 Flow of the System

1.  **Elevation Check:** Upon launch, the tool verifies that it has administrative control via a Windows logic check.
2.  **Queue Initialization:** The task sequence is built into a "Worker Thread," allowing the interface to remain responsive while heavy logic runs in the background.
3.  **Process Strip-down:** The engine loops through all active software, terminating anything matching the "Bloat" list to clear RAM.
4.  **Service Modification:** Telemetry and tracking services are stopped immediately and marked as "Disabled" to prevent them from restarting on reboot.
5.  **Sequential Repairs:** The engine runs through a checklist of command-line tools, progressing through Network, Disk, and Structural File repairs.
6.  **Optimization Phase:** The final stage cleans the local update cache and re-bases the component store for a "Linux-Lean" storage footprint.

---

## 🛠 Troubleshooting

*   **Script Hangs on Task 5 or 6:** This is standard behavior. The `SFC` and `DISM` commands take several minutes to analyze deep system files; please allow the progress bar to finish.
*   **"Access Denied" in Console:** Ensure you ran the script as an **Administrator**. Windows security blocks non-elevated scripts from stopping system services.
*   **UI Does Not Appear:** Ensure the `psutil` library is correctly installed. Run `pip install psutil` again and check for any installation errors.
*   **Killed Apps Restarting:** Some applications (like Steam or Discord) may be set to auto-start in their internal settings. You must disable their "Launch on Startup" toggle within the app's specific menu.

---
*Created for High-Performance Windows Environments*
