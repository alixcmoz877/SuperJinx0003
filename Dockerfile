# ⚡ Super JinX | Marzban on Railway | t.me/Super_Jinx
ARG MARZBAN_TAG=v0.8.4
FROM gozargah/marzban:${MARZBAN_TAG}

RUN apt-get update \
 && apt-get install -y --no-install-recommends nginx ca-certificates \
 && rm -rf /var/lib/apt/lists/* /etc/nginx/sites-enabled/default

WORKDIR /code
COPY config-xray_config.template.json /opt/jinx/config/xray_config.template.json
COPY config-nginx.template.conf /opt/jinx/config/nginx.template.conf
COPY script-start.sh /opt/jinx/scripts/start.sh
COPY script-bootstrap.py /opt/jinx/scripts/bootstrap.py
COPY script-backup.sh /opt/jinx/scripts/backup.sh
COPY script-smoke_test.py /opt/jinx/scripts/smoke_test.py
COPY script-validate_project.py /opt/jinx/scripts/validate_project.py
RUN chmod +x /opt/jinx/scripts/*.sh

ENV UVICORN_HOST=127.0.0.1 \
    UVICORN_PORT=8000 \
    XRAY_JSON=/var/lib/marzban/xray_config.json \
    SQLALCHEMY_DATABASE_URL=sqlite:////var/lib/marzban/db.sqlite3 \
    SUB_PROFILE_TITLE="𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫" \
    SUB_SUPPORT_URL="https://t.me/Super_Jinx" \
    SUB_UPDATE_INTERVAL=6 \
    PYTHONUNBUFFERED=1

EXPOSE 8080
CMD ["/opt/jinx/scripts/start.sh"]
