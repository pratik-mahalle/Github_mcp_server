# Use a Python base image that is compatible with AWS Lambda
FROM public.ecr.aws/lambda/python:3.12

# Working directory in the container
WORKDIR /app

# Copy the application code
COPY app.py /app/
COPY utils/ /app/utils/
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install -r requirements.txt --no-cache-dir

# Set the entrypoint for the Lambda function
CMD ["app.webhook_handler"]
