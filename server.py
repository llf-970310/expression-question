import logging

import mongoengine
from config import MongoConfig
from question import QuestionService
from question.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import handler


class QuestionServiceHandler:
    def __init__(self):
        self.log = {}

    def getRetellingQuestion(self, request: GetRetellingQuestionRequest) -> GetRetellingQuestionResponse:
        return handler.get_retelling_question(request)

    def generateWordbase(self, request: GenerateWordbaseRequest) -> GenerateWordbaseResponse:
        return handler.generate_wordbase(request)

    def delQuestion(self, request: DelQuestionRequest) -> DelQuestionResponse:
        return handler.del_question(request)

    def delOriginalQuestion(self, request: DelOriginalQuestionRequest) -> DelOriginalQuestionResponse:
        return handler.del_original_question(request)


if __name__ == '__main__':
    # init mongo
    mongoengine.connect(
        db=MongoConfig.db,
        host=MongoConfig.host,
        port=MongoConfig.port,
        username=MongoConfig.user,
        password=MongoConfig.password
    )

    # init logging
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    # init thrift server
    question_handler = QuestionServiceHandler()
    processor = QuestionService.Processor(question_handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9094)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    server.serve()
