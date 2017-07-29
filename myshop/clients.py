from imgurpython import ImgurClient
import base64
import requests

class uploadClient(ImgurClient):
    def upload_from_memory(self, memory_data, config=None, anon=True):
        if not config:
            config = dict()

        # read the memory and upload it to imgur api
        contents = memory_data.read()
        b64 = base64.b64encode(contents)
        data = {
            'image': b64,
            'type': 'base64',
        }
        data.update({meta: config[meta] for meta in set(self.allowed_image_fields).intersection(config.keys())})

        return self.make_request('POST', 'upload', data, anon)