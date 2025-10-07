import os, time, json, threading, requests
from datetime import datetime
from flask import Flask, jsonify


ENDPOINT_URL = os.getenv("ENDPOINT_URL", "https://webhook.site/5ba64671-cd25-49df-8cc7-6af1ecd681dc")
INTERVAL_SECONDS = float(os.getenv("INTERVAL_SECONDS", "10"))
PORT = int(os.getenv("PORT", "8000"))  


state = {
    "endpoint": ENDPOINT_URL,
    "interval_seconds": INTERVAL_SECONDS,
    "last_post_status": None,   
    "last_post_at": None,       
    "last_error": None
}

app = Flask(__name__)

def send_loop():
    while True:
        try:
            payload = {
                "message": "Tarea completada",
                "sent_at": datetime.now().isoformat() + "Z"
            }
            r = requests.post(ENDPOINT_URL, json=payload, timeout=10)
            state["last_post_status"] = r.status_code
            state["last_post_at"] = datetime.now().isoformat() + "Z"
            state["last_error"] = None
            print(f"[{datetime.now()}] POST {ENDPOINT_URL} -> {r.status_code} | {json.dumps(payload)}")
        except Exception as e:
            state["last_error"] = str(e)
            state["last_post_at"] = datetime.now().isoformat() + "Z"
            print(f"[{datetime.now()}] ERROR: {e}")
        time.sleep(INTERVAL_SECONDS)


worker = threading.Thread(target=send_loop, daemon=True)
worker.start()

@app.get("/")
def status():
    return jsonify({
        "running": True,
        **state
    })

if __name__ == "__main__":
    
    print(f"Iniciando Flask en puerto 8000. Enviando a https://webhook.site/5ba64671-cd25-49df-8cc7-6af1ecd681dc cada 10s")
    app.run(host="0.0.0.0", port=PORT)



