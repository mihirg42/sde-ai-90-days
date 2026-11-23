# sde-ai-90-days

A simple Task Manager REST API built with [FastAPI](https://fastapi.tiangolo.com/) and [Pydantic](https://docs.pydantic.dev/). Tasks are stored in memory, so data resets whenever the server restarts.

## Prerequisites

- Python 3.10 or newer
- `pip`

## Setup

### 1. Create and activate a virtual environment

From the project root:

```bash
python3 -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**

```cmd
venv\Scripts\activate.bat
```

When it is active, your terminal prompt shows `(venv)`. To leave the environment later, run `deactivate`.

### 2. Install dependencies

If the repo has a `requirements.txt`:

```bash
pip install -r requirements.txt
```

Otherwise, install FastAPI with its standard extras (this includes the `fastapi` CLI and Uvicorn):

```bash
pip install "fastapi[standard]"
```

Pydantic is installed automatically as a FastAPI dependency.

## Running the server

Start the development server with auto-reload:

```bash
fastapi dev main.py
```

Alternatively, using Uvicorn directly:

```bash
uvicorn main:app --reload
```

The API is now available at <http://127.0.0.1:8000>.

## API documentation (Swagger UI)

Interactive docs are generated automatically. Open:

- **Swagger UI:** <http://127.0.0.1:8000/docs>
- **ReDoc:** <http://127.0.0.1:8000/redoc>

From Swagger UI you can try every endpoint directly in the browser.

## Data model

```json
{
  "id": 1,
  "title": "Write docs",
  "description": "Finish the README",
  "completed": false
}
```

| Field         | Type    | Notes                               |
| ------------- | ------- | ----------------------------------- |
| `id`          | integer | Assigned by the server, starts at 1 |
| `title`       | string  | Required, must not be empty         |
| `description` | string  | Required, must not be empty         |
| `completed`   | boolean | Optional, defaults to `false`       |

## Endpoints

| Method   | Path               | Description                                                                                          |
| -------- | ------------------ | ---------------------------------------------------------------------------------------------------- |
| `GET`    | `/tasks`           | Returns the list of all tasks.                                                                       |
| `GET`    | `/tasks/{task_id}` | Returns a single task by its ID. Responds with 404 if not found.                                     |
| `POST`   | `/tasks`           | Creates a new task and returns it with its generated `id`. Rejects empty `title` or `description`.   |
| `PUT`    | `/tasks/{task_id}` | Fully replaces an existing task with the request body. Responds with 404 if the task does not exist. |
| `DELETE` | `/tasks/{task_id}` | Deletes the task with the given ID. Responds with 404 if not found.                                  |

### Example requests

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Write docs", "description": "Finish the README"}'
```

List all tasks:

```bash
curl http://127.0.0.1:8000/tasks
```

Get one task:

```bash
curl http://127.0.0.1:8000/tasks/1
```

Update a task (send the full object; omitted `completed` resets to `false`):

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Write docs", "description": "Finish the README", "completed": true}'
```

Delete a task:

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```
