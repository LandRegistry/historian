#!/usr/bin/env python
from application.server import app
import os
app.run(host="0.0.0.0", port=int(os.environ['PORT']), debug=True)