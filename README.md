# hello-lambda

A minimal AWS Lambda function written in Python.  
When invoked, it **logs the incoming request** to Amazon CloudWatch Logs and returns a `200 OK` JSON response.

---

## Project structure

```
.
├── src/
│   ├── __init__.py
│   └── handler.py          # Lambda entry point
├── tests/
│   ├── __init__.py
│   └── test_handler.py     # Unit tests (pytest)
├── .gitignore
├── pyproject.toml          # pytest config
├── requirements.txt        # Runtime dependencies (empty for stdlib-only code)
├── requirements-dev.txt    # Dev/test dependencies
└── README.md
```

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.12+ |
| pip | latest |
| AWS CLI | v2 |
| AWS account | free tier is sufficient |

---

## Local setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2. Install dev dependencies
pip install -r requirements-dev.txt
```

---

## Run the tests

```bash
pytest
```

Expected output:
```
tests/test_handler.py::TestLambdaHandler::test_body_contains_message      PASSED
tests/test_handler.py::TestLambdaHandler::test_body_contains_request_id   PASSED
tests/test_handler.py::TestLambdaHandler::test_content_type_is_json       PASSED
tests/test_handler.py::TestLambdaHandler::test_logs_invocation            PASSED
tests/test_handler.py::TestLambdaHandler::test_returns_200_for_empty_event PASSED
tests/test_handler.py::TestLambdaHandler::test_returns_200_for_get_request PASSED
```

---

## Deploy manually (one-time, to verify your AWS setup)

### 1. Create the Lambda function in AWS Console

1. Sign in to [AWS Console](https://console.aws.amazon.com/lambda)
2. **Create function** → Author from scratch
3. Name: `hello-lambda`
4. Runtime: **Python 3.12**
5. Architecture: `x86_64`
6. Click **Create function**

### 2. Set the handler

In the function's **Configuration → General configuration**, set:
```
Handler: src.handler.lambda_handler
```

### 3. Build a deployment zip and upload

```bash
# From the project root
pip install -r requirements.txt --target ./package
cd package && zip -r ../deployment-package.zip . && cd ..
zip -g deployment-package.zip -r src/

# Upload via AWS CLI
aws lambda update-function-code \
  --function-name hello-lambda \
  --zip-file fileb://deployment-package.zip
```

### 4. Test in the console

Use the **Test** tab with any JSON payload (e.g. `{}`).  
Open **Monitor → View CloudWatch logs** — you will see the two log lines
emitted by `handler.py`.

---

## View logs in CloudWatch

```bash
# Tail live logs (requires aws cli v2 + jq)
aws logs tail /aws/lambda/hello-lambda --follow
```

---

## What's next — GitHub Actions CD

The next step is adding a `.github/workflows/deploy.yml` workflow that:
1. Runs `pytest` on every push
2. Builds `deployment-package.zip`
3. Calls `aws lambda update-function-code` to deploy automatically

Stay tuned — we'll build that workflow together.
