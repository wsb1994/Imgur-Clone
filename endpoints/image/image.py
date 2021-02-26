import time
import uuid, base64
import json


class image:
    def __init__(self, image, tagline):
        self.image = image
        self.timestamp = int(time.time())
        self.tagline = tagline
        self.uuid = str(uuid.uuid4())

    def __ge__(self, other):
        if self.timestamp <= other.timestamp:
            return True
        else:
            return False

    def __le__(self, other):
        if self.timestamp >= other.timestamp:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.timestamp > other.timestamp:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.timestamp < other.timestamp:
            return True
        else:
            return False
    def select_local_image(self, filename):
        with open(filename, "rb") as image2string: 
            converted_string = base64.b64encode(image2string.read())
            self.image = converted_string
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
