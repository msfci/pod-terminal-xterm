import os
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
import terminado
import json
import re

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
PORT = 8082


class TerminalPageHandler(RequestHandler):
    def get(self):
        return self.render("termpage.html",  ws_url_path="/terminal")


class TermSocket(terminado.TermSocket):
    def send_json_message(self, content):
        json_msg = json.dumps(content)
        print("Before regex ==> " + json_msg)
        json_msg = re.sub(r'(\\u001b]0;)(.*)(\\u0007)(.+)(\$|#)(.*)', r'\1\2\3\5\6', json_msg)
        print("After regex ==> " + json_msg)
        self.write_message(json_msg)


def main():
    term_manager = terminado.UniqueTermManager(shell_command=['bash'])
    handlers = [
                            (r"/terminal", TermSocket, {'term_manager': term_manager}),
                            (r"/", TerminalPageHandler),
                         ]
    app = Application(handlers, static_path=STATIC_DIR, template_path=TEMPLATE_DIR, debug=True)
    app.listen(PORT, address='0.0.0.0')
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        print(" Shutting down on SIGINT")
    finally:
        term_manager.shutdown()
        IOLoop.current().close()


if __name__ == '__main__':
    main()



