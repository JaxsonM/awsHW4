import json
import pytest
from WidgetRequestHandler import lambda_handler  # Import your Lambda handler

def test_valid_request():
    # Construct a valid event
    event = {
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
    }
    context = {}  # Mock context, if needed
    
    # Call the Lambda handler
    response = lambda_handler(event, context)
    
    # Assert the response is as expected
    assert response['statusCode'] == 200
    assert "Widget request submitted successfully" in response['body']

def test_invalid_request():
    # Construct an invalid event (missing 'type' field)
    event = {
        "body": json.dumps({
            # Incorrect or missing fields
        })
    }
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 400
    assert "Validation failed" in response['body']
