def goodbye(x, y, z):
    print('goodbye')
    return x * y * z

class MyClass():
    """
    This class has attr - they must be captured too - TBD
    """
    arg_1 = "toto"
    arg_2 = 42

    def __init__(self, arg1, zozo):
        self.arg_1 = arg1
        self.zozo = zozo
    
    def the_answer_to_everything(self):
        return self.arg_2

