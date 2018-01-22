from flask import Flask, current_app
from bunq.sdk import context
from bunq.sdk.json import converter


def get_connection_settings(config):
    return {
        "sandbox": config.get("BUNQ_API_SANDBOX", True),
        "api_key": config.get("BUNQ_API_KEY"),
        "device_description": config.get("BUNQ_API_IDENTIFIER", "FlaskBunq"),
    }


def create_context(api_key, device_description, sandbox):
    try:
        return context.ApiContext.restore()
    except Exception as e:
        print(e)

    if sandbox:
        environment_type = context.ApiEnvironmentType.SANDBOX
    else:
        environment_type = context.ApiEnvironmentType.PRODUCTION

    from pprint import pprint
    pprint([environment_type, api_key, device_description])
    api_context = context.ApiContext(environment_type, api_key, device_description)
    api_context.save()
    return api_context


class FlaskBunq(object):
    """Wrapper for Bunq SDK"""
    _name = "bunq"

    def __init__(self, app=None, config=None):
        self.app = None

        if app is not None:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        if not app or not isinstance(app, Flask):
            raise Exception('Invalid Flask application instance')

        self.app = app

        app.extensions = getattr(app, 'extensions', {})

        if self._name not in app.extensions:
            app.extensions[self._name] = {}

        if self in app.extensions[self._name]:
            # Raise an exception if extension already initialized as
            # potentially new configuration would not be loaded.
            raise Exception('Extension already initialized')

        if not config:
            # If not passed a config then we read the connection settings
            # from the app config.
            config = app.config

        # Obtain auth and api client connection
        context = create_context(**get_connection_settings(config))

        # Store objects in application instance so that multiple apps do not
        # end up accessing the same objects.
        app.extensions[self._name][self] = {
            'app': app,
            'context': context,
        }

    @property
    def context(self):
        """Return Bunq context instance."""
        return current_app.extensions[self._name][self]['context']
