"""Gunicorn configuration file."""
import os
import logging
import sys

# Get port from environment (Railway sets this)
port = os.environ.get('PORT', '8080')
bind_address = f"0.0.0.0:{port}"

# Log the binding address
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)
logger.info(f"Gunicorn will bind to: {bind_address}")
logger.info(f"PORT environment variable: {port}")

# Bind to all interfaces on the port Railway provides
bind = bind_address

# Worker configuration
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "stationary-backend"

def on_starting(server):
    """Called just before the master process is started."""
    logger.info(f"Starting gunicorn server, will bind to {bind_address}")

def when_ready(server):
    """Called just after the server is started."""
    logger.info("=" * 60)
    logger.info("Gunicorn server is READY to accept connections")
    logger.info(f"Listening on: {bind_address}")
    logger.info(f"Worker class: {worker_class}")
    logger.info(f"Workers: {workers}")
    logger.info("=" * 60)

def post_worker_init(worker):
    """Called just after a worker has been forked."""
    logger.info(f"Worker {worker.pid} initialized and ready to accept requests")
    logger.info(f"Worker {worker.pid} is listening on {bind_address}")

def worker_int(worker):
    """Called when a worker receives INT or QUIT signal."""
    logger.warning(f"Worker {worker.pid} received interrupt signal")

def worker_abort(worker):
    """Called when a worker times out."""
    logger.error(f"Worker {worker.pid} timed out!")

def on_exit(server):
    """Called just before exiting."""
    logger.info("Gunicorn server is shutting down")

