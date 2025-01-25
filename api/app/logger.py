import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.propagate = False

handler = logging.FileHandler("logs/oauth2.log")
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
log.addHandler(handler)