class EthereumNodeResponseError(Exception):
    def __init__(self, message, code, body):
        super().__init__(message)
        self.message = message
        self.code = code
        self.body = body

    def __str__(self):
        return f'Error: {self.message}, {self.code} response: {self.body}'


class EthereumNodeResponseException(EthereumNodeResponseError):
    def __init__(self, params, message, code, data):
        super().__init__(message, code, data)
        self.params = params


class EthereumNodeNoResponse(EthereumNodeResponseError):
    def __init__(self, node_answer=None):
        super().__init__('No response', 500, node_answer)


class EthereumNodeEmptyResponse(EthereumNodeResponseError):
    def __init__(self):
        super().__init__('Empty response', 400, None)


class EthereumNodeInvalidResponse(EthereumNodeResponseError):
    def __init__(self, node_answer):
        super().__init__('Invalid response', 503, node_answer)
