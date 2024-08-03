import logging

from flask import Flask

from endpoints.v1.v1_app import V1App
from settings import get_settings

settings = get_settings()


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register_blueprint(V1App(), url_prefix="/v1")

        self.add_url_rule("/healthcheck", methods=["GET"], view_func=self.healthcheck)

        for r in self.url_map.iter_rules():
            self.logger.debug(f"{r.rule} {r.methods}")

    @staticmethod
    def healthcheck():
        return "Success", 200


log_fmt = (
    "%(asctime)s - %(levelname)s - [%(name)s:%(funcName)s:%(lineno)3s] %(message)s"
)
handler = logging.StreamHandler()
if settings.is_prod:
    handler = logging.FileHandler("/var/log/app/app.log")
logging.basicConfig(level=logging.DEBUG, format=log_fmt, handlers=[handler])

app = FlaskApp(__name__)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
