import logging

class LogMessage(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: "\n" + grey + format + reset + "\n",
        logging.INFO: "\n" + grey + format + reset + "\n",
        logging.WARNING: "\n" + yellow + format + reset + "\n",
        logging.ERROR: "\n" + red + format + reset + "\n",
        logging.CRITICAL: "\n" + bold_red + format + reset + "\n"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)



# create logger
logger = logging.getLogger("ShopOnline")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(LogMessage())
logger.addHandler(ch)