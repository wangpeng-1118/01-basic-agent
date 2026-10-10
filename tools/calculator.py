

def calculate(expression) -> str:
    """
    计算数学表达式

    Args:
        expression:
            数学表达式，例如：
            123 * 456

    Returns:
        计算结果
    """
    try:
        # 测试用eval()
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"calcution fault: {e}"

