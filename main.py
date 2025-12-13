import time

from src.application.configuration import start_server_in_background


def main():
    start_server_in_background()
    time.sleep(1000000000)


if __name__ == "__main__":
    main()
