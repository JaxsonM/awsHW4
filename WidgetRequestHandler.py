import json
import boto3
from botocore.exceptions import ClientError
import re

# Initialize SQS client
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/792766465280/cs5260-requests'

def validate_widget_request(widget_request):
    # Define the required top-level fields
    required_fields = {"type", "requestId", "widgetId", "owner"}
    # Define the valid types for the type field
    valid_types = {"WidgetCreateRequest", "WidgetDeleteRequest", "WidgetUpdateRequest"}
    # Define the pattern for the owner field
    owner_pattern = "[A-Za-z ]+"

    # Check for required fields
    if not all(field in widget_request for field in required_fields):
        return False, "Missing required field(s)."

    # Check the 'type' field is one of the valid types
    if widget_request['type'] not in valid_types:
        return False, "Invalid type value."

    # Check the 'owner' field matches the pattern
    if not isinstance(widget_request['owner'], str) or not re.match(owner_pattern, widget_request['owner']):
        return False, "Invalid owner value."

    # Validate 'otherAttributes' if present
    if 'otherAttributes' in widget_request:
        if not isinstance(widget_request['otherAttributes'], list):
            return False, "'otherAttributes' must be a list."
        
        for attribute in widget_request['otherAttributes']:
            if not isinstance(attribute, dict):
                return False, "Each item in 'otherAttributes' must be an object."
            if 'name' not in attribute or 'value' not in attribute:
                return False, "Each item in 'otherAttributes' must contain 'name' and 'value'."

    return True, None

def lambda_handler(event, context):
    try:
        # Parse the JSON body from the event
        widget_request = json.loads(event['body']) if isinstance(event['body'], str) else event['body']

        # Validate the widget request
        is_valid, validation_error = validate_widget_request(widget_request)
        if not is_valid:
            raise ValueError(f'Validation failed for the widget request: {validation_error}')

        # Send the valid widget request to the SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(widget_request)
        )

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
    print("MAIN")
    # Simulate an empty event and context
    mock_event = {}
    mock_context = {}
    valid_widget_event_string = json.dumps({
    "body": json.dumps({
        "type": "WidgetCreateRequest",
        "requestId": "req-123456",
        "widgetId": "widget-001",
        "owner": "John Doe",
        "label": "My First Widget",
        "description": "This is a description for my first widget.",
        "otherAttributes": [
            {"name": "color", "value": "blue"},
            {"name": "size", "value": "medium"}
        ]
    })
})
    event = json.loads(valid_widget_event_string)
    # Call the lambda handler
    response = lambda_handler(event, mock_context)
    print(response)
