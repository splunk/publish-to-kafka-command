
import import_declare_test

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    SingleModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunktaucclib.rest_handler.admin_external import AdminExternalHandler
import logging

util.remove_http_proxy_env_vars()


fields = [
    field.RestField(
        'bootstrap_servers',
        required=True,
        encrypted=False,
        default=None,
        validator=None
    ), 
    field.RestField(
        'security_protocol',
        required=True,
        encrypted=False,
        default='PLAINTEXT',
        validator=None
    ), 
    field.RestField(
        'sasl_plain_username',
        required=False,
        encrypted=False,
        default=None,
        validator=None
    ), 
    field.RestField(
        'sasl_plain_password',
        required=False,
        encrypted=True,
        default=None,
        validator=None
    )
]
model = RestModel(fields, name=None)


endpoint = SingleModel(
    'publish_to_kafka_environment',
    model,
    config_name='environment'
)


if __name__ == '__main__':
    logging.getLogger().addHandler(logging.NullHandler())
    admin_external.handle(
        endpoint,
        handler=AdminExternalHandler,
    )
