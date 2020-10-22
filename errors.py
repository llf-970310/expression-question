class ErrorWithCode(Exception):
    def __init__(self, code=-1, msg=""):
        self.status_code = code
        self.status_msg = msg

    def get_status_code(self):
        return self.status_code

    def get_status_msg(self):
        return self.status_msg


class InvalidParam(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4000, "请求参数错误")


class ExamNotExist(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4001, "测试不存在")


class NoExamTimes(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4004, "没有剩余考试次数")


class QuestionNotExist(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4006, "题目不存在")


class VipExpired(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4008, "评测权限已过期")


class InvalidInvitationCode(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4039, "无效的邀请码")


class AuthenticationFailed(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4301, "账号或密码错误")


class UserNotExist(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4302, "用户不存在")


class UserAlreadyExist(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 4303, "用户已存在")


class InProcessing(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 5104, "正在处理")


class InternalError(ErrorWithCode):
    def __init__(self):
        ErrorWithCode.__init__(self, 6000, "服务内部错误")


def fill_status_of_resp(resp, error: ErrorWithCode = None):
    if error:
        resp.statusCode = error.get_status_code()
        resp.statusMsg = error.get_status_msg()
    else:
        resp.statusCode = 0
        resp.statusMsg = ""
