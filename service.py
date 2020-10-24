import logging

from errors import *
from manager import wordbase_manager, question_manager
from model.origin import OriginTypeTwoQuestionModel
from model.question import QuestionModel
from question.ttypes import *


def get_retelling_question(question_index: int, page: int, page_size: int) -> (list, int):
    if question_index:
        result_question = QuestionModel.objects(index=question_index).first()

        # 要获取的题目不存在
        if not result_question:
            raise QuestionNotExist

        question = RetellingQuestion(
            questionIndex=question_index,
            rawText=result_question['text'],
            keywords=result_question['wordbase']['keywords'],
            detailwords=result_question['wordbase']['detailwords'],
            feedbackUpCount=result_question['feedback_ups'],
            feedbackDownCount=result_question['feedback_downs'],
            usedTimes=result_question['used_times'],
        )
        return [question], 1
    else:
        all_questions_num = len(QuestionModel.objects(q_type=2))

        temp_question_query_max = page * page_size
        question_query_max = all_questions_num if temp_question_query_max > all_questions_num \
            else temp_question_query_max
        questions = QuestionModel.objects(q_type=2)[((page - 1) * page_size):question_query_max].order_by('index')

        data = []
        for question in questions:
            data.append(RetellingQuestion(
                questionIndex=question['index'],
                rawText=question['text'],
                keywords=question['wordbase']['keywords'],
                detailwords=question['wordbase']['detailwords'],
                feedbackUpCount=question['feedback_ups'],
                feedbackDownCount=question['feedback_downs'],
                usedTimes=question['used_times'],
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


def save_retelling_question(new_question: RetellingQuestion):
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
