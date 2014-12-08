from wsgiref import simple_server
import pecan
from api import config as api_config

def get_pecan_config():
    # Set up the pecan configuration
    filename = api_config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def setup_app(pecan_config=None):
    if not pecan_config:
        pecan_config = get_pecan_config()
    hooks = []

    app = pecan.make_app(
        pecan_config.app.root,
        debug=True,
        hooks=hooks,
        force_canonical=getattr(pecan_config.app, 'force_canonical', True),
        guess_content_type_from_ext=False
    )

    return app

def start():
    host = "0.0.0.0"
    port = 8080
    api_root = setup_app()
    srv = simple_server.make_server(host, port, api_root)
    srv.serve_forever()

if __name__ == '__main__':
    start()
