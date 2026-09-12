# web-app-security

---

Проект выполнен в рамках практических работ по дисциплине "Обеспечение безопасности при разработке программного обеспечения" 
ФГБОУ ВО "Тольяттинский государственный университет" (ФГБОУ В "ТГУ"), 01.09.2026 - 22.01.2027, г. Тольятти.

Автор: Бакулин Алексей Михайлович, студент ФГБОУ ВО "ТГУ", ИИиЭБ, группа ПИб-2310а.

---

## Установка и запуск проекта:

> [!NOTE]
> Для установки и запуска проекта необходимы Git и Python 3.8+

```comandline
git clone https://github.com/VanirSama/web-app-security.git
cd web-app-security
python -m venv .venv
```
Для Windows:
```comandline
.venv\Scripts\activate
```
Для Linux:
```commandline
source .venv\bin\activate
```

```commandline
python -m pip install --upgrade pip
pip install -r requirements.txt
```

В папке `src\` создайте `notes.db`, измените конфигурацию в `.env.example` и переименуйте в `.env`

```commandline
python -m src.app
```

В любом удобном браузере перейдите по `https://localhost:5000` или `https://127.0.0.1:5000`

---

Ссылки на отчеты по практическим работам:

- [Практическая работа №1](docs/L1.md)