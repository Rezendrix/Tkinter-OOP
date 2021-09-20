from model import Model
from gui_manager import GUI_Event_Handler, StatusCode, GUI_Manager

class Controller:
    def __init__(self):
        self.model = Model()

        '''A dispatch table in Python is basically a dictionary of functions. 
        This concept is not Python-specific, rather quite common in Computer Science.
        A dispatch table is a table of pointers to functions or methods. 
        Dispatch tables are among the most common approaches in OOP to implement late binding'''
        self.dispatch_table = {
            StatusCode.DUMMY_TEST: print,
            StatusCode.LOG_IN: self.model.log_in,
            StatusCode.CLOSE_BROWSER_DRIVER: print,
            StatusCode.DO_SOMETHING: self.model.do_something,
            StatusCode.POS_GENERATED_BIND: self.model.pos_generated_bind,
            StatusCode.CHECK_LOGIN: self.model.check_login}

    def update(self, status_code, *args, **kwargs):
        self.dispatch_table[status_code](*args, **kwargs)
