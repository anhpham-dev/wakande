class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column



if __name__ == "__main__":
    token = Token(kind="NUMBER", value=25, line=1, column=1)

    print(token)