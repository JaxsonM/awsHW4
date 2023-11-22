import json
import pytest
from holder import lambda_handler

# A sample correct widget request event as a JSON string
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

# A sample correct widget request event as a dictionary
valid_widget_event_dict = {
    "body": {
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
    }
}

# A sample incorrect widget request
invalid_widget_event = json.dumps({
    "body": json.dumps({
        # Missing required fields
    })
})

def test_lambda_handler_with_valid_string_body():
    event = json.loads(valid_widget_event_string)
    context = {}
    response = lambda_handler(event, context)
    response_body = json.loads(response['body'])
    
    assert response['statusCode'] == 200
    assert response_body['message'] == 'Widget request submitted successfully'
    print("Test with valid string passed: Response ->", response)

def test_lambda_handler_with_valid_dict_body():
    event = valid_widget_event_dict
    context = {}
    response = lambda_handler(event, context)
    response_body = json.loads(response['body'])
    
    assert response['statusCode'] == 200
    assert response_body['message'] == 'Widget request submitted successfully'
    print("Test with valid dictionary passed: Response ->", response)

def test_lambda_handler_with_invalid_body():
    event = json.loads(invalid_widget_event)
    context = {}
    response = lambda_handler(event, context)
    
    assert response['statusCode'] == 400
    print("Test with invalid body passed: Response ->", response)

# def test_lambda_handler_with_non_json_body():
#     event = {"body": "not a json string"}
#     context = {}
#     with pytest.raises(ValueError) as excinfo:
#         lambda_handler(event, context)
#     print(excinfo)
#     print(excinfo.value)
#     assert "Invalid JSON format in request body" in str(excinfo.value)
#     print("Test with non-JSON string passed: Exception ->", excinfo.value)

if __name__ == "__main__":
    pytest.main()
