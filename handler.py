import service

from question.ttypes import *
from errors import *
from util import func_log


@func_log
def get_question_list(request: GetQuestionListRequest) -> GetQuestionListResponse:
    resp = GetQuestionListResponse()
    question_index = request.questionIndex
    question_type = request.questionType
    page = request.page
    page_size = request.pageSize

    try:
        question_list, total = service.get_question_list(question_index, question_type, page, page_size)
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


@func_log
def save_question_feedback(request: SaveQuestionFeedbackRequest) -> SaveQuestionFeedbackResponse:
    resp = SaveQuestionFeedbackResponse()
    question_id = request.questionId
    user_id = request.userId
    up = request.upChange if request.upChange else 0
    down = request.downChange if request.downChange else 0
    like = request.likeChange if request.likeChange else 0
    if not user_id or not question_id:
        fill_status_of_resp(resp, InvalidParam())
        return resp

    try:
        service.save_question_feedback(question_id, user_id, up, down, like)
        fill_status_of_resp(resp)
    except ErrorWithCode as e:
        fill_status_of_resp(resp, e)

    return resp
