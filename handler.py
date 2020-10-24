import service

from question.ttypes import *
from errors import *
from util import func_log


@func_log
def get_retelling_question(request: GetRetellingQuestionRequest) -> GetRetellingQuestionResponse:
    resp = GetRetellingQuestionResponse()
    question_index = request.questionIndex
    page = request.page
    page_size = request.pageSize

    try:
        question_list, total = service.get_retelling_question(question_index, page, page_size)
        resp.questions = question_list
        resp.total = total
        fill_status_of_resp(resp)
    except ErrorWithCode as e:
        fill_status_of_resp(resp, e)

    return resp


@func_log
def generate_wordbase(request: GenerateWordbaseRequest) -> GenerateWordbaseResponse:
    resp = GenerateWordbaseResponse()
    text = request.text

    try:
        keywords, detail_words = service.generate_wordbase(text)
        resp.keywords = keywords
        resp.detailwords = detail_words
        fill_status_of_resp(resp)
    except ErrorWithCode as e:
        fill_status_of_resp(resp, e)

    return resp


@func_log
def del_question(request: DelQuestionRequest) -> DelQuestionResponse:
    resp = DelQuestionResponse()
    question_index = request.questionIndex

    try:
        service.del_question(question_index)
        fill_status_of_resp(resp)
    except ErrorWithCode as e:
        fill_status_of_resp(resp, e)

    return resp


@func_log
def del_original_question(request: DelOriginalQuestionRequest) -> DelOriginalQuestionResponse:
    resp = DelOriginalQuestionResponse()
    q_id = request.id

    try:
        service.del_original_question(q_id)
        fill_status_of_resp(resp)
    except ErrorWithCode as e:
        fill_status_of_resp(resp, e)

    return resp


@func_log
def save_retelling_question(request: SaveRetellingQuestionRequest) -> SaveRetellingQuestionResponse:
    resp = SaveRetellingQuestionResponse()
    new_question = request.newQuestion

    try:
        service.save_retelling_question(new_question)
        fill_status_of_resp(resp)
    except ErrorWithCode as e:
        fill_status_of_resp(resp, e)

    return resp
