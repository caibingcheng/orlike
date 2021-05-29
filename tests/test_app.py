import os
import unittest


class TestAPP(unittest.TestCase):
    def test_run(self):
        if "APPID" not in os.environ:
            os.environ["APPID"] = "INVALID APPID"
        if "APPKEY" not in os.environ:
            os.environ["APPKEY"] = "INVALID APPKEY"

        from orlike import app_orlike

        app_orlike.run()
