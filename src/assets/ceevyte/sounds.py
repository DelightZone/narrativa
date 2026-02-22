import json

def make_dialogue_json(dialogue_name, sound_path, count):
    data = {}
    for i in range(count):
        idx = f"{i}"
        key = f"{dialogue_name}.{idx}"
        data[key] = {"sounds": [{"name": f"{sound_path}/{idx}"}]}
    return data

def auto_merge_dialogues(dialogue_specs):
    merged = {}
    for spec in dialogue_specs:
        if len(spec) == 3:
            name, path, count = spec
        else:
            raise ValueError("Wrong specs.")

        d = make_dialogue_json(name, path, count)
        overlap = merged.keys() & d.keys()
        if overlap:
            raise ValueError(f"Duplicate dialogue keys found: {overlap}!")
        merged.update(d)
    return merged


if __name__ == "__main__":
    specs = [
        ("dialogues.example.hello_world", "ceevyte:dialogues/example/hello_world", 18),
        ("dialogues.example.hello_world.cheese", "ceevyte:dialogues/example/hello_world/cheese", 9),
        ("dialogues.example.hello_world.could_you_explain", "ceevyte:dialogues/example/hello_world/could_you_explain", 25),
        ("dialogues.example.hello_world.that_s_so_cool", "ceevyte:dialogues/example/hello_world/that_s_so_cool", 5)
    ]

    final_json = auto_merge_dialogues(specs)
    with open("sounds.json", "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4)
