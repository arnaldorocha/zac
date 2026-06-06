# Zac API Documentation

Complete REST API reference for Zac Personal Assistant.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required. For production deployment, consider adding JWT tokens.

## Response Format

All responses are JSON:

```json
{
  "message": "Operation completed",
  "success": true
}
```

---

## Endpoints

### Health Check

#### `GET /health`

Check if API is running.

**Response:**
```json
{
  "status": "online",
  "assistant": "Zac"
}
```

---

## Commands

### Execute Voice Command

#### `POST /command`

Execute a text command (simulates voice input).

**Request:**
```json
{
  "text": "adicionar tarefa estudar Python"
}
```

**Response:**
```json
{
  "message": "Tarefa adicionada: estudar Python",
  "success": true
}
```

### Listen for Voice

#### `POST /listen`

Listen for voice command and execute.

**Response:**
```json
{
  "message": "Tarefa adicionada: estudar Python",
  "success": true
}
```

---

## Tasks

### Create Task

#### `POST /tasks`

Create a new task.

**Request:**
```json
{
  "title": "Study Machine Learning",
  "description": "Complete ML course",
  "priority": "high",
  "due_date": "2024-06-10T19:00:00",
  "tags": ["learning", "ai"]
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Study Machine Learning",
  "status": "todo",
  "priority": "high"
}
```

### List All Tasks

#### `GET /tasks`

Get all tasks.

**Response:**
```json
{
  "count": 5,
  "tasks": [
    {
      "id": 1,
      "title": "Study Machine Learning",
      "status": "todo",
      "priority": "high",
      "due_date": "2024-06-10T19:00:00"
    }
  ]
}
```

### Get Today's Tasks

#### `GET /tasks/today`

Get tasks for today.

**Response:**
```json
{
  "count": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Morning workout",
      "status": "todo",
      "priority": "medium"
    }
  ]
}
```

### Complete Task

#### `PATCH /tasks/{task_id}/complete`

Mark task as completed.

**Response:**
```json
{
  "message": "Task 1 completed",
  "success": true
}
```

### Delete Task

#### `DELETE /tasks/{task_id}`

Delete a task.

**Response:**
```json
{
  "message": "Task 1 deleted",
  "success": true
}
```

---

## Calendar/Events

### Create Event

#### `POST /events`

Create calendar event.

**Request:**
```json
{
  "title": "Team Meeting",
  "description": "Weekly sync",
  "start_time": "2024-06-05T14:00:00",
  "end_time": "2024-06-05T15:00:00",
  "location": "Conference Room A"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Team Meeting",
  "start_time": "2024-06-05T14:00:00"
}
```

### List All Events

#### `GET /events`

Get all calendar events.

**Response:**
```json
{
  "count": 3,
  "events": [
    {
      "id": 1,
      "title": "Team Meeting",
      "start_time": "2024-06-05T14:00:00",
      "location": "Conference Room A"
    }
  ]
}
```

### Get Today's Events

#### `GET /events/today`

Get today's events.

**Response:**
```json
{
  "count": 1,
  "events": [
    {
      "id": 1,
      "title": "Team Meeting",
      "start_time": "2024-06-05T14:00:00"
    }
  ]
}
```

---

## Memory

### Save Memory Entry

#### `POST /memory`

Save information to memory.

**Query Parameters:**
- `key` (string): Memory key
- `value` (string): Memory value
- `category` (string, optional): Category

**Example:**
```
POST /memory?key=phone_john&value=555-1234&category=contacts
```

**Response:**
```json
{
  "message": "Memory saved: phone_john",
  "success": true
}
```

### Get Memory Entry

#### `GET /memory/{key}`

Retrieve memory entry.

**Response:**
```json
{
  "key": "phone_john",
  "value": "555-1234",
  "category": "contacts"
}
```

### List Memories

#### `GET /memory`

List all memories (optional: filter by category).

**Query Parameters:**
- `category` (string, optional): Filter by category

**Response:**
```json
{
  "count": 5,
  "entries": [
    {
      "key": "phone_john",
      "value": "555-1234",
      "category": "contacts"
    }
  ]
}
```

---

## Browser

### Open Browser

#### `POST /browser/open`

Open browser (optional: navigate to URL).

**Query Parameters:**
- `url` (string, optional): Initial URL

**Response:**
```json
{
  "message": "Browser opened",
  "success": true
}
```

### Navigate

#### `POST /browser/navigate`

Navigate to URL.

**Query Parameters:**
- `url` (string): Target URL

**Response:**
```json
{
  "message": "Navigating to https://example.com",
  "success": true
}
```

### Close Browser

#### `POST /browser/close`

Close browser window.

**Response:**
```json
{
  "message": "Browser closed",
  "success": true
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Error description"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

---

## Example Usage

### Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Create task
response = requests.post(
    f"{BASE_URL}/tasks",
    json={
        "title": "Learn Python",
        "priority": "high",
        "due_date": "2024-06-10T19:00:00"
    }
)
task = response.json()
print(f"Created task: {task['id']}")

# Get tasks
response = requests.get(f"{BASE_URL}/tasks")
tasks = response.json()
print(f"Total tasks: {tasks['count']}")

# Complete task
response = requests.patch(f"{BASE_URL}/tasks/{task['id']}/complete")
print(response.json()['message'])
```

### JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000";

// Create task
const response = await fetch(`${BASE_URL}/tasks`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    title: "Learn Python",
    priority: "high"
  })
});

const task = await response.json();
console.log(`Created task: ${task.id}`);
```

### cURL

```bash
# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Python",
    "priority": "high"
  }'

# Get tasks
curl http://localhost:8000/tasks

# Execute command
curl -X POST http://localhost:8000/command \
  -H "Content-Type: application/json" \
  -d '{"text": "abrir chrome"}'
```

---

## Running the API Server

```bash
# Activate environment
venv\Scripts\activate

# Run API server
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000

# With auto-reload (development)
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000 --reload
```

Access API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Rate Limiting

Currently no rate limiting. For production, consider implementing:
- Token bucket algorithm
- Per-IP limits
- Per-user limits

---

## Future Enhancements

- JWT authentication
- Rate limiting
- Caching
- WebSocket support
- GraphQL endpoint
- OpenAPI 3.1 compliance
- Request logging
- Metrics/Monitoring

---

For more information, see [README.md](README.md)
