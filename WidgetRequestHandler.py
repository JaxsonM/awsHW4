import json
import boto3
from botocore.exceptions import ClientError

# Initialize SQS client
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/792766465280/cs5260-requests'

def validate_widget_request(widget_request):
    # Add validation logic based on the JSON schema provided
    # This is a placeholder for the validation code
    # You can use libraries like jsonschema for validation against the schema
    return True  # Assuming validation is successful

# def lambda_handler(event, context):
def lambda_handler():
    try:
        # Parse the JSON body from the event
        # widget_request = json.loads(event['body'])
        with open('widgetRequest.json', 'r') as file:
            widget_request = json.load(file)


        # Validate the widget request
        # if not validate_widget_request(widget_request):
        #     raise ValueError('Validation failed for the widget request.')

        # Send the valid widget request to the SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(widget_request)
        )
        print("made it")
        print(response)

        # Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Widget request submitted successfully',
                'requestId': widget_request['requestId']
            })
        }

    except ValueError as ve:
        # Return a validation error response
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(ve)
            })
        }
    except ClientError as ce:
        # Return an SQS client error response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error sending message to SQS: ' + str(ce)
            })
        }
    except Exception as e:
        # Return a general error response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'An unexpected error occurred: ' + str(e)
            })
        }


if __name__ == "__main__":
    # Simulate an empty event and context
    # mock_event = {}
    # mock_context = {}

    # Call the lambda handler
    lambda_handler()
