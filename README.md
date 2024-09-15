# DreamNotes

### Структура проекта

- **app/api/**: Содержит роутеры для обработки запросов.
- **app/models/**: Модели SQLAlchemy для базы данных.
- **app/schemas

### API для заметок

- **POST /notes/**: Создание новой заметки.
- **GET /notes/**: Получение списка заметок.
- **GET /notes/{note_id}**: Получение заметки по ID.
- **PUT /notes/{note_id}**: Обновление заметки по ID.
- **DELETE /notes/{note_id}**: Удаление заметки по ID.

### Примеры запросов

- **Создание заметки**:

```bash
curl -X POST "http://localhost:8000/notes/" -H "Content-Type: application/json" -d '{"title": "Note Title", "content": "Note Content", "tags": ["tag1", "tag2"]}'
