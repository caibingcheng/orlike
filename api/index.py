import os
import sys

root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)

# if "APPID" not in os.environ:
#     os.environ["APPID"] = "INVALID APPID"
# if "APPKEY" not in os.environ:
#     os.environ["APPKEY"] = "INVALID APPKEY"

from src.orlike import app_orlike as app

if __name__ == '__main__':
    app.run()