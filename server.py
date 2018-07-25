import json
import logging
import quip
import web

logging.basicConfig(level=logging.DEBUG)

urls = (
    '/thread/copy', 'copy_thread',
    '/thread/get', 'get_thread',
    '/(.*)', 'hello',
)
app = web.application(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'


def set_cors_headers():
    web.header('Access-Control-Allow-Origin', '*')
    web.header('Access-Control-Allow-Credentials', 'true')
    web.header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

class get_thread:
    def GET(self):
        set_cors_headers()
        web_input = web.input()
        logging.debug("web_input: %s", web_input)

        access_token = web_input.get('access_token')
        thread_id = web_input.get('thread_id')

        client = quip.QuipClient(access_token)
        thread_json = client.get_thread(thread_id)
        logging.debug("thread_json: %s", thread_json)
        web.header('Content-Type', 'application/json')
        return json.dumps(thread_json)

class copy_thread:

    def create_new_from_template(self, access_token, template_thread_id, title, member_ids):
        client = quip.QuipClient(access_token)

        template_json = client.get_thread(template_thread_id)
        logging.debug("template_json: %s", template_json)

        template_html = template_json.get("html")
        template_title = template_json.get("thread").get("title")

        new_html = template_html.replace(template_title, title)

        new_thread_response = client.new_document(new_html, member_ids=member_ids)
        logging.debug("new_thread_response %s", new_thread_response)
        return new_thread_response

    def OPTIONS(self):
        set_cors_headers()
        return 'ok'

    def POST(self):
        set_cors_headers()

        web_data = json.loads(web.data())
        logging.debug("web_data: %s", web_data)
        access_token = web_data.get('access_token')
        template_thread_id = web_data.get('template_thread_id')
        member_ids = web_data.get('member_ids')
        title = web_data.get('title')

        new_document_response = self.create_new_from_template(access_token,
            template_thread_id, title, member_ids)

        web.header('Content-Type', 'application/json')
        return json.dumps(new_document_response)

if __name__ == "__main__":
    print('running')
    app.run()
