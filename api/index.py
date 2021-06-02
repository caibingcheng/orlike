import os
import sys

root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)

from src.orlike import app_orlike as app

if __name__ == '__main__':
    app.run()