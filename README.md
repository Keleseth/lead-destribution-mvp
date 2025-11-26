ТЗ по реализации сервиса распределния запросов из арзнычх источников по оператором для вакансии ИП Веренько Игорь Николаевич - Backend-разработчик

### Технологии и инструменты
![Python](https://img.shields.io/badge/-Python%203.12-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-red?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/-Pydantic-orange?style=for-the-badge)
![Uvicorn](https://img.shields.io/badge/-Uvicorn-4B8BBE?style=for-the-badge)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![aiosqlite](https://img.shields.io/badge/-aiosqlite-2CA5E0?style=for-the-badge)

Описание:

Модели (SQLAlchemy, кратко):
- Source: источник обращения (бот). Поля: `id`, `description`.
- Operator: оператор обрабатывающий обращения. Поля: `id`, `name`, `active`, `load_limit`.
- Lead: Конечный пользователь. Поля: `uuid` (PK), `email` (UNIQUE). Связь: `interactions`.
- Interaction: обращение/взаимодействие. Поля: `id`, `lead_uuid` FK -> `Lead.uuid`, `source_id` FK -> `Source.id`, `operator_id` FK -> `Operator.id`, `is_active` - активно ли обращение.
- SourceOperatorSetting: Связующая таблица - настройка распределения для источника(Source). Поля: `id`, `source_id` FK -> `Source.id`, `operator_id` FK -> `Operator.id`, `weight` - приоритет для источника по выбору оператора (+ уникальность по паре `source_id`+`operator_id`).

CRUD (репозитории):
1. Круд-класс работы с таблицей `Interaction`
- InteractionCRUD: `create(lead_uuid, source_id, operator_id?)`, `get_by_id(id)`, `set_inactive(id)`, `flush/commit` через `AsyncSession`.
2. Круд-класс работы со связующей таблицей SourceOperatorSettingCRUD
- SourceOperatorSettingCRUD: `list_by_source(source_id)`, `get_candidates_for_distribution(source_id)` (только активные операторы), `replace_source_weights(...)`.
3. Круд-класс работы с таблицей `Lead`
- LeadCRUD: `get_or_create_by_email(email)` - найти по email или создать нового `Lead` если с таким email отсутствует, использует защищенный метод _get_by_email.

Схемы:
- CreateInteraction - создание Interaction, ожидает `email`, `source_id` и необязательное тело обращения - `payload`.
- ReadInteraction - схема чтения `Interactions` конкретного `Lead`.

Распределение (utils):
- `select_operator(session, source_id)`: выбирает оператора по weight активных операторов для заданного источника. Нагрузка пока не входит в mvp.

mvp Эндпоинты: 
- POST `/interaction`: приём обращения, find/create Lead по email, выбор оператора, создание `Interaction`.
- GET `/leads/{lead_uuid}/interactions`: Получение Interactions конкретного пользователя по его uuid.

База и зависимости:
- SQLite (async) через `aiosqlite`, `AsyncSession` для всех операций.


Развертывание и запуск:
```bash
git clone https://github.com/Keleseth/lead-destribution-mvp.git
cd lead-destribution-mvp

python -m venv venv
source .venv/Scripts/activate

pip install --upgrade pip
pip install -r requirements.txt

# Запуск приложения
uvicorn app.main:app --reload
```
