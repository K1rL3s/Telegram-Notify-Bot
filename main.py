from src import register_handlers_client, register_handlers_admin
from create_bot import app


if __name__ == '__main__':
    register_handlers_client(app)
    register_handlers_admin(app)
    print("Les gooo")
    app.run()
