<details open>
<summary>🌍 <strong>Language / Язык</strong></summary>

- [English](README.md)
- [Русский](README.ru.md)

</details>

---

<div align="center">

# ⚔️ Narrativa

### A powerful dialogue system for Minecraft datapacks based on Bolt pre-compiler

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Beet](https://img.shields.io/badge/Powered%20by-Beet-yellow)](https://github.com/minecraft-beet/beet)
[![Bolt](https://img.shields.io/badge/Built%20with-Bolt-orange)](https://github.com/mcbeet/bolt)
[![Minecraft](https://img.shields.io/badge/Minecraft-Datapack-green)](https://www.minecraft.net)

**Made by [@ceevyte](https://github.com/ceevyte)**

[Features](#-features) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Examples](#-examples) •
[FAQ](#-frequently-asked-questions)

</div>

---

## ✨ Features

- 🎭 **Easy Dialogue Creation** - Define dialogues in simple YAML format
- 🎨 **Rich Text Support** - Full tellraw formatting with colors, hover events, and click actions
- 🔊 **Auto-Dubbing** - Automatic voice generation with English voices
- 🔀 **Choice System** - Interactive player choices with customizable options
- ⚡ **Fast Compilation** - Built on Beet & Bolt for optimal performance
- 🎮 **Trigger System** - Flexible dialogue triggering with predicates
- 📦 **Modular Design** - Separate datapack for better organization

---

## 🚀 Quick Start

### Prerequisites

- [Beet](https://github.com/minecraft-beet/beet) - Minecraft datapack development toolchain
- Python 3.x (for auto-dubbing feature)

### Installation

```bash
# Clone the repository
git clone https://github.com/ceevyte/narrativa.git
cd narrativa

# Install dependencies
pip install -r requirements.txt  # if using auto-dubbing

# Build the datapack
beet build
```

### Usage

Run `/function ceevyte:dialogues/example/hello_world` to start the example dialogue.

---

## 📚 Documentation

### Setup Steps

<details>
<summary><strong>Step 1: Dialogues Folder</strong></summary>

Place the `dialogues` folder at the top level of your project. Put your `.yml` files inside it.

</details>

<details>
<summary><strong>Step 2: Create Module</strong></summary>

Create a module (recommended name: `X_narrativa_content.bolt`).
Register it in `beet.json` under `meta/bolt/entrypoint`, next to `narrativa.bolt`.

</details>

<details>
<summary><strong>Step 3: Dialogue Format</strong></summary>

Dialogues must follow this structure:
```
DialogueArray [ IndividualLine [ FirstList { Components } ] ]
```

**⚠️ Warning:** Deviation from this structure will cause in-game silent errors.

</details>

<details>
<summary><strong>Step 4: Auto-Dub (Optional)</strong></summary>

1. Place your dialogue file in the `tools/autodub` folder
2. Rename it to `input.yml`
3. Run the script (requires English voices on your system)
4. Output: `.ogg` files from 0 to N

</details>

<details>
<summary><strong>Step 5: Sounds Configuration</strong></summary>

1. Open `src/assets/ceevyte/sounds.py`
2. Add dialogue lines to the `specs` array
3. Run the script
4. Output: `sounds.json` - Place it in your ResourcePack

</details>

<details>
<summary><strong>Step 6: Choice System</strong></summary>

Three calls required:
1. `Narrativa.newChoice()`
2. Send a tellraw with your choice menu
3. `Narrativa.lockChoice(Array[ChoiceN{function: "ChoiceN's Function"}])`

</details>

### Dialogue Example

```yaml
# dialogues/example/hello_world.yml
[
  [
    {"text": "<NarrativaBot> Hello there!"},
    {"text": "\n", "color": "white"},
    {"text": "Welcome to Narrativa!", "color": "gold"}
  ]
]
```

### Code Example

```python
function username:dialogues/example/hello_world:
    Narrativa.newDialogue(Narrativa.loadDialogue(
        "dialogues/example/hello_world.yml"
    ), "username:dialogues.example.hello_world.")
```

---

## 🎮 Usage Examples

### Dialogue Trigger

```bolt
function username:dialogue/load:
    scoreboard objectives add username.dialogue.trigger dummy
    {"text": "Dialogue Trigger Flip-Flop", "color": "gold"}

function username:dialogue/tick:
    execute as @a[tag=ceevyte.narrativa.dialogue.active]:
        execute if score @s[predicate=!username:dialogue/trigger] username.dialogue.trigger matches 1:
            scoreboard players reset @s username.dialogue.trigger
        execute unless score @s[predicate=username:dialogue/trigger] username.dialogue.trigger matches 1..:
            function ceevyte:narrativa/dialogue/_/step
            scoreboard players set @s username.dialogue.trigger 1
```

### Choice Menu

```bolt
function ceevyte:choices/example/hello_world:
    Narrativa.newChoice()
    tellraw @s [
        {
            "text": "\n— [1] Wowww, that's so cool :0",
            "color": "gray",
            "click_event": {
                "action": "run_command",
                "command": Narrativa.choiceCounter()
            }
        },
        {
            "text": "\n— [2] Could you explain it a bit more?",
            "color": "gray",
            "click_event": {
                "action": "run_command",
                "command": Narrativa.choiceCounter()
            }
        }
    ]
    Narrativa.lockChoice([
        {"function": "ceevyte:dialogues/example/hello_world/cool"},
        {"function": "ceevyte:dialogues/example/hello_world/explain"}
    ])
```

---

## ❓ Frequently Asked Questions

<details>
<summary><strong>Q: Do I really need to load the narrativa.bolt as a module?</strong></summary>

**A:** Yes, the `narrativa.bolt` is the Library module itself, and is required to be loaded by Beet, preferably before the narrativa_content modules.
</details>

<details>
<summary><strong>Q: Why is there code instead of just .mcfunction?</strong></summary>

**A:** Beet provides powerful features that plain .mcfunction doesn't have, like module system, macros, and better organization.
</details>

<details>
<summary><strong>Q: Can I rewrite your code and make a better one?</strong></summary>

**A:** **PLEASE DO!** This is an open-source project, and contributions are welcome. 🙏
</details>

<details>
<summary><strong>Q: How do I install Beet properly?</strong></summary>

**A:** Check out [this tutorial](https://www.youtube.com/watch?v=IOS-OnqE4GY)
</details>

<details>
<summary><strong>Q: How to install the datapack?</strong></summary>

**A:** Either use `beet link (your world path)` in VSCode, drag the build folder manually, or download the latest Release from this repository.
</details>

<details>
<summary><strong>Q: Will it be updated further?</strong></summary>

**A:** Of course! There's always room for improvement and bug fixes.
</details>

---

## 🤝 Contributing

Contributions are welcome! If you want to improve Narrativa:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

- Built with [Beet](https://github.com/minecraft-beet/beet)
- Powered by [Bolt](https://github.com/mcbeet/bolt)
- Made with ❤️ by [@ceevyte](https://github.com/ceevyte)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [@ceevyte](https://github.com/ceevyte)

</div>
