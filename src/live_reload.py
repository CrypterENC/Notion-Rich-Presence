import os
import sys
import time
import threading

def watch_files():
    """Monitor Python files for changes and restart if modified."""
    time.sleep(2)  # Delay to avoid detecting changes on startup
    files = [os.path.join(root, file) for root, dirs, files in os.walk('.') for file in files if file.endswith('.py')]
    last_mtimes = {f: os.stat(f).st_mtime for f in files if os.path.exists(f)}

    while True:
        time.sleep(1)
        for f in files:
            if os.path.exists(f):
                mtime = os.stat(f).st_mtime
                if mtime != last_mtimes.get(f, 0):
                    print("File changed, restarting...")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
        # Update mtimes
        last_mtimes = {f: os.stat(f).st_mtime for f in files if os.path.exists(f)}

def start_live_reload():
    """Start the live reload watcher in a daemon thread."""
    watcher_thread = threading.Thread(target=watch_files, daemon=True)
    watcher_thread.start()
