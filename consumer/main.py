# consumer/main.py
import asyncio
import logging
import os
from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI

from models import Message

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("consumer")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    app.state.rabbit_conn = await get_connection_with_retry()
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
# 1 - Connection helpers
# -------------------------------------------------------------
async def get_connection_with_retry(
    max_retries: int = 5,
    initial_delay: float = 1.0,
) -> aio_pika.RobustConnection:
    """Return a new RabbitMQ connection with retry logic."""
    url = os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq:5672/%2F")

    for attempt in range(max_retries):
        try:
            return await aio_pika.connect_robust(url=url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = initial_delay * (2**attempt)
            log.warning(f"Connection attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            await asyncio.sleep(delay)


async def get_connection() -> aio_pika.RobustConnection:
    """Return a new RabbitMQ connection."""
    return await get_connection_with_retry()


# -------------------------------------------------------------
# 2 - Message handler
# -------------------------------------------------------------
async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    """Callback executed for every incoming message."""
    payload = Message.model_validate_json(message.body)
    log.info(f"Processing {payload!r}")
    await message.ack()


# -------------------------------------------------------------
# 3  Optional health‑check
# -------------------------------------------------------------
@app.get("/status")
async def status_endpoint() -> dict:
    return {"status": "running"}
