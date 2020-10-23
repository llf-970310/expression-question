from mongoengine import *


class OriginTypeTwoQuestionModel(DynamicDocument):
    """
    正常使用的题目 question
    """
    text = StringField(max_length=512)
    wordbase = DictField(default={})
    q_id = IntField(min_value=0)  # 题号，从0开始
    origin = StringField(max_length=512)
    url = StringField(max_length=512)
    up_count = IntField(default=0)
    down_count = IntField(default=0)
    used_times = IntField(default=0)

    meta = {'collection': 'origin_questions'}

    def __str__(self):
        return "{id:%s,text:%s,used_times:%s,wordbase:%s}" % (
            self.id, self.text.__str__(), self.used_times.__str__(), self.wordbase.__str__())
