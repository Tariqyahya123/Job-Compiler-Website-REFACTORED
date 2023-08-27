FROM python:3.11.0-alpine

# Install nginx
RUN apk update && apk add nginx
# Copy our nginx configuration to overwrite nginx defaults
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
# Link nginx logs to container stdout
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

ENV adzuna_app_id=ac3dc425
ENV adzuna_app_key=a77ca4c4cb4816504e4b00af81b49755
ENV jooble_api_key=a1d4f23d-cdc4-46d6-b3fd-7fa40b962731

WORKDIR /app



# Copy the Django code
COPY . .

# Create virtual env (notice the location?)
# Update pip
# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic

# Make our entrypoint.sh executable
RUN chmod +x config/entrypoint.sh

# Execute our entrypoint.sh file
CMD ["sh","./config/entrypoint.sh"]
