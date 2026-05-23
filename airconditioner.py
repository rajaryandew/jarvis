import httpx
import os
from speak import speak, speak_async

SMARTTHINGS_TOKEN = os.getenv("SMARTTHINGS_TOKEN")
headers = {"Authorization": f"Bearer {SMARTTHINGS_TOKEN}"}



try:
    devices = httpx.get(
        "https://api.smartthings.com/v1/devices", headers=headers
    ).json()
    ac_id = devices["items"][1]["deviceId"]
except:
    print("Failed to get the ac information")


def createbody(capability: str, command: str, arguments: str = ""):
    return {
        "commands": [
            {
                "component": "main",
                "capability": capability,
                "command": command,
                **({"arguments": [arguments]} if arguments else {}),
            }
        ]
    }


def airconditioneraction(response: str):
    action = response.split(" ")[1]
    if action == "turn_on":
        body = createbody(capability="switch", command="on")
        speak_async("Turning on the AC")
        httpx.post(
            f"https://api.smartthings.com/v1/devices/{ac_id}/commands",
            headers=headers,
            json=body,
        )
    elif action == "turn_off":
        body = createbody(capability="switch", command="off")
        speak_async("Turning off the AC")
        httpx.post(
            f"https://api.smartthings.com/v1/devices/{ac_id}/commands",
            headers=headers,
            json=body,
        )
    elif action.startswith("setTemp"):
        temp = action.split("_")[1]
        if (int(temp) < 16) or (int(temp) > 30):
            speak("Invalid temperature provided")
            return
        body = createbody(
            capability="thermostatCoolingSetpoint",
            command=f"setCoolingSetpoint",
            arguments=int(temp),
        )
        response = httpx.post(
            f"https://api.smartthings.com/v1/devices/{ac_id}/commands",
            headers=headers,
            json=body,
        )
        speak(f"Setting the temperature to {temp}")
