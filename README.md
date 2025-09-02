# smart-health-ai-api
A serverless cloud-native platform built with AWS API Gateway, Lambda, and DynamoDB that provides AI-powered personalized health insights and real-time monitoring.
Smart Health AI API Platform

This project is a minimal serverless Smart Health API Platform using AWS SAM.

Prerequisites:
- AWS CLI configured with credentials
- AWS SAM CLI installed
- Python 3.11

To build and deploy:
sam build
sam deploy --guided

After deployment:
- Note the API endpoint from the CloudFormation outputs.
- POST /user/register with JSON {"username":"alice","email":"a@b.com"}
- POST /health/log with JSON {"userId":"<id>","bloodPressureSystolic":120,...}
- GET /health/insights?userId=<id>
