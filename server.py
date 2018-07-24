import json
import logging
import quip
import web

logging.basicConfig(level=logging.DEBUG)

urls = (
    '/new', 'new',
    '/(.*)', 'hello',
)
app = web.application(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'
class new:
    def cors_headers(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    def create_new_from_template(self, access_token, template_thread_id, title, member_ids):
        client = quip.QuipClient(access_token)
        template_json = client.get_thread(template_thread_id)
        template_html = template_json.get("html")

        new_html = template_html.replace("Feedback For Engineers Template", title)
        logging.debug("new_html %s", new_html)
        new_thread_response = client.new_document(new_html, member_ids=member_ids)
        logging.debug("new_thread_response %s", new_thread_response)
        return new_thread_response

    def GET(self):
        access_token = "Qk9NQU1BRmRxVVI=|1563906415|mJ6/zBHv4bECSoxp1AUfrjURmao4JP0ABp97nwvl2ts="
        template_thread_id = "IrdIAvWi0VAp"
        member_ids = ["BOMAEAS9Vni", "dXOAEAtFEvl"]

        self.create_new_from_template(access_token, template_thread_id, member_ids)
        return "ok"

    def OPTIONS(self):
        self.cors_headers()
        return 'ok'

    def POST(self):
        self.cors_headers()

        web_data = json.loads(web.data())
        logging.debug("WEB DATA %s", web_data)
        access_token = web_data.get('access_token')
        template_thread_id = web_data.get('template_thread_id')
        member_ids = web_data.get('member_ids')
        title = web_data.get('title')

        new_document_response = self.create_new_from_template(access_token,
            template_thread_id, title, member_ids)

        web.header('Content-Type', 'application/json')
        return json.dumps({'api_response': new_document_response})

if __name__ == "__main__":
    print('running')
    app.run()
