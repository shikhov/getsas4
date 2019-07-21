# Описание
Приложение для платформы Google App Engine, которое периодически проверяет папку в Google Drive на наличие новой версии SAS4Android и присылает ее в Telegram.

Результат работы: https://t.me/sas4android

# Настройка
Переименуйте прилагаемый example.config.py в config.py и отредактируйте его.

**TGTOKEN** — токен бота в Telegram

**TGCHATID** — id целевого чата в Telegram

**GAPIKEY** — ключ Google Drive API

**GFOLDERID** — id папки в Google Drive

В файле cron.yaml задается периодичность проверки, по умолчанию — раз в час.