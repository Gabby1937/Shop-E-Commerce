# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /project_work

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 8000

# Specify the command to run your Flask app
CMD ["python", "app.py"]