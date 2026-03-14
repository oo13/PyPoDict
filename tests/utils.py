#!/usr/bin/python3
'''Test Utilities'''
# Copyright © 2026 OOTA, Masato
# This package is published under MIT License.

import queue
import sys
import threading
import time


class Tests:
    def __init__(self):
        self._tests = []
        self._result_queue = queue.Queue()
    def add(self, f, timeout):
        self._tests.append(( lambda: self._result_queue.put(f()), f.__name__, timeout, ))
        return f
    def __iter__(self):
        return iter(self._tests)
    def has_result(self):
        return not self._result_queue.empty()
    def get_result(self):
        return self._result_queue.get(block=False)


def add_test(tests, timeout=1):
    return lambda f: tests.add(f, timeout)


def run_test(tests, msgout=sys.stdout, verbose=True):
    good = True
    for f, name, timeout in tests:
        # A bug might cause an inifinity loop.
        t = threading.Thread(target=f, name=name, daemon=True)
        t.start()
        t.join(timeout)
        if tests.has_result():
            r = tests.get_result()
            if r is not None:
                msgout.write(f'ERROR: {name}: {r}\n')
                good = False
            else:
                if verbose:
                    msgout.write(f'Good: {name}\n')
        elif t.is_alive():
            # Timeout
            # Python cannot kill a thread, so exit.
            sys.stderr.write(f'FATAL ERROR: {name}: Timeout. Aborting.\n')
            sys.exit(1)
        else:
            msgout.write(f'ERROR: {name}: The test returns no result, maybe raise an exception\n')
            good = False
    return good
