# consumer/main.py
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
import aio_pika
from models import Message

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("consumer")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    app.state.rabbit_conn = await get_connection()
    channel = await app.state.rabbit_conn.channel()
    queue = await channel.declare_queue("task_queue", durable=True)
    await queue.consume(process_message)
    app.state.rabbit_channel = channel
    log.info("Consumer started and listening on 'task_queue'")
    yield
    # Shutdown
    await app.state.rabbit_channel.close()
    await app.state.rabbit_conn.close()

app = FastAPI(title="Consumer Service", lifespan=lifespan)

# -------------------------------------------------------------
# 1️⃣  Connection helpers
# -------------------------------------------------------------
async def get_connection() -> aio_pika.RobustConnection:
    """Return a new RabbitMQ connection."""
    return await aio_pika.connect_robust(
        url=os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/%2F")
    )

# -------------------------------------------------------------
# 2️⃣  Message handler
# -------------------------------------------------------------
async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    """Callback executed for every incoming message."""
    payload = Message.model_validate_json(message.body)
    log.info(f"Processing {payload!r}")
    await message.ack()


# -------------------------------------------------------------
# 4️⃣  Optional health‑check
# -------------------------------------------------------------
@app.get("/status")
async def status_endpoint() -> dict:
    return {"status": "running"}
