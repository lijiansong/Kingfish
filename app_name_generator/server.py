#-*- coding: utf-8 -*-

import os
import sys
import signal
import time
import json
from tornado import httpserver
from tornado import ioloop
from tornado import web
from inference import InferenceApiHanler
from log_util import g_log_inst as logger


MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 0.5


class MainHandler(web.RequestHandler):
    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def get(self):
        self.render("index.html")

    def post(self):
        '''
        Handle POST requests.
        '''
        post_keyword1 = self.get_argument('post_arg1')
        post_keyword2 = self.get_argument('post_arg1')
        post_keyword3 = self.get_argument('post_arg1')
        print("post var: ", post_keyword1, post_keyword2, post_keyword3)

        # Get the "Back" link.
        back_link = self.get_template_path()
        print(back_link)
        #back_link = self.path if self.path.find('?') < 0 else self.path[:self.path.find('?')]
        # Tell the browser everything is OK and that there is HTML page to display.
        #self.write('OK')
        self.set_header('Content-type', 'text/html')
        # display the POST keywords

        self.write('<html>')
        self.write('  <head>')
        self.write('    <title>Server POST Response</title>')
        self.write('  </head>')
        self.write('  <body>')
        self.write('    <p>POST variables 3.</p>')

        self.write('    <table>')
        self.write('      <tbody>')
        i = 0
        for val in sorted([post_keyword1, post_keyword2, post_keyword3]):
            i += 1
            self.write('        <tr>')
            self.write('          <td align="right">%d</td>' % (i))
            self.write('          <td align="right">%result 1:</td>')
            self.write('          <td align="left">%s</td>' % val)
            self.write('        </tr>')
        self.write('      </tbody>')
        self.write('    </table>')

        #self.write('    <p><a href="%s">Back</a></p>' % (back))
        self.write('  </body>')
        self.write('</html>')



class AppNameRecommandHandler(web.RequestHandler):
    def get(self):
        # Parse query params
        params = {}
        required_keys = ["query"]
        optional_keys = {"size": 10,}
        for key in required_keys:
            value = self.get_query_argument(key)
            params[key] = value
        for k, v in optional_keys.items():
            value = self.get_query_argument(k, v)
            params[k] = value
        # Process request
        (status, rsp) = InferenceApiHanler.predict_app_name(params)
        if 200 == status:
            self.set_header("content-type", "application/json")
            self.finish(rsp)
        else:
            self.set_status(404)
            self.finish()


def signal_handler(sig, frame):
    logger.get().warn("Caught signal: %s", sig)
    ioloop.IOLoop.instance().add_callback_from_signal(shutdown)


def shutdown():
    logger.get().info("begin to stop http server ...")
    server.stop()

    logger.get().info("shutdown in %s seconds ...", MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = ioloop.IOLoop.instance()
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logger.get().info("shutdown finished")
    stop_loop()


def main():
    try:
        log_path = "log/search.log"
        logger.start(log_path, name = __name__, level = "DEBUG")

        if False == InferenceApiHanler.init():
            logger.get().warn("init failed, quit now")
            return 1

        app_inst = web.Application([
            (r"/", MainHandler),
            (r"/get_app_name", AppNameRecommandHandler),
            ],
            compress_response=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            )

        global server
        port = 80
        server = httpserver.HTTPServer(app_inst)
        server.listen(port)

        ## install signal handler, for gracefully shutdown
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        logger.get().info("server start, port=%s" % (port))
        ioloop.IOLoop.instance().start()
    except Exception as e:
        raise


if "__main__" == __name__:
    main()
