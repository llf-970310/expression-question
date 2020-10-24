from model.question import QuestionModel


def get_next_available_question_index():
    """获取当前题目 question 中最大的题号

    :return: 当前最大题号
    """
    max_question = QuestionModel.objects(q_type=2).order_by('-index').limit(1).first()
    return max_question['index'] + 1
