
## Virtual environment

### Установка

```bash
pip install virtualenv
virtualenv env
source env/bin/activate
alias pip=`pwd`/env/bin/pip3.7
alias python=`pwd`/env/bin/puyhon3.7
pip install -r requirements.txt
```

### Запуск сервера
```bash
FLASK_APP=app.py python app.py
```
---
## REST API

