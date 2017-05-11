import web
import json
from pprint import pprint

urls = [
    '/(.*)', 'index',
]

app = web.application(urls, globals())


class index(object):
    def GET(self, info):
        # test_func(name)
        return "Hello", info

    def POST(self, info):
        data = web.input()
        test_func(data)
        return data


def test_func(item):
    # info = json.loads(item)
    pprint(item)
#
if __name__ == '__main__':
    app.run()
