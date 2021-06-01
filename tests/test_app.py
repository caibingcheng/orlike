import os
import unittest

import pytest


class TestAPP(unittest.TestCase):
    def setUp(self) -> None:
        if "APPID" not in os.environ:
            os.environ["APPID"] = "INVALID APPID"
        if "APPKEY" not in os.environ:
            os.environ["APPKEY"] = "INVALID APPKEY"

    @pytest.mark.skip(reason="block")
    def test_run(self):
        from orlike import app_orlike

        app_orlike.run()

    def test_add_version_to_response(self):
        from orlike.__version__ import __version__
        from orlike.index import add_version_to_response

        response = {}
        add_version_to_response(response)

        assert "version" in response
        assert response["version"] == f"V{__version__}"

    def test_import_version(self):
        import orlike

        print(orlike.__version__)
