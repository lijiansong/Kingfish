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
        """Handle POST requests."""
        post_keyword1 = self.get_argument('post_arg1').strip()
        post_keyword2 = self.get_argument('post_arg2').strip()
        post_keyword3 = self.get_argument('post_arg3').strip()
        print("post vars: ", post_keyword1, post_keyword2, post_keyword3)
        keywords = [post_keyword1, post_keyword2, post_keyword3]
        params = {"query": "|".join(keywords)}
        _, results = InferenceApiHanler.predict_app_name(params)
        print(results["names"])
        self.render('result.html',
            keyword1=post_keyword1,
            keyword2=post_keyword2,
            keyword3=post_keyword3,
            infer_result1=results["names"][0],
            infer_result2=results["names"][1],
            infer_result3=results["names"][2],
            infer_result4=results["names"][3],
            infer_result5=results["names"][4],
            infer_result6=results["names"][5],
            infer_result7=results["names"][6],
            infer_result8=results["names"][7],
            infer_result9=results["names"][8],
            infer_result10=results["names"][9],
            )

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
