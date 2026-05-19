# Narrativa

[![English](https://img.shields.io/badge/Language-English-blue)](README.md)
[![Русский](https://img.shields.io/badge/Язык-Русский-red)](assets/README/ru.md)

> Движок диалогов для Minecraft.

[![GitHub][github-repo]][repo-url]

### Что такое Narrativa?
Narrativa это движок диалогов для датапаков Minecraft 1.21.11. Он позволяет писать разветвлённые разговоры, описания, текст для атмосферы и всё, что угодно. Он сделан с помощью Bolt и использует модули `.bolt`.

Он обрабатывает API, визуальную часть, логику и автоматические голосовые строки. Ты просто задаёшь контент, а он делает остальное.

![Эт я :3](assets/header/ru.png)

## Как это использовать

Диалог состоит из двух основных частей: узлов диалога и меню выбора.

### Узел диалога
```Python
function username:dialog/example/greeting:
    Narrativa.new_dialog(
        lines=[
            ['Cee Vyte: "Это полностью под твоим', 'контролем, кстати говоря.'],
            ''
        ],
        actions=[
            "",
            "function username:choice/example/greeting"
        ],
        autodub="username:dialog.example.greeting."
    )
```
`lines` это текст, который показывается каждый кадр. Каждый элемент это либо список строк (как сообщение /tellraw), либо пустая строка для пропуска кадра.

`actions` запускает команды после каждого кадра. Пустые строки ничего не делают. Каждое действие должно соответствовать кадру, иначе всё сломается и рассинхронизируется.

`autodub` это префикс для автоматического воспроизведения звука текущего кадра. Он сам управляет индексом кадров. Его можно не использовать, если не нужно.

### Меню выбора
```Python
function username:choice/example/greeting:
    choice_menu(
        title="Заголовок меню выбора:",
        options=[
            Choice(
                "Вариант A.",
                "say Выбран: Вариант А!"
            ),
            Choice(
                "Вариант Б.",
                "say Выбран: Вариант Б!"
            )
        ]
    )
```

Меню выбора показывает варианты и выполняет команду при выборе. Оно предназначено для вариантов ответа, но его можно использовать как угодно.

### Связывание всего вместе
Ты связываешь узлы, делая последнее действие переходом к следующему узлу или меню выбора. Попробуй и поймёшь.

Замени `username` на свой юзернейм в Minecraft, а `example` на название твоего проекта или пространство имён.

## Настройка разработки
Склонируй репозиторий и всё готово.
```Bash
curl -L https://github.com/DelightZone/narrativa/releases/latest/download/release.zip -o narrativa.zip
unzip narrativa.zip -d narrativa/
cd narrativa
pip install -r requirements.txt
```

## Метаданные
Cee Vyte, @ceevyte, kosoycded@gmail.com

Распространяется под лицензией GPL-3.0. См. LICENSE для подробностей.

[github-repo]: https://img.shields.io/badge/DelightZone-narrativa-blue?logo=github
[repo-url]: https://github.com/DelightZone/narrativa

## Участие в разработке

1. Сделай форк [GitHub fork](https://github.com/DelightZone/narrativa/fork)
2. Cоздай ветку (`git checkout -b feature/fooBar`)
3. Закоммить изменения (`git commit -am 'Add fooBar'`)
4. Запушь изменения (`git push origin feature/fooBar`)
5. Открой [Пул-Реквест](https://github.com/DelightZone/narrativa/pulls)

## Атрибуция

- [xllifi](https://modrinth.com/resourcepack/mc10) — автор шрифта `mc10`, использованного в Narrativa