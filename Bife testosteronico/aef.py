import requests
r = requests.get("https://api.openrouter.ai/")
print(r.status_code)
