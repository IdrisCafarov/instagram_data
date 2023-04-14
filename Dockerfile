FROM python:3.9-alpine3.13
LABEL maintainer="idriscafarov.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts

COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update musl-dev && \
    apk add --no-cache linux-headers && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt &&\
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --home /home/django-user \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


# Set ownership of the home directory
# ...
# ...
RUN chown -R django-user:django-user /home/django-user && \
    mkdir -p /tmp && \
    chmod -R 777 /tmp
# ...

# ...

# Install Chromium and its dependencies
RUN apk add --update --no-cache \
        chromium \
        chromium-chromedriver \
        harfbuzz \
        nss \
        freetype \
        ttf-freefont

# Set environment variables for headless Chromium
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/lib/chromium/

ENV PATH="/scripts:/py/bin:$PATH"
USER django-user


CMD ["run.sh"]