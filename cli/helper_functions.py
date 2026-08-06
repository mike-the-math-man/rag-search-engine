def tokenize(input: str):
    result=input.split()
    if "" in result:
        result.remove("")
    return result