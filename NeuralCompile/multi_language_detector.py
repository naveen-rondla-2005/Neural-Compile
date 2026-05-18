import re

class UniversalScorer:
    """
    Heuristic-based Code Quality Analyzer for multiple languages using Regex.
    Mimics the logic of the Python AST-based scorer.
    """
    def __init__(self, code, language):
        self.code = code
        self.language = language.lower()
        self.total_lines = len(code.splitlines())
        
        # Statistics
        self.functions = []
        self.classes = []
        self.variables = []
        self.imports = []
        
        # Language-specific patterns
        self.patterns = {
            "javascript": {
                "func": r"(?:function\s+([a-zA-Z_$][\w$]*)|([a-zA-Z_$][\w$]*)\s*=\s*(?:\(.*\)|[\w$]+)\s*=>)",
                "class": r"class\s+([a-zA-Z_$][\w$]*)",
                "var": r"(?:const|let|var)\s+([a-zA-Z_$][\w$]*)",
                "import": r"(?:import\s+.*?\s+from|require\()",
                "naming_func": r"^[a-z][a-zA-Z0-9]*$", # camelCase
                "naming_class": r"^[A-Z][a-zA-Z0-9]*$" # PascalCase
            },
            "typescript": {
                "func": r"(?:function\s+([a-zA-Z_$][\w$]*)|([a-zA-Z_$][\w$]*)\s*=\s*(?:\(.*\)|[\w$]+)\s*=>)",
                "class": r"class\s+([a-zA-Z_$][\w$]*)",
                "var": r"(?:const|let|var)\s+([a-zA-Z_$][\w$]*)",
                "import": r"(?:import\s+.*?\s+from|require\()",
                "naming_func": r"^[a-z][a-zA-Z0-9]*$",
                "naming_class": r"^[A-Z][a-zA-Z0-9]*$"
            },
            "java": {
                "func": r"(?:public|private|protected|static|\s)+\s+[\w<>\d\[\]]+\s+([a-z][\w\d]*)\s*\(",
                "class": r"(?:public\s+)?class\s+([A-Z][\w\d]*)",
                "var": r"(?:[\w<>\d\[\]]+)\s+([a-z][\w\d]*)\s*(?:=|;)",
                "import": r"import\s+([\w\.\*]+);",
                "naming_func": r"^[a-z][a-zA-Z0-9]*$",
                "naming_class": r"^[A-Z][a-zA-Z0-9]*$"
            },
            "cpp": {
                "func": r"(?:[\w<>\d]+\s+)?([a-zA-Z_]\w*)\s*\(.*?\)\s*\{",
                "class": r"(?:class|struct)\s+([a-zA-Z_]\w*)",
                "var": r"(?:[\w<>\d]+\s+)([a-zA-Z_]\w*)\s*(?:=|;)",
                "import": r"#include\s*[<\"].*?[>\"]",
                "naming_func": r"^[a-zA-Z_]\w*$",
                "naming_class": r"^[A-Z]\w*$"
            }
        }
        # Alias for C
        self.patterns["c"] = self.patterns["cpp"]
        self.patterns["c++"] = self.patterns["cpp"]

    def _analyze(self):
        p = self.patterns.get(self.language, self.patterns["javascript"])
        
        # Extract Functions
        func_matches = re.findall(p["func"], self.code)
        self.functions = [m[0] or m[1] for m in func_matches if m[0] or m[1]]
        
        # Extract Classes
        self.classes = re.findall(p["class"], self.code)
        
        # Extract Variables
        self.variables = re.findall(p["var"], self.code)
        
        # Extract Imports
        self.imports = re.findall(p["import"], self.code)

    def calculate_scores(self):
        self._analyze()
        p = self.patterns.get(self.language, self.patterns["javascript"])
        
        # 1. Naming Score (0-20)
        naming_pts = 0
        if self.functions:
            naming_pts += (len([f for f in self.functions if re.match(p["naming_func"], f)]) / len(self.functions)) * 10
        else: naming_pts += 10
            
        if self.classes:
            naming_pts += (len([c for c in self.classes if re.match(p["naming_class"], c)]) / len(self.classes)) * 10
        else: naming_pts += 10
        
        # 2. Structure Score (0-20)
        # Avg lines per function heuristic
        struct_pts = 0
        if self.functions:
            avg_lines = self.total_lines / len(self.functions)
            if avg_lines < 40: struct_pts += 10
            elif avg_lines < 80: struct_pts += 5
        else: struct_pts += 10
        # Check for modularity (having at least one class or multiple functions)
        if len(self.classes) > 0 or len(self.functions) > 1: struct_pts += 10
        else: struct_pts += 5
        
        # 3. Logic Score (0-20)
        # Heuristic: Check for potential depth issues or complex control flow
        logic_pts = 20
        # Deduct for long files without structure
        if self.total_lines > 100 and not self.classes: logic_pts -= 5
        # Check for suspicious patterns like 'goto' or 'var'
        if "javascript" in self.language and "var " in self.code: logic_pts -= 5
        if ("c" in self.language or "cpp" in self.language) and "goto " in self.code: logic_pts -= 10

        # 4. Cleanliness Score (0-20)
        clean_pts = 20
        if not self.imports and self.total_lines > 50: clean_pts -= 5
        # Check for console logs or print statements
        p_count = self.code.count("console.log") + self.code.count("System.out.println") + self.code.count("printf")
        if p_count > 10: clean_pts -= 5

        # 5. Robustness/Quality Score (0-20)
        quality_pts = 20
        # Check for error handling
        if "try" not in self.code and "catch" not in self.code:
            quality_pts -= 10
        # Check for too short variable names
        short_vars = [v for v in self.variables if len(v) < 3 and v not in ['i', 'j', 'k', 'x', 'y']]
        if short_vars: quality_pts -= 5

        res = {
            "naming": round(naming_pts),
            "structure": round(struct_pts),
            "logic": round(logic_pts),
            "cleanliness": round(clean_pts),
            "quality": round(quality_pts)
        }
        res["total"] = sum(res.values())
        return res

def get_language_full_score(code: str, language: str) -> dict:
    """Universal dispatcher for deterministic scoring across languages."""
    scorer = UniversalScorer(code, language)
    return scorer.calculate_scores()
