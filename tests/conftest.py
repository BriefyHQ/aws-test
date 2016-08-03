"""Configuration and base mock for tests."""
import botocore.endpoint
import os


class BaseTest:
    """Base test for AWS integration."""

    host = os.environ.get('SVC_IP', '127.0.0.1')
    port = os.environ.get('SVC_PORT', '5000')

    @property
    def endpoint_host(self):
        """Return the base uri for the AWS endpoints."""
        params = {
            'host': self.host,
            'port': self.port,
        }
        return 'http://{host}:{port}'.format(**params)

    def setup_method(self, method):
        """Mock endpoint for this method."""
        endpoint_host = self.endpoint_host

        class MockEndpoint(botocore.endpoint.Endpoint):
            def __init__(self, host, *args, **kwargs):
                super().__init__(endpoint_host, *args, **kwargs)

        botocore.endpoint.Endpoint = MockEndpoint
