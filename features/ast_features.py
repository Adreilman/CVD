import ast

def extract_features(code:str)->dict:
    features = {
        "sqli_sink_calls": 0,
        "cmd_sink_calls": 0,
        "deser_sink_calls": 0,
        "uses_string_concat": 0,
        "uses_fstring": 0,
        "has_hardcoded_secret_var": 0
    }

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return features
    cmd_sinks = {"system", "popen", "run", "call", "Popen"}
    sql_sinks = {"execute", "executemany"}
    deser_sinks = {
    "pickle.load",
    "pickle.loads",
    "yaml.load"
    }
    secret_var = {
        "password","secret","api_key","api","token","pwd","passwd","apikey","access_key"
    }

    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            if isinstance(node.func, ast.Attribute):
                call_name = node.func.attr

                if isinstance(node.func.value, ast.Name):
                    full_name = f"{node.func.value.id}.{call_name}"
                else : full_name = None
            elif isinstance(node.func,ast.Name):
                call_name = node.func.id
                full_name = call_name
            else:
                call_name = None
                full_name = None
            if call_name in sql_sinks:
                features["sqli_sink_calls"]+=1
            elif call_name in cmd_sinks:
                features["cmd_sink_calls"]+=1
            elif full_name in deser_sinks:
                features["deser_sink_calls"]+=1
            for arg in node.args:
                if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
                    features["uses_string_concat"] += 1
                if isinstance(arg, ast.JoinedStr):
                    features["uses_fstring"] += 1
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name):
                    if target.id.lower() in secret_var:
                         if isinstance(node.value, ast.Constant):
                            if isinstance(node.value.value, str):
                                features["has_hardcoded_secret_var"] += 1
            
    return features
print(extract_features('os.system("ping " + host)'))

print(extract_features(
    'cursor.execute(f"SELECT * FROM users WHERE id={uid}")'
))

print(extract_features('pickle.loads(data)'))
print(extract_features('pickle.dumps(data)'))
print(extract_features('password = "SuperSecret123!"'))
tree = ast.parse('password = "SuperSecret123!"')
node = tree.body[0]
print(type(node.targets))
print(node.targets)
print(extract_features('a = 1 + 2'))
print(extract_features('api_key = os.environ.get("API_KEY")'))
print(extract_features('api_key = "hardcoded_key_123"'))         