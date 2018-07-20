import os
import web

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app = web.application(urls, globals())
    app.run()
