# publisher/main.py
import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends
import aio_pika
from models import Message

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    app.state.rabbit_conn = await get_connection()
    yield
    # Shutdown
    await app.state.rabbit_conn.close()

app = FastAPI(title="Publisher Service", lifespan=lifespan)

# -------------------------------------------------------------
# 1 - Connection helpers
# -------------------------------------------------------------
async def get_connection() -> aio_pika.RobustConnection:
    """Return a new RabbitMQ connection (or reuse an existing one)."""
    return await aio_pika.connect_robust(
        url=os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/%2F")
    )

async def get_channel(connection = Depends(get_connection)):
    """Return a channel from the given connection."""
    return await connection.channel()

# -------------------------------------------------------------
# 2 - Endpoint: POST /publish
# -------------------------------------------------------------
@app.post("/publish", status_code=status.HTTP_202_ACCEPTED)
async def publish(
    payload: Message,
    channel = Depends(get_channel),
):
    """
    Accept a payload, publish it to the queue and return immediately.
    """
    queue = await channel.declare_queue("task_queue", durable=True)

    body = json.dumps(payload.model_dump()).encode()

    await channel.default_exchange.publish(
        aio_pika.Message(body=body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
        routing_key=queue.name,
    )

    return {"msg": "Message queued"}

