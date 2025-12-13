import sys
import unittest

from tests.acceptance.test_serve_sentence import ServeTestCase


def wait_for_server_ready(port, timeout=30):
    import socket, time

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.05)
    return False

def run_test_cases():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(ServeTestCase)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    summary = {
        "ran": result.testsRun,
        "failures": [
            {
                "test": str(test),
                "traceback": tb,
            }
            for test, tb in result.failures
        ],
        "errors": [
            {
                "test": str(test),
                "traceback": tb,
            }
            for test, tb in result.errors
        ],
        "skipped": [
            {
                "test": str(test),
                "reason": reason,
            }
            for test, reason in result.skipped
        ],
    }

    print(summary)

    if not result.wasSuccessful():
        sys.exit(1)


def run_tests_with_server():
    if wait_for_server_ready(8980):
        run_test_cases()


if __name__ == "__main__":
    run_tests_with_server()
