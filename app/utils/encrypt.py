def encrypt(source_string: str, password: str) -> str:
    """加密函数，与原Java版本保持一致"""
    p = list(password)
    n = len(p)
    c = list(source_string)
    m = len(c)
    
    for k in range(m):
        mima = ord(c[k]) + ord(p[k % n])
        c[k] = chr(mima)
    
    return ''.join(c) 