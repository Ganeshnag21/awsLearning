import json
import logging

# Configure logger — Lambda captures stdout/stderr to CloudWatch Logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, context) -> dict:
    """
    Entry point for the AWS Lambda function.

    Parameters
    ----------
    event   : dict  – The event data passed by the invoker (API Gateway, etc.)
    context : LambdaContext – Runtime info (function name, request ID, etc.)

    Returns
    -------
    dict – HTTP-style response compatible with API Gateway proxy integration.
    """
    request_id = getattr(context, "aws_request_id", "local-test")

    logger.info(
        "Lambda invoked",
        extra={
            "request_id": request_id,
            "event": event,
        },
    )

    # Log a structured summary so it is easy to find in CloudWatch
    logger.info(
        json.dumps(
            {
                "message": "Lambda function was called",
                "request_id": request_id,
                "http_method": event.get("httpMethod"),
                "path": event.get("path"),
                "query_params": event.get("queryStringParameters"),
            }
        )
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "message": "Hello from Lambda!",
                "request_id": request_id,
            }
        ),
    }
