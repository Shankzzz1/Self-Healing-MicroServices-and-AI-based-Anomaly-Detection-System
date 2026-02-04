import subprocess
import time

def restart_service(service_name: str):
    print(f"🔁 Restarting service: {service_name}")

    subprocess.run(
        ["docker", "restart", service_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(5)
    print(f"✅ {service_name} restarted successfully")
