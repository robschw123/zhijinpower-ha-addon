import requests
import os
import traceback

HEADERS = {
    "platform": "App",
    "langtype": "en",
    "token": os.getenv("TOKEN"),
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) Html5Plus/1.0 uni-app"
}

print(f"[DEBUG] Headers: {HEADERS}")

def get_mach_info(machine_id: str) -> dict:
    url = f"http://app.gz529.com/index.php/api/Machine/getMachInfo?id={machine_id}"
    try:
        resp = requests.get(url, headers=HEADERS, params={"id": machine_id}, timeout=10)
        resp.raise_for_status()
        return resp.json()["data"]["info"]["property_data"]
    except Exception as e:
        print("[ERROR] Exception in get_mach_info:")
        traceback.print_exc()     # gesamter Trace
        return {}
