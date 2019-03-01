from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.options import define, options
import tornado.ioloop
import oml_function as oml
import json
import redis
import os
import settings
import subprocess
import asyncio
import threading


class Index(RequestHandler):
    def get(self):
        self.render("templates/oml_html.html")


class WebSocket(WebSocketHandler):
    clients = set()
    rcon = oml.redis_init()

    def listen_task(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        while True:
            test_message = self.rcon.brpop(settings.redis_queue_name)[1]
            test_message = json.loads(test_message)
            # print(test_message)
            self.write_message(test_message)

    def check_origin(self, origin):
        return True

    def open(self):
        WebSocket.clients.add(self)

    def on_message(self, message):
        print(message)
        self.write_message("get message:" + message)
        if message == 'start':
            WebSocket.spout = subprocess.Popen(
                ['python', '/home/yc/VSCode/Python/oml/src/main.py'])
            listen_thread = threading.Thread(target=self.listen_task)
            listen_thread.setDaemon(True)
            listen_thread.start()
        if message == 'continue':
            WebSocket.spout.send_signal(subprocess.signal.SIGCONT)

        if message == 'stop':
            WebSocket.spout.send_signal(subprocess.signal.SIGSTOP)

    def on_close(self):
        WebSocket.clients.remove(self)


def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }  # 配置静态文件路径
    return tornado.web.Application([
        ('/', Index),
        ('/oml', WebSocket),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8123)
    tornado.ioloop.IOLoop.current().start()
