import os
import platform
import time

START_TIME = time.time()

def runtime_meta() -> dict:
    return {
        "env": os.getenv("APP_ENV", "dev"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "git_sha": os.getenv("GIT_SHA", "unknown"),
    }
