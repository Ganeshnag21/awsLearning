import json
import unittest
from unittest.mock import MagicMock

from src.handler import lambda_handler


def _make_context(request_id: str = "test-request-id") -> MagicMock:
    """Return a minimal mock that mimics the Lambda context object."""
    ctx = MagicMock()
    ctx.aws_request_id = request_id
    return ctx


class TestLambdaHandler(unittest.TestCase):

    def _invoke(self, event: dict | None = None, request_id: str = "test-id"):
        return lambda_handler(event or {}, _make_context(request_id))

    # ------------------------------------------------------------------ #
    # Status code
    # ------------------------------------------------------------------ #

    def test_returns_200_for_empty_event(self):
        response = self._invoke()
        self.assertEqual(response["statusCode"], 200)

    def test_returns_200_for_get_request(self):
        event = {"httpMethod": "GET", "path": "/hello", "queryStringParameters": None}
        response = self._invoke(event)
        self.assertEqual(response["statusCode"], 200)

    # ------------------------------------------------------------------ #
    # Response body
    # ------------------------------------------------------------------ #

    def test_body_contains_message(self):
        response = self._invoke()
        body = json.loads(response["body"])
        self.assertIn("message", body)
        self.assertEqual(body["message"], "Hello from Lambda!")

    def test_body_contains_request_id(self):
        response = self._invoke(request_id="req-abc-123")
        body = json.loads(response["body"])
        self.assertEqual(body["request_id"], "req-abc-123")

    # ------------------------------------------------------------------ #
    # Headers
    # ------------------------------------------------------------------ #

    def test_content_type_is_json(self):
        response = self._invoke()
        self.assertEqual(response["headers"]["Content-Type"], "application/json")

    # ------------------------------------------------------------------ #
    # Logging
    # ------------------------------------------------------------------ #

    def test_logs_invocation(self, caplog=None):
        """Ensure the handler logs at least one INFO message."""
        import logging

        with self.assertLogs("root", level="INFO") as cm:
            self._invoke()

        self.assertTrue(
            any("Lambda invoked" in line or "Lambda function was called" in line for line in cm.output),
            msg=f"Expected log message not found in: {cm.output}",
        )


if __name__ == "__main__":
    unittest.main()
