FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv
COPY app/requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir -r /srv/requirements.txt
COPY app /srv/app
RUN find /srv/app -type d -exec chmod 755 {} \; && find /srv/app -type f -exec chmod 644 {} \; \
  && useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 8080
CMD ["python", "-m", "flask", "--app", "app.main:app", "run", "--host=0.0.0.0", "--port=8080"]
