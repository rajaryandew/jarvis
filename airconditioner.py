import subprocess
from gtts.tts import json
from speak import speak, speak_async

ac_id = None
devices = json.loads(
    subprocess.run(
        ["smartthings", "devices", "--json"], capture_output=True, text=True
    ).stdout
)

for device in devices:
    if device["label"] == "Room air conditioner":
        ac_id = device["deviceId"]
print(ac_id)


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
        speak_async("Turning on the AC")
        subprocess.run(["smartthings","devices:commands", ac_id, 'switch:on'])
    elif action == "turn_off":
        speak_async("Turning off the AC")
        subprocess.run(["smartthings", "devices:commands", ac_id, "switch:off"])
    elif action.startswith("setTemp"):
        temp = action.split("_")[1]
        if (int(temp) < 16) or (int(temp) > 30):
            speak("Invalid temperature provided")
            return
        subprocess.run(["smartthings",'devices:commands', ac_id, f"thermostatCoolingSetpoint:setCoolingSetpoint({int(temp)})"])
        speak(f"Setting the temperature to {temp}")
