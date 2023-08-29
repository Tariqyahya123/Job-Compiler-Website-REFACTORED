FROM python:3.11.0-alpine


ENV adzuna_app_id=API_ID
ENV adzuna_app_key=APP_KEY
ENV jooble_api_key=API_KEY

WORKDIR /app



# Copy the Django code
COPY . .


RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic

# Make our entrypoint.sh executable
RUN chmod +x config/entrypoint.sh

# Execute our entrypoint.sh file
CMD ["sh","./config/entrypoint.sh"]
