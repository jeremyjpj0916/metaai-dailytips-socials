provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "metaai_dailytips_socials" {
  filename      = "lambda_function_payload.zip"
  function_name = "metaai-dailytips-socials"
  handler       = "main.lambda_handler"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_execution_role.arn
}

resource "aws_iam_role" "lambda_execution_role" {
  name        = "lambda-execution-role"
  description = "Execution role for Lambda function"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect = "Allow"
      }
    ]
  })
}

resource "aws_api_gateway_rest_api" "metaai_dailytips_socials" {
  name        = "metaai-dailytips-socials"
  description = "API Gateway for Lambda function"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.metaai_dailytips_socials.id
  parent_id   = aws_api_gateway_rest_api.metaai_dailytips_socials.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.metaai_dailytips_socials.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.metaai_dailytips_socials.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.proxy.http_method
  integration_http_method = "POST"
  type        = "LAMBDA"
  uri         = "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:123456789012:function:metaai-dailytips-socials/invocations"
}

resource "aws_s3_bucket" "metaai_dailytips_socials" {
  bucket = "metaai-dailytips-socials"
  acl    = "private"
}
