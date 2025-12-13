import socket
import struct
import os
import sys
import unittest

from tests.acceptance.test_serve_sentence import ServeTestCase

AF_NETLINK = 16
NETLINK_INET_DIAG = 4

SOCK_DIAG_BY_FAMILY = 20

NLM_F_REQUEST = 0x01
NLM_F_DUMP    = 0x300

AF_INET = 2
IPPROTO_TCP = 6

TCP_LISTEN = 10
TCPF_LISTEN = 1 << TCP_LISTEN



def wait_for_server_ready(port):
    nl = socket.socket(
        socket.AF_NETLINK,
        socket.SOCK_RAW,
        NETLINK_INET_DIAG
    )

    nl.bind((os.getpid(), 0))

    sockid = b'\x00' * 48

    req = struct.pack(
        "BBBBI",
        AF_INET,  # family
        IPPROTO_TCP,  # protocol
        0,  # idiag_ext
        0,  # pad
        TCPF_LISTEN  # states
    ) + sockid

    nlmsg_len = 16 + len(req)

    nlmsg = struct.pack(
        "IHHII",
        nlmsg_len,
        SOCK_DIAG_BY_FAMILY,
        NLM_F_REQUEST | NLM_F_DUMP,
        1,  # seq
        0  # pid (kernel)
    ) + req

    nl.send(nlmsg)

    while True:
        data = nl.recv(8192)
        offset = 0

        while offset < len(data):
            nlmsg_len, nlmsg_type, _, _, _ = struct.unpack_from(
                "IHHII", data, offset
            )

            if nlmsg_type == 3:  # NLMSG_DONE
                return 0

            msg = data[offset + 16: offset + nlmsg_len]

            # inet_diag_msg (partial)
            (
                family,
                state,
                _,
                _,
                sport,
                dport,
            ) = struct.unpack_from("BBBBHH", msg, 0)

            if state == TCP_LISTEN:
                port = socket.ntohs(sport)
                print(f"LISTENING on port {port}")

            offset += nlmsg_len


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
    if wait_for_server_ready(8980) == 0:
        run_test_cases()



if __name__ == "__main__":
    run_tests_with_server()
