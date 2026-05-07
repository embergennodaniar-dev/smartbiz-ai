"""
SmartBiz AI — EXE Launcher
Ikki marta bosing → server yoqiladi → brauzer ochiladi
"""
import sys, os, time, threading, webbrowser, subprocess, signal
import tkinter as tk
from tkinter import ttk, messagebox

# ── Paths ────────────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    # PyInstaller EXE ichida
    BASE_DIR = sys._MEIPASS
    APP_DIR  = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR  = BASE_DIR

BACKEND_DIR = os.path.join(BASE_DIR, "backend")
DB_PATH     = os.path.join(BACKEND_DIR, "models", "smartbiz.db")
PORT        = 8000
URL         = f"http://localhost:{PORT}"

sys.path.insert(0, BACKEND_DIR)

server_process = None


# ── DB init ─────────────────────────────────────────────────
def ensure_db():
    try:
        os.chdir(BACKEND_DIR)
        from models.database import init_db
        init_db()
    except Exception as e:
        print(f"DB xato: {e}")


# ── Server ───────────────────────────────────────────────────
def start_server():
    global server_process
    os.chdir(BACKEND_DIR)
    env = os.environ.copy()
    env["PYTHONPATH"] = BACKEND_DIR
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--host", "0.0.0.0", "--port", str(PORT), "--log-level", "warning"],
        cwd=BACKEND_DIR, env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def wait_for_server(timeout=20) -> bool:
    import urllib.request, urllib.error
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(f"{URL}/health", timeout=1)
            return True
        except:
            time.sleep(0.4)
    return False


def stop_server():
    global server_process
    if server_process:
        server_process.terminate()
        try:
            server_process.wait(timeout=3)
        except:
            server_process.kill()


# ── GUI ──────────────────────────────────────────────────────
class LauncherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SmartBiz AI")
        self.root.geometry("420x280")
        self.root.resizable(False, False)
        self.root.configure(bg="#0d0d0d")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 420) // 2
        y = (self.root.winfo_screenheight() - 280) // 2
        self.root.geometry(f"+{x}+{y}")

        self._build_ui()

    def _build_ui(self):
        # Logo area
        logo_frame = tk.Frame(self.root, bg="#0d0d0d")
        logo_frame.pack(pady=(32, 0))

        tk.Label(logo_frame, text="◈", font=("Segoe UI", 32),
                 fg="#c9973a", bg="#0d0d0d").pack()
        tk.Label(logo_frame, text="SmartBiz AI",
                 font=("Segoe UI", 18, "bold"),
                 fg="#ffffff", bg="#0d0d0d").pack()
        tk.Label(logo_frame, text="Biznes boshqaruv tizimi",
                 font=("Segoe UI", 10),
                 fg="#767676", bg="#0d0d0d").pack()

        # Status
        self.status_var = tk.StringVar(value="Ishga tushirilmoqda...")
        self.status_lbl = tk.Label(self.root,
                                   textvariable=self.status_var,
                                   font=("Segoe UI", 10),
                                   fg="#767676", bg="#0d0d0d")
        self.status_lbl.pack(pady=(24, 6))

        # Progress bar
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Gold.Horizontal.TProgressbar",
                         troughcolor="#1a1a1a", background="#c9973a",
                         bordercolor="#0d0d0d", lightcolor="#c9973a", darkcolor="#a87828")
        self.progress = ttk.Progressbar(self.root, style="Gold.Horizontal.TProgressbar",
                                         length=300, mode="indeterminate")
        self.progress.pack(pady=4)
        self.progress.start(12)

        # Open button (initially hidden)
        self.open_btn = tk.Button(
            self.root, text="🌐  Brauzerde Ochish",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff", bg="#c9973a",
            activebackground="#a87828", activeforeground="#fff",
            relief="flat", cursor="hand2", padx=20, pady=8,
            command=self.open_browser
        )

        # Version
        tk.Label(self.root, text="v2.0 — AI Powered",
                 font=("Segoe UI", 8),
                 fg="#333333", bg="#0d0d0d").pack(side="bottom", pady=8)

    def set_status(self, msg: str, color: str = "#767676"):
        self.status_var.set(msg)
        self.status_lbl.configure(fg=color)

    def show_ready(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.set_status("✓ Tayyor! Sayt ishlamoqda", "#c9973a")
        self.open_btn.pack(pady=12)
        # Auto-open browser once
        self.root.after(800, self.open_browser)

    def show_error(self, msg: str):
        self.progress.stop()
        self.progress.pack_forget()
        self.set_status(f"✗ {msg}", "#e53e3e")

    def open_browser(self):
        webbrowser.open(URL)

    def launch(self):
        threading.Thread(target=self._launch_thread, daemon=True).start()

    def _launch_thread(self):
        try:
            self.root.after(0, lambda: self.set_status("Ma'lumotlar bazasi tayyorlanmoqda...", "#767676"))
            ensure_db()

            self.root.after(0, lambda: self.set_status("Server yoqilmoqda...", "#767676"))
            start_server()

            self.root.after(0, lambda: self.set_status("Tayyor bo'lishi kutilmoqda...", "#767676"))
            ok = wait_for_server(timeout=25)

            if ok:
                self.root.after(0, self.show_ready)
            else:
                self.root.after(0, lambda: self.show_error("Server ishga tushmadi"))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)[:60]))

    def on_close(self):
        stop_server()
        self.root.destroy()

    def run(self):
        self.launch()
        self.root.mainloop()


# ── Entry point ──────────────────────────────────────────────
if __name__ == "__main__":
    app = LauncherApp()
    app.run()
