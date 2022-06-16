import enum

class ExceptionType(enum.Enum):
    DB_ERROR = 1
    SERVER_ERROR = 2
    VPN_SERVER_ERROR = 3
    INVALID_DATA = 4

class MyException(Exception):

    def __init__(self, error_msg, type=ExceptionType.SERVER_ERROR):
        self.error_msg = error_msg
        self.type = type
        super().__init__(self.error_msg)
    
    def __str__(self):
        return f'{self.type}: {self.error_msg}'

    



