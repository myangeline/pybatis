
def read_file(name, mode='w', encoding='utf-8'):
    with open(name, mode, encoding=encoding) as handler:
        return handler.read()
