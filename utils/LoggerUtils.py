import logging.handlers

def createLogger(fileName, name, **kwargs):
    LOG_FILE = fileName
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler

    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    if "fmt" in kwargs:
        fmt = kwargs["fmt"]

    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter

    logger = logging.getLogger(name)  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(logging.DEBUG)
    return logger
