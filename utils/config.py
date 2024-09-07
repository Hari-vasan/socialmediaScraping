import json
from dotenv import load_dotenv
import os
import os
import ast

load_dotenv()


import os
import json

config = {
    "global": {
        "CONTACT_UPLOAD": os.getenv("CONTACT_UPLOAD"),
        "log_directory": "logs",
        "log_cleanup_day": 7,
    },
}
