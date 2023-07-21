FROM python:3.7.3-stretch

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY . .ls

# Expose port
EXPOSE 8000

# Specify the command to run Django directly
CMD ["/bin/sh", "-c", "python manage.py makemigrations mail_client && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
