export APP_SETTINGS='config.DevelopmentConfig'
gunicorn -b :5000 main:app --timeout=300 --log-level=debug
