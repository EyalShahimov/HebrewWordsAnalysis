# Helper function for hebrew phrases display
def rtl(phrase: str) -> str:
    return phrase[::-1].replace(')', '%').replace('(', ')').replace('%', '(')
