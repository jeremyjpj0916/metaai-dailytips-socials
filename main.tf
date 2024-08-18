provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "metaai_dailytips_socials" {
  filename      = "tips_generator.zip"
  function_name = "metaai-dailytips-socials"
  handler       = "tips_generator.py"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_execution_role.arn
  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.metaai_dailytips_socials.id
    }
  }
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

resource "aws_iam_policy" "lambda_execution_policy" {
  name        = "lambda-execution-policy"
  description = "Policy for Lambda execution role"

  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
        Effect    = "Allow"
      },
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = aws_s3_bucket.metaai_dailytips_socials.arn
        Effect    = "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_execution_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_execution_policy.arn
}

resource "aws_s3_bucket" "metaai_dailytips_socials" {
  bucket = "metaai-dailytips-socials"
  acl    = "private"
}

resource "aws_s3_bucket_policy" "metaai_dailytips_socials_policy" {
  bucket = aws_s3_bucket.metaai_dailytips_socials.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = aws_s3_bucket.metaai_dailytips_socials.arn
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}
