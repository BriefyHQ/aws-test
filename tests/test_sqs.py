"""Test SQS mock."""
from conftest import BaseTest

import boto3


class TestSQS(BaseTest):
    """Testcase for sqs docker container."""

    def get_queue(self):
        """Return a SQS Queue."""
        queue_name = 'foobar'
        sqs = boto3.resource('sqs')
        sqs.create_queue(QueueName=queue_name)
        queue = sqs.get_queue_by_name(QueueName=queue_name)
        # Cleanup messages
        for message in queue.receive_messages(MaxNumberOfMessages=100):
            message.delete()
        return queue

    def test_create_queue(self):
        """Create a queue."""
        queue = self.get_queue()
        assert queue is not None
        assert queue.__class__.__name__ == 'sqs.Queue'

    def test_handle_message(self):
        """Write and read message."""
        from datetime import datetime
        import json
        body = {'hello': 'world'}
        queue = self.get_queue()
        resp = queue.send_message(
            MessageBody=json.dumps(body),
            MessageAttributes={
                'Origin': {'StringValue': 'testcase', 'DataType': 'String'},
                'Author': {'StringValue': 'RideLink', 'DataType': 'String'},
                'CreationDate': {'StringValue': str(datetime.now()), 'DataType': 'String'}
            }
        )
        assert resp is not None
        message_id = resp.get('MessageId').strip()
        assert message_id is not None
        messages = queue.receive_messages(MaxNumberOfMessages=100)

        assert isinstance(messages, list)
        assert len(messages) == 1

        message = messages[0]
        assert json.loads(message.body) == body
