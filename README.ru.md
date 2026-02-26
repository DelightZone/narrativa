<div align="center">
  🌍 <strong>Язык / Language:</strong>
  <br>
  <a href="README.ru.md">Русский</a> • <a href="README.md">English</a>
</div>

---

<div align="center">

# ⚔️ Narrativa

### Проект на основе предкомпилятора Bolt для датапаков. Создан специально для удобной разработки диалогов.

[![Beet](https://img.shields.io/badge/Powered%20by-Beet-yellow)](https://github.com/minecraft-beet/beet)
[![Bolt](https://img.shields.io/badge/Built%20with-Bolt-orange)](https://github.com/mcbeet/bolt)
[![Minecraft](https://img.shields.io/badge/Minecraft-Datapack-green)](https://www.minecraft.net)

[Быстрый старт](#-quick-start--examples) •
[Установка и документация](#-setup--documentation) •
[Диалоги](#-dialogues) •
[Выборы](#-choices) •
[FAQ](#-commonly-asked-questions)

</div>

---

## 🚀 Быстрый старт и примеры

Всё в папке `examples` работает как задумано. Если найдёте баг или проблему, пожалуйста сообщите.

Чтобы запустить пример Hello World в игре, выполните команду:
```mcfunction
/function ceevyte:dialogues/ru_ru/example/hello_world
```
Диалог объяснит основы. В конце появятся варианты выбора. Это отдельная система.
Выберите `[2] Сыр.` чтобы увидеть демонстрацию возможностей. Или `[3] Можешь объяснить это немного подробнее?` для более технического объяснения.

---

## 📚 Установка и документация

Чтобы сэкономить вам время, ниже техническое объяснение:

> ⚠️ **Внимание:** Держите Нарратива в отдельном датапаке от основного проекта. Иначе статические диалоги будут пересобираться при каждом `beet build`. Это нежелательно.

### Шаг 1: Папки
Поместите папку `dialogues` в корень проекта.
Внутрь добавьте ваши файлы `.yml`.
Название и путь должны быть одинаковыми везде.
Подключайте их через модуль.

### Шаг 2: Модули
Создайте модуль. Рекомендуемое имя: `X_narrativa_content.bolt`.
Зарегистрируйте его в `beet.json` в разделе meta/bolt/entrypoint, рядом с `narrativa.bolt`.
**Важно:** Внутри вашего модуля необходимо импортировать Нарратива. Оба файла должны быть в одной папке:
```bolt
import ./narrativa as Narrativa
```

### Шаг 3: Autodub и звуки. Необязательно
Autodub автоматически создаёт озвучку.
1. Поместите файл диалога в папку script, переименуйте в `input.yml` и запустите скрипт.
   *(Результат: файлы `.ogg` от 0 до N. На системе должны быть установлены разные английские голоса.)*
2. Откройте `sounds.py`. Добавьте строки диалога в массив `specs` по примеру.
3. Запустите скрипт. *(Результат: `sounds.json`).*
4. Поместите его в ресурспак. Убедитесь, что путь к `.ogg` в `sounds.py` совпадает с реальным расположением файла.

---

## 💬 Диалоги

Внутри файлов `.yml` используется формат JSON. Представьте, что вы пишете команду `/tellraw`, где каждый массив внутри основного массива это новая строка.

### Формат диалога
Диалоги **обязаны** строго соблюдать структуру:
```json
DialogueArray[ IndividualLine[ FirstList{ Components } ] ]
```
> 🛑 Отклонение от этой структуры вызовет тихие ошибки в игре. Исключений нет. Иначе всё просто ломается.

*Пример корректной структуры:*
```json
[
  [{"text": "<username> Hello there!"}], 
  [{"text": "I'm inside a dialogue. Cool, right?"}]
]
```
*(Autodub добавляет компонент `autodub` в первый список строки. В нём хранится индексированное имя звука.)*

### Загрузка диалога
Чтобы импортировать YML как диалог, структура функции должна быть такой:
```bolt
function START_FUNCTION:
    Narrativa.newDialogue(Narrativa.loadDialogue(
        "PATH_TO_DIALOGUE_FILE.yml"
    ), "AUTODUB_SOUND_NAME")
```

Пример:
```bolt
function username:dialogues/ru_ru/example/hello_world:
    Narrativa.newDialogue(Narrativa.loadDialogue(
        "dialogues/ru_ru/example/hello_world.yml"
    ), "username:dialogues.ru_ru.example.hello_world.")
```
*(Можно написать собственный интерпретатор, так как `Narrativa.newDialogue(ArrayJSON)` просто требует корректную структуру /tellraw, описанную выше.)*

### Пример триггера диалога
Так это пример, мы сделаем простой триггер. Просто вызови `function ceevyte:narrativa/dialogue/_/step` когда триггер активирован. На пример:

<details>
<summary><strong>Показать Код Триггера (Логика по Нажатию Кнопки)</strong></summary>

```bolt
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
    scoreboard objectives add username.dialogue.trigger dummy {"text": "Триггер Диалога по Нажатию", "color": "gold"}

function username:dialogue/tick:
    execute as @a[tag=ceevyte.narrativa.dialogue.active]:
        execute if score @s[predicate=!username:dialogue/trigger] username.dialogue.trigger matches 1:
            scoreboard players reset @s username.dialogue.trigger
        execute unless score @s[predicate=username:dialogue/trigger] username.dialogue.trigger matches 1..:
            function ceevyte:narrativa/dialogue/_/step
            scoreboard players set @s username.dialogue.trigger 1
```
</details>

После выполнения `beet build` диалоги будут скомпилированы в датапак.

---

## 🔀 Выборы

Эта система проще и требует меньше настроек.
Нужно три вызова:
1. `Narrativa.newChoice()` в начале функции.
2. `tellraw` с меню выбора. Стиль на ваше усмотрение.
3. `Narrativa.lockChoice(...)` в конце.

### Как работают клики
Используйте `click_event` с `run_command`, но вместо команды укажите Narrativa.choiceCounter(). **Она автоматически создаёт `/trigger`, поэтому всё работает даже без включённых читов.**

### Полный пример выбора
```bolt
function ceevyte:choices/ru_ru/example/hello_world:
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
                "function": "ceevyte:dialogues/ru_ru/example/hello_world/that_s_so_cool"
            },
            # [2]
            {
                "function": "ceevyte:dialogues/ru_ru/example/hello_world/cheese"
            },
            # [3]
            {
                "function": "ceevyte:dialogues/ru_ru/example/hello_world/could_you_explain"
            }
        ]
    )
```
*Запомните: Каждый параметр "function" в lockChoice соответствует варианту выбора по порядку. Это может быть любая функция.*

---

## ❓ Частые вопросы

**В: Нужно ли подключать narrativa.bolt как модуль?**
> **О:** Да. Это библиотечный модуль. Он должен быть загружен через Beet, желательно раньше модулей `narrativa_content`.

**В: Почему используется код, а не просто `.mcfunction`?**
> **О:** Потому что используется Beet.

**В: Можно переписать код и сделать лучше?**
> **О:** Да. Пожалуйста.

**В: Как правильно установить Beet?**
> **О:** [https://www.youtube.com/watch?v=IOS-OnqE4GY](https://www.youtube.com/watch?v=IOS-OnqE4GY)

**В: Как установить датапак?**
> **О:** Выполните `beet link (путь к миру "../saves/")` в консоли VSCode, либо перенесите файлы вручную, либо скачайте последний релиз из репозитория.

**В: Будут ли обновления?**
> **О:** Да. Проект ещё требует доработки.