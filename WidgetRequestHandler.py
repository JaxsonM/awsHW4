import json
import boto3
from botocore.exceptions import ClientError
from jsonschema import validate
from jsonschema.exceptions import ValidationError


# Initialize SQS client
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/792766465280/cs5260-requests'

# Define the JSON schema for validation
widget_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "type": {
      "type": "string",
      "pattern": "WidgetCreateRequest|WidgetDeleteRequest|WidgetUpdateRequest"
    },
    "requestId": {
      "type": "string"
    },
    "widgetId": {
      "type": "string"
    },
    "owner": {
      "type": "string",
      "pattern": "[A-Za-z ]+"
    },
    "label": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "otherAttributes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "value": {
            "type": "string"
          }
        },
        "required": ["name", "value"]
      }
    }
  },
  "required": ["type", "requestId", "widgetId", "owner"]
}

def validate_widget_request(widget_request):
    try:
        validate(instance=widget_request, schema=widget_schema)
    except ValidationError as e:
        return False, str(e)
    return True, None

def lambda_handler(event, context):
    print("entering lambda")
    try:
        if isinstance(event['body'], str):
            print("String")
            try:
                widget_request = json.loads(event['body'])
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format in request body")
        elif isinstance(event['body'], dict):
            widget_request = event['body']
        else:
            raise ValueError("Request body must be a JSON object or string")


        # Validate the widget request
        is_valid, validation_error = validate_widget_request(widget_request)
        print(is_valid)
        if not is_valid:
            raise ValueError(f'Validation failed for the widget request: {validation_error}')
        print("Sending message")
        # Send the valid widget request to the SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(widget_request)
        )
        print("Message sent to queue")

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
    lambda_handler(event, mock_context)
