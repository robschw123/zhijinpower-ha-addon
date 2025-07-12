import requests
import traceback

def get_mach_info(token: str, machine_id: str) -> dict:
    HEADERS = {
        "platform": "App",
        "langtype": "en",
        "token": token,
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) Html5Plus/1.0 uni-app"
    }    
    print(f"[DEBUG] Headers: {HEADERS}")
    url = f"http://app.gz529.com/index.php/api/Machine/getMachInfo?id={machine_id}"
    try:
        resp = requests.get(url, headers=HEADERS, params={"id": machine_id}, timeout=10)
        resp.raise_for_status()
        return resp.json()["data"]["info"]["property_data"]
    except Exception as e:
        print("[ERROR] Exception in get_mach_info:")
        traceback.print_exc()     # gesamter Trace
        return {}
