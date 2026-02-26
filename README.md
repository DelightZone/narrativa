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
Dialogues must follow this structure: DialogueArray[ IndividualLine[ FirstTellraw{ Components } ] ]
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

## Commonly asked questions:
Q: Do I really need to load the narrativa.bolt as a module?
A: Yes, the `narrativa.bolt` is the Library module itself, and is required to be loaded by beet, preferably before the narrativa_content modules.

Q: Why is there code instead of just .mcfunction?
A: Beet.

Q: How do I install it properly?
A: https://www.youtube.com/watch?v=IOS-OnqE4GY

Q: How to install it?
A: Either do `beet link (your world path at "../saves/")` in VSCode's console, or drag them there manually OR download the latest Release from this repository.

Q: How did you even came up with this spaghetti code?
A: You tell me.

Q: Will it be updated further?
A: Of course, I need to fix everything here, lol.
