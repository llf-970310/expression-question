from errors import *
from manager import wordbase_manager
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
