import logging.handlers

def createLogger(fileName, name, **kwargs):
    LOG_FILE = fileName
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler

    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    if "fmt" in kwargs:
        fmt = kwargs["fmt"]

    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
