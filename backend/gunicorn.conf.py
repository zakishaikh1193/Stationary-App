"""Gunicorn configuration file."""
import os
import logging

# Bind to all interfaces on the port Railway provides
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

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

def post_worker_init(worker):
    """Called just after a worker has been forked."""
    logger = logging.getLogger(__name__)
    logger.info(f"Worker {worker.pid} initialized and ready to accept requests")

def when_ready(server):
    """Called just after the server is started."""
    logger = logging.getLogger(__name__)
    logger.info("Gunicorn server is ready to accept connections")

def on_exit(server):
    """Called just before exiting."""
    logger = logging.getLogger(__name__)
    logger.info("Gunicorn server is shutting down")

