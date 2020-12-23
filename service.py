import datetime
import logging

from errors import *
from manager import wordbase_manager, question_manager
from model.origin import OriginTypeTwoQuestionModel
from model.question import QuestionModel
from model.user import UserModel
from question.ttypes import *


def get_question_list(question_index: int, question_type: int, page: int, page_size: int) -> (list, int):
    if question_index:
        result_question = QuestionModel.objects(index=question_index).first()

        # 要获取的题目不存在
        if not result_question:
            raise QuestionNotExist

        question = Question(
            questionIndex=question_index,
            rawText=result_question['text'],
            keywords=result_question['wordbase']['keywords'] if result_question['q_type'] == 2 else None,
            detailwords=result_question['wordbase']['detailwords'] if result_question['q_type'] == 2 else None,
            feedbackUpCount=result_question['feedback_ups'],
            feedbackDownCount=result_question['feedback_downs'],
            usedTimes=result_question['used_times'],
            type=result_question['q_type'],
            questionId=str(result_question['id'])
        )
        return [question], 1
    else:
        if question_type:
            all_questions_num = len(QuestionModel.objects(q_type=question_type))

            temp_question_query_max = page * page_size
            question_query_max = all_questions_num if temp_question_query_max > all_questions_num \
                else temp_question_query_max
            questions = QuestionModel.objects(q_type=question_type)[
                        ((page - 1) * page_size):question_query_max].order_by('index')
        else:
            all_questions_num = len(QuestionModel.objects())

            temp_question_query_max = page * page_size
            question_query_max = all_questions_num if temp_question_query_max > all_questions_num \
                else temp_question_query_max
            questions = QuestionModel.objects()[((page - 1) * page_size):question_query_max].order_by('index')

        data = []
        for question in questions:
            data.append(Question(
                questionIndex=question['index'],
                rawText=question['text'],
                keywords=question['wordbase']['keywords'] if question['q_type'] == 2 else None,
                detailwords=question['wordbase']['detailwords'] if question['q_type'] == 2 else None,
                feedbackUpCount=question['feedback_ups'],
                feedbackDownCount=question['feedback_downs'],
                usedTimes=question['used_times'],
                type=question['q_type'],
                questionId=str(question['id'])
            ))

        return data, all_questions_num


def generate_wordbase(text: str) -> (list, list):
    wordbase_generator = wordbase_manager.WordbaseGenerator()
    wordbase = wordbase_generator.generate_wordbase(text)
    return wordbase['keywords'], wordbase['detailwords']


def del_question(question_index: int):
    to_delete_question = QuestionModel.objects(index=question_index).first()

    # 要获取的题目不存在
    if not to_delete_question:
        raise QuestionNotExist
    else:
        to_delete_question.delete()


def del_original_question(q_id: int):
    origin_question = OriginTypeTwoQuestionModel.objects(q_id=q_id).first()

    if not origin_question:
        raise QuestionNotExist
    else:
        origin_question.delete()


def save_retelling_question(new_question: Question):
    # modify
    if new_question.questionIndex:
        question = QuestionModel.objects(index=new_question.questionIndex).first()
        if not question:
            raise QuestionNotExist

        # 修改关键词的同时需要重置关键词权重
        wordbase = {
            "keywords": new_question.keywords,
            "detailwords": new_question.detailwords
        }
        question.update(
            text=new_question.rawText,
            wordbase=wordbase,
            weights=wordbase_manager.reset_question_weights(wordbase)
        )
    # add
    else:
        next_q_index = question_manager.get_next_available_question_index()
        logging.info('[save_retelling_question] next_question_index: ' + next_q_index.__str__())

        # 插入 questions，初始化关键词权重 weights
        wordbase = {
            "keywords": new_question.keywords,
            "detailwords": new_question.detailwords
        }
        new_question = QuestionModel(
            q_type=2,
            level=5,
            text=new_question.rawText,
            wordbase=wordbase,
            weights=wordbase_manager.reset_question_weights(wordbase),
            index=next_q_index
        )
        new_question.save()


def save_question_feedback(question_id: str, user_id: str, up: int, down: int, like: int):
    user = UserModel.objects(id=user_id).first()
    question = QuestionModel.objects(id=question_id).first()
    if not question:
        raise QuestionNotExist

    # up
    if up == 1 and down == 0:
        question.feedback_ups += 1
        question.save()
    # cancel up
    elif up == -1 and down == 0:
        question.feedback_ups -= 1
        question.save()
    # down
    elif up == 0 and down == 1:
        question.feedback_downs += 1
        question.save()
    # cancel down
    elif up == 0 and down == -1:
        question.feedback_downs -= 1
        question.save()
    # up to down
    elif up == -1 and down == 1:
        question.feedback_ups -= 1
        question.feedback_downs += 1
        question.save()
    # down to up
    elif up == 1 and down == -1:
        question.feedback_downs -= 1
        question.feedback_ups += 1
        question.save()
    # like
    elif like == 1 and question_id not in user.questions_liked:
        question.feedback_likes += 1
        question.save()
        like_time = datetime.datetime.utcnow()
        user.questions_liked.update({question_id: like_time})
        user.save()
    # cancel like
    elif like == -1 and question_id in user.questions_liked:
        question.feedback_likes -= 1
        question.save()
        user.questions_liked.pop(question_id)
        user.save()
