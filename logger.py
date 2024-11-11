import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("Password Manager")

if __name__ == "__main__":
    logger.info("This is for testing if run this file")
    logger.debug("This is for testing if run this file")
    logger.warning("This is for testing if run this file")
    logger.error("This is for testing if run this file")
