# Briefy AWS Mock server

Image to mock AWS services for tests using moto

For available options: 

	docker run briefy/aws-test

Example running SQS on port 5000: 

	docker run -d -p 127.0.0.1:5000:5000 briefy/aws-test sqs

This image can be found on:

	https://hub.docker.com/r/briefy/aws-test/
