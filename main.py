from transport.sanic.configure_sanic import configure_app
from context import Context
from configs.config import ApplicationConfig


def main():
    config = ApplicationConfig()
    context = Context()
    app = configure_app(config, context)

    app.run(
        host=config.sanic.host,
        port=config.sanic.port,
        workers=config.sanic.workers,
        debug=config.sanic.debug,
    )


if __name__ == '__main__':
    main()