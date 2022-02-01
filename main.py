# Adding server to main project
from asyncio.base_futures import _format_callbacks
from gettext import install
from server import app


# Starting the app with all the files
if __name__ == "__main__":
    app.run()
