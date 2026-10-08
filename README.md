# FastAPI + RabbitMQ Producer/Consumer

A simple asynchronous message queue system using FastAPI, RabbitMQ, and aio-pika. This project demonstrates a producer-consumer pattern where messages are published to a RabbitMQ queue and processed asynchronously by a consumer service.

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Producer  │──────│  RabbitMQ   │──────│  Consumer   │
│  (FastAPI)  │      │   Queue     │      │  (FastAPI)  │
│  Port:8001  │      │  Port:5672  │      │  Port:8002  │
└─────────────┘      └─────────────┘      └─────────────┘
```

- **Producer Service**: HTTP API that accepts messages and publishes them to a RabbitMQ queue
- **Consumer Service**: Listens to the queue and processes incoming messages asynchronously
- **RabbitMQ**: Message broker that handles message queuing and delivery

## Features

- **Async I/O**: Built on FastAPI and aio-pika for high-performance async operations
- **Durable Queues**: Messages persist across RabbitMQ restarts
- **Health Checks**: Both services expose `/status` endpoints
- **RabbitMQ Management UI**: Web interface for monitoring queues and connections
- **Docker Compose**: Single-command setup with health check dependencies
- **Modern FastAPI**: Uses lifespan context managers (not deprecated `on_event`)

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository and navigate to the project directory:
```bash
cd FastAPIRabbitMQ
```

2. Start all services:
```bash
docker-compose up -d
```

3. Verify services are running:
```bash
docker-compose ps
```

You should see three services: `rabbitmq`, `producer`, and `consumer` all with "Up" status.

## Usage

### Publishing Messages

Send a message to the producer API:

```bash
curl -X POST http://localhost:8001/publish \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 42,
    "action": "created",
    "data": {"title": "Hello world"}
  }'
```

Response:
```json
{"msg": "Message queued"}
```

### Verifying Consumer Processing

Check the consumer logs to see messages being processed:

```bash
docker-compose logs consumer --tail 20
```

You should see log entries like:
```
INFO:consumer:Processing Message(user_id=42, action='created', data={'title': 'Hello world'})
```

### Health Checks

Check producer status:
```bash
curl http://localhost:8001/status
```

Check consumer status:
```bash
curl http://localhost:8002/status
```

Both return:
```json
{"status": "running"}
```

## RabbitMQ Management UI

Access the RabbitMQ web interface at:

**http://localhost:15672**

- Username: `guest`
- Password: `guest`

From the UI you can:
- View queue statistics
- Monitor message rates
- Inspect connections and channels
- Manage queues and exchanges

## API Documentation

### Producer API

**POST /publish**

Publish a message to the queue.

**Request Body:**
```json
{
  "user_id": 42,
  "action": "created",
  "data": {"title": "Hello world"}
}
```

**Response:** `202 Accepted`
```json
{"msg": "Message queued"}
```

**GET /status**

Health check endpoint.

**Response:** `200 OK`
```json
{"status": "running"}
```

### Consumer API

**GET /status**

Health check endpoint.

**Response:** `200 OK`
```json
{"status": "running"}
```

## Configuration

Environment variables are configured via `.env` file:

```env
RABBIT_URL=amqp://guest:guest@rabbitmq:5672/%2F
```

## Project Structure

```
FastAPIRabbitMQ/
├── consumer/
│   ├── Dockerfile
│   ├── main.py           # Consumer FastAPI app
│   └── requirements.txt
├── producer/
│   ├── Dockerfile
│   ├── main.py           # Producer FastAPI app
│   └── requirements.txt
├── models.py             # Shared Pydantic model
├── docker-compose.yml    # Service orchestration
├── .env                  # Environment variables
└── README.md
```

## Development

### Running Locally (without Docker)

If you want to run services locally:

1. Install RabbitMQ locally or use the Docker container:
```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

2. Install dependencies:
```bash
cd producer && pip install -r requirements.txt
cd ../consumer && pip install -r requirements.txt
```

3. Update `.env` to use `localhost` instead of `rabbitmq`:
```env
RABBIT_URL=amqp://guest:guest@localhost:5672/%2F
```

4. Run services:
```bash
cd producer && uvicorn main:app --reload --port 8001
cd consumer && uvicorn main:app --reload --port 8002
```

## Stopping Services

```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
```

## Troubleshooting

### Consumer not connecting to RabbitMQ

Check RabbitMQ health:
```bash
docker-compose logs rabbitmq
```

Ensure RabbitMQ is healthy before consumer starts (handled by healthcheck in docker-compose).

### Messages not being processed

Check consumer logs:
```bash
docker-compose logs consumer -f
```

Verify the consumer started successfully and is listening on the queue.

### Port conflicts

If ports 5672, 15672, 8001, or 8002 are already in use, modify the port mappings in `docker-compose.yml`.

## License

MIT
