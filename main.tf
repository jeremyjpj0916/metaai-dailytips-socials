provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "metaai_dailytips_socials" {
  filename      = "tips_generator.zip"
  function_name = "metaai-dailytips-socials"
  handler       = "tips_generator.py"
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

resource "aws_s3_bucket" "metaai_dailytips_socials" {
  bucket = "metaai-dailytips-socials"
  acl    = "private"
}
