from app import create_app
import logging
import os

app = create_app()


def main():
    """Start the Flask development server with an optional simpler log mode.

    Set the environment variable SIMPLE_LOG=1 to reduce built-in Flask/Werkzeug
    debug/reloader messages and print a single clear startup line.
    
    For Railway deployment, PORT environment variable is automatically set.
    """
    # Railway provides PORT, fallback to FLASK_RUN_PORT or default 5000
    port = int(os.environ.get('PORT', os.environ.get('FLASK_RUN_PORT', 5000)))
    # Bind to 0.0.0.0 for Railway (or use FLASK_RUN_HOST if set)
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')

    # Default to clean/simple startup (no reloader/debugger noise).
    # Set VERBOSE=1 in the environment to run in the regular Flask debug mode.
    simple = os.environ.get('SIMPLE_LOG', os.environ.get('VERBOSE', '1')) in ('1', 'true', 'True')

    # Detect the reloader child process to avoid printing startup lines twice
    is_reloader_child = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'

    if simple:
        # Clean mode: reduce noisy log output and run without reloader/debugger
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        logging.getLogger('flask').setLevel(logging.ERROR)
        # Print once (either when not using the reloader, or only in the child process)
        if not is_reloader_child:
            print(f"Backend started successfully — http://{host}:{port}")
        app.run(debug=False, use_reloader=False, host=host, port=port)
    else:
        # Verbose debug mode (developer option). Print a single informative line and
        # allow Flask/Werkzeug to show their usual debug/reloader output.
        if not is_reloader_child:
            print(f"Starting backend in verbose (debug) mode — http://{host}:{port}")
        app.run(debug=True, host=host, port=port)


if __name__ == '__main__':
    main()