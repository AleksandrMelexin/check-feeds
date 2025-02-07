class notYMLError(Exception):
    def __init__(self, message):
        super().__init__(message)

class emptyIDError(Exception):
    def __init__(self, message):
        super().__init__(message)
