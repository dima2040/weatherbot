# weatherbot
Weather telegram bot
Использует API open-meteo.com

## Установка и настройка

Создайте и активируйте окружение
```sh
python3 -m venv .venv
source .venv/bin/activate
```

Установите зависимости
```sh
python -m pip install -r requirements.txt
```

## Запуск

Укажите нужную переменную окружения
```sh
export WEATHER_BOT_API_TOKEN=***
```

```sh
python main.py
```
