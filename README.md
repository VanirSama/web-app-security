# web-app-security

---

Проект выполнен в рамках практических работ по дисциплине "Обеспечение безопасности при разработке программного обеспечения" 
ФГБОУ ВО "Тольяттинский государственный университет" (ФГБОУ В "ТГУ"), 01.09.2026 - 22.01.2027, г. Тольятти.

Автор: Бакулин Алексей Михайлович, студент ФГБОУ ВО "ТГУ", ИИиЭБ, группа ПИб-2310а.

---

## Установка и запуск проекта:

> [!NOTE]
> Для установки и запуска проекта необходимы Git и Python 3.8+

```bash
git clone https://github.com/VanirSama/web-app-security.git
cd web-app-security
python -m venv .venv
```
Для Windows:
```bash
.venv\Scripts\activate
```
Для Linux:
```bash
source .venv\bin\activate
```

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

В папке `src\` создайте `notes.db`, измените конфигурацию в `.env.example` и переименуйте в `.env`

```bash
python run.py
```

В любом удобном браузере перейдите по `https://localhost:5000` или `https://127.0.0.1:5000`