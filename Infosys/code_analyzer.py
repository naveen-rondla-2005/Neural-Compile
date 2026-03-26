from code_parser import parse_student_code
from error_detector import code_review
from ai_suggester import get_ai_suggestion


def analyze_code_pipeline(code):

    syntax_result = parse_student_code(code)

    if not syntax_result["success"]:
        return syntax_result["error"]["message"]

    tree = syntax_result["tree"]

    #errors = code_review(tree)

    ai_suggestion = get_ai_suggestion(code)

    return f"""
AI Suggestions:
{ai_suggestion}
"""