"""
Made by: @ceevyte
---- --- --------
"""

import os
import re
import shutil
import subprocess
import yaml
import pyttsx3


"""
Config Options
------ -------
"""

INPUT_FILE = "input.yml"
WAV_DIR = "tts_wav"
OGG_DIR = "tts_ogg"


if os.path.exists(WAV_DIR):
    shutil.rmtree(WAV_DIR)
if not os.path.exists(WAV_DIR):
    os.makedirs(WAV_DIR)

if os.path.exists(OGG_DIR):
    shutil.rmtree(OGG_DIR)
if not os.path.exists(OGG_DIR):
    os.makedirs(OGG_DIR)


def get_text(x):
    if isinstance(x, str):
        return x

    if isinstance(x, dict):
        if "text" in x:
            return x["text"]

        if "translate" in x:
            return apply_translate(
                x["translate"],
                x.get("with", [])
            )

        return ""

    if isinstance(x, list):
        return "".join(get_text(item) for item in x)

    return ""


def apply_translate(fmt, items):
    values = []
    for thing in items:
        values.append(get_text(thing))

    def replace(m):
        token = m.group(0)

        if token == "%s":
            if values:
                return values.pop(0)
            return ""

        num = re.match(r"%(\d+)\$s", token)
        if num:
            idx = int(num.group(1)) - 1
            if idx >= 0 and idx < len(values):
                return values[idx]

        return ""

    return re.sub(r"%\d+\$s|%s", replace, fmt)


with open(INPUT_FILE, encoding="utf-8") as f:
    raw = yaml.safe_load(f)

dialogue = []
speaker = None

for block in raw:
    for entry in block:
        if "text" in entry:
            line = entry["text"]
        elif "translate" in entry:
            line = apply_translate(entry["translate"], entry.get("with", []))
        else:
            continue

        line = line.strip()
        if not line:
            continue

        if line.startswith("[") and "]" in line:
            close = line.find("]")
            speaker = line[1:close].strip()
            remainder = line[close + 1:].strip()
            if remainder:
                dialogue.append((speaker, remainder))
        elif speaker:
            dialogue.append((speaker, line))


if not dialogue:
    raise RuntimeError("No dialogue found. Womp womp.")


speakers = []
for s, _ in dialogue:
    if s not in speakers:
        speakers.append(s)

engine = pyttsx3.init()
voices = engine.getProperty("voices")

english = [
    v.id for v in engine.getProperty("voices")
    if "en" in str(v.languages).lower() or "english" in v.name.lower()
]

if len(english) < len(speakers):
    raise RuntimeError("Not enough English voices installed :[")

voice_map = {}
for i, name in enumerate(speakers):
    voice_map[name] = english[i]

engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

print("Voice map:")
for k in voice_map:
    print(f"{k}: {voice_map[k]}")


for i in range(len(dialogue)):
    spk, text = dialogue[i]
    engine.setProperty("voice", voice_map[spk])
    out = os.path.join(WAV_DIR, f"{i}.wav")
    engine.save_to_file(text, out)

engine.runAndWait()


files = os.listdir(WAV_DIR)
files.sort(key=lambda x: int(x.split(".")[0]))

for f in files:
    if not f.endswith(".wav"):
        continue

    wav_path = os.path.join(WAV_DIR, f)
    ogg_path = os.path.join(OGG_DIR, f.replace(".wav", ".ogg"))

    # help 🥀
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", wav_path,
            "-af", "loudnorm,aresample=async=1",
            "-ac", "2",
            "-c:a", "libvorbis",
            "-q:a", "5",
            ogg_path,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

print(f"Generated {len(dialogue)} lines! :D")

if os.path.isdir(WAV_DIR):
    shutil.rmtree(WAV_DIR)