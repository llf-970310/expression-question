class ReportConfig(object):
    structure_list = ['sum-aspects', 'aspects', 'example', 'opinion', 'sum']
    logic_list = ['cause-affect', 'transition', 'progressive', 'parallel']

    hit_dict = {
        'sum-aspects': '你在表达时，很好的使用了分层法。分层法是有一种经典的表达方法，也就是我们平时说的总-分结构，它将观点层层剥离，'
                       '是讲述内容更有层次性。自上而下、现总结后具体的表达顺序，能够提前说明你叙述内容之间的逻辑关系，让倾听者对内容做出与你相同的理解。',
        'aspects': '你在交流中，能将内容进行有逻辑的组织。利用分点，将你的观点进行拆分讲解，相信你在平时工作、生活和学习的表达中，也是一名思路清晰，有条理的表达者。',
        'example': '在表达时，合理的使用了举例。例子是表达力必不可少的的元素，它能支撑或强调表达者的观点，增强说服力。',
        'opinion': '在表达时，你能够将自己的观点进行浓缩，用简洁、有力的语言表达自己的观点，让人印象深刻。',
        'sum': '在表达时，你会有意识的在结束进行一个总的回顾，这种前后呼应的表达方式，它能再次强化你的观点，突出内容的重点，加深别人对你的印象。'
               '自下而上的思考，能让你在思考、设计交流内容时，充分完善你的思路，以有效的组织思想的方式，让对方立刻理解你想要表达的信息。'
    }
    not_hit_dict = {
        'sum-aspects': '在表达你的观点，或者进行发言时，你可以适当的使用分层法。分层法是有一种经典的表达方法，'
                       '也就是我们平时说的总-分结构，它将观点层层剥离，是讲述内容更有层次性。',
        'aspects': '在论述复杂话题时，利用分点，将你的观点进行拆分讲解，能让你的表达更清晰。',
        'example': '在表达观点时，你可以适当的使用举例，来证明你的观点。例子是表达力必不可少的的元素，它能支撑或强调表达者的观点，增强说服力。',
        'opinion': '表达中，亮明观点，用简洁、有力的语言表达自己的观点，能够让人印象更深刻。',
        'sum': '当结束活临近话题结尾时，有意识的在结束进行一个总的回顾，这种前后呼应的表达方式，它能再次强化你的观点，突出内容的重点，加深别人对你的印象。'
    }


class MongoConfig:
    host = 'mongo-server.expression.hosts'
    port = 27017
    auth = 'SCRAM-SHA-1'  # auth mechanism, set to None if auth is not needed
    user = ''
    password = ''
    db = ''


class SystemConfig:
    IGNORE_LOGIN_PASSWORD = False
    INVITATION_CODE_LEN = 16
