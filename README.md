# Narrativa
A project based on Bolt datapack pre-compiler, made specifically to aid in creating dialogues with ease. 

## Examples:
Everything in the examples folder works the way it was intended, please report any bugs or issues.

Run `/function ceevyte:dialogues/example/hello_world` to start the example Hello World dialogue.
It will explain the basics to you. At the end of the dialogue, there will be Choice options (which is it's own system).
Pick either `[2] Cheese.` for the showcase of capabilities in-use; or `[3] Could you explain it a bit more?` for a more technical explanation of how to actually use it.

To simplify your pain in the back, I'll paste the technical explanation here directly:

### could_you_explain.yml
Hello. I am NarrativaBot. I will now explain Narrativa.
Warning. Keep Narrativa in a separate datapack from your main project.
Failing to do so will cause static dialogues to rebuild on every 'beet build'. This is undesirable.
- Step 1. Place the 'dialogues' folder at the top level of your project.
Place your .yml files inside it. Reference them from a module.
- Step 2. Create a module. Recommended name: 'X_narrativa_content.bolt'.
Register it in beet.json under meta/bolt/entrypoint, next to 'narrativa.bolt'.
For module contents, refer to provided examples. They are sufficient.
- Step 3. Dialogue format.
Dialogues must follow this structure: DialogueArray[ IndividualLine[ FirstList{ Components } ] ]
Deviation from this structure will cause in-game silent errors. There are no exceptions.
- Step 4. Autodub. Place your dialogue file in the script folder, rename it 'input.yml', run the script.
Output: .ogg files from 0 to N. Requires enough different English voices to be installed on your system.
- Step 5. sounds.py. Open it. Add dialogue lines to the 'specs' array as shown in examples.
Run the script. Output: sounds.json. Place it in your ResourcePack.
Ensure the .ogg file path in sounds.py matches the actual file location.
- Step 6. Choice system. Three calls required.
[1] Narrativa.newChoice()
[2] Send a tellraw with your choice menu. Style is yours to define.
[3] Call Narrativa.lockChoice( Array[ ChoiceN{ function: \ChoiceN's Function\} ] ), with ChoiceN for each option provided.
End of documentation. Beep-boop.

(This dialogue file can be found at: `..\dialogues\example\hello_world\could_you_explain.yml`, if you want to see the structure behind it.)

# Usage:
## Dialogues
After setup, create a new dialogue in `..\dialogues\`, please keep the name & path of it consistent everywhere.
Inside of it, you'll quickly notice that the YML format is simply JSON here. Imagine yourself writing a `/tellraw` command, where arrays inside the main array each are a new line.
Make sure it follows this structure: DialogueArray[ IndividualLine[ FirstList{ Components } ] ], or otherwise it just breaks. (Yeah, I know.)
After you're done with that, head over to your newly created `narrativa_content.bolt` module, import Narrativa module `import ./narrativa as Narrativa` (both should be in the same folder).

Since this is an example, we'll do a simple dialogue trigger for now, but you can make your own, just call `function ceevyte:narrativa/dialogue/_/step` when it does trigger:
```
append function_tag minecraft:load {
    "values": [
        "username:dialogue/load"
    ]
}
append function_tag minecraft:tick {
    "values": [
        "username:dialogue/tick"
    ]
}
predicate username:dialogue/trigger {
    "condition": "minecraft:entity_properties",
    "entity": "this",
    "predicate": {
        "type_specific": {
            "type": "minecraft:player",
            "input": {
                "forward": false,
                "backward": false,
                "left": false,
                "right": false,
                "jump": false,
                "sneak": false,
                "sprint": true
            }
        }
    }
}
function username:dialogue/load:
    scoreboard objectives add username.dialogue.trigger dummy {"text": "Dialogue Trigger Flip-Flop", "color": "gold"}
function username:dialogue/tick:
    execute as @a[tag=ceevyte.narrativa.dialogue.active]:
        execute if score @s[predicate=!username:dialogue/trigger] username.dialogue.trigger matches 1:
            scoreboard players reset @s username.dialogue.trigger
        execute unless score @s[predicate=username:dialogue/trigger] username.dialogue.trigger matches 1..:
            function ceevyte:narrativa/dialogue/_/step
            scoreboard players set @s username.dialogue.trigger 1
```

This will be enough for now. Next, you need to load all dialogues, choices, actions, etc.

To import the YML file as a Dialogue, do this:
```
function username:dialogues/example/hello_world:
    Narrativa.newDialogue(Narrativa.loadDialogue(
        "dialogues/example/hello_world.yml"
    ), "username:dialogues.example.hello_world.")
```

This structure is essentially this:
```
function START_FUNCTION:
    Narrativa.newDialogue(Narrativa.loadDialogue(
        "PATH_TO_DIALOGUE_FILE.yml"
    ), "AUTODUB_SOUND_NAME")
```

Autodub is optional; works by inserting `autodub` component inside of the first list of the line, which contains an indexed sound name.
You can also build your own interpreter: The `Narrativa.newDialogue(ArrayJSON)` just requires a valid `/tellraw` command by this structure: `[[NewDialogueLine], ..., [NewDialogueLine]]`
(E.g. `[[{"text": "<username> Hello there!"}], [{"text": "I'm inside a dialogue. Cool, right?"}]]` is a valid input.

By running `beet build`, the dialogues should be compiled into a datapack properly.

## Choices
This one is a lot easier, and requires less fiddling with my awful code.
To make a choice, you define a new starting function, just like with a dialogue's starting function:
```
function username:choices/example/hello_world:
    Narrativa.newChoice()
```
Place `Narrativa.newChoice()` inside of it.
Second command should be the `/tellraw` display of your choice. Use `click_event` to `run_command`, but instead of running an actual command, just put `Narrativa.choiceCounter()` there. It automatically generates a /trigger command, so it will work even without the cheats being on!
After the command, you should call
```
Narrativa.lockChoice( [
      {
      # 1st Option
      "function": "username:dialogues/example/hello_world/destination1"
      },
      {
      # 2nd Option
      "function": "username:actions/example/hello_world/destination2"
      }
  ])
```
where each "function" parameter correlates to the according choice option. This can be any function.

Here's an example choice:
```
function ceevyte:choices/example/hello_world:
    Narrativa.newChoice()
    tellraw @s [
        {
            "text": "\n"
        },
        {
            "text": "— [1] Wowww, that's so cool :0",
            "color": "gray",
            "click_event": {
                "action": "run_command",
                # This function exists so that you don't have to type out the numbers manually,
                # and you can thank me later :^
                "command": Narrativa.choiceCounter()
            },
            "hover_event": {
                "action": "show_text",
                "value": [
                    {
                        # You can do like, descriptions and stuff, but that's just
                        # generic Json tellraw.
                        "text": "False flattery. Classic."
                    }
                ]
            }
        },
        {
            "text": "\n"
        },
        {
            "text": "— [2] Cheese.",
            "color": "gray",
            "click_event": {
                "action": "run_command",
                "command": Narrativa.choiceCounter()
            },
            "hover_event": {
                "action": "show_text",
                "value": [
                    {
                        "text": "I... honestly don't remember putting this in. O_o"
                    }
                ]
            }
        },
        {
            "text": "\n"
        },
        {
            "text": "— [3] Could you explain it a bit more?",
            "color": "gray",
            "click_event": {
                "action": "run_command",
                "command": Narrativa.choiceCounter()
            },
            "hover_event": {
                "action": "show_text",
                "value": [
                    {
                        "text": "Nerd."
                    }
                ]
            }
        }
    ]
    Narrativa.lockChoice(
        [
            # [1]
            {
                "function": "ceevyte:dialogues/example/hello_world/that_s_so_cool"
            },
            # [2]
            {
                "function": "ceevyte:dialogues/example/hello_world/cheese"
            },
            # [3]
            {
                "function": "ceevyte:dialogues/example/hello_world/could_you_explain"
            }
        ]
    )
```

# Commonly asked questions:
Q: Do I really need to load the narrativa.bolt as a module?
A: Yes, the `narrativa.bolt` is the Library module itself, and is required to be loaded by beet, preferably before the narrativa_content modules.

Q: Why is there code instead of just .mcfunction?
A: Beet.

Q: Can I rewrite your stupid code and make a better one?
A: PLEASE DO.

Q: How do I install Beet properly?
A: https://www.youtube.com/watch?v=IOS-OnqE4GY

Q: How to install the datapack?
A: Either do `beet link (your world path at "../saves/")` in VSCode's console, or drag them there manually OR download the latest Release from this repository.

Q: Will it be updated further?
A: Of course, I need to fix everything here, lol.
