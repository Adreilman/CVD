"""
Generates a small synthetic seed dataset of labeled Python code snippets.

This is NOT a substitute for real data (CVEfixes / GitHub-mined commits).
It exists so the pipeline (features -> model -> eval) can be built and
tested end-to-end before the real dataset is ready. Swap this out later
by dropping a real labeled CSV into data/processed/ with the same schema:
    columns: snippet, label, source
"""
import pandas as pd
import os

samples = []

def add(snippet, label, source="synthetic"):
    samples.append({"snippet": snippet.strip("\n"), "label": label, "source": source})

# ---------------- CWE-89: SQL Injection ----------------
add("""
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()
""", "CWE-89_SQLi")

add("""
def find_order(order_id):
    sql = f"SELECT * FROM orders WHERE id = {order_id}"
    return db.execute(sql).fetchall()
""", "CWE-89_SQLi")

add("""
def login(user, pwd):
    q = "SELECT * FROM accounts WHERE user='%s' AND pwd='%s'" % (user, pwd)
    cursor.execute(q)
""", "CWE-89_SQLi")

add("""
def search_products(term):
    query = "SELECT * FROM products WHERE name LIKE '%" + term + "%'"
    cursor.execute(query)
""", "CWE-89_SQLi")

add("""
def delete_user(uid):
    cursor.execute("DELETE FROM users WHERE id = " + str(uid))
""", "CWE-89_SQLi")

add("""
def update_email(uid, email):
    cursor.execute("UPDATE users SET email='{}' WHERE id={}".format(email, uid))
""", "CWE-89_SQLi")

add("""
def get_comments(post_id):
    query = "SELECT * FROM comments WHERE post_id=" + post_id
    return db.execute(query)
""", "CWE-89_SQLi")

add("""
def raw_filter(table, condition):
    return db.execute(f"SELECT * FROM {table} WHERE {condition}")
""", "CWE-89_SQLi")

# ---------------- CWE-78: OS Command Injection ----------------
add("""
def ping_host(host):
    os.system("ping -c 1 " + host)
""", "CWE-78_CmdInjection")

add("""
def run_backup(filename):
    subprocess.call("tar -cvf backup.tar " + filename, shell=True)
""", "CWE-78_CmdInjection")

add("""
def convert_file(user_path):
    os.popen("convert " + user_path + " out.png")
""", "CWE-78_CmdInjection")

add("""
def resolve_dns(domain):
    result = os.system(f"nslookup {domain}")
    return result
""", "CWE-78_CmdInjection")

add("""
def compress_dir(dirname):
    subprocess.Popen("zip -r out.zip " + dirname, shell=True)
""", "CWE-78_CmdInjection")

add("""
def run_script(script_name):
    os.system("python3 " + script_name)
""", "CWE-78_CmdInjection")

add("""
def user_grep(pattern, filename):
    subprocess.call(f"grep {pattern} {filename}", shell=True)
""", "CWE-78_CmdInjection")

add("""
def cleanup(path):
    os.system("rm -rf " + path)
""", "CWE-78_CmdInjection")

# ---------------- CWE-502: Insecure Deserialization ----------------
add("""
def load_session(data):
    return pickle.loads(data)
""", "CWE-502_InsecureDeser")

add("""
def restore_state(raw_bytes):
    obj = pickle.load(open(raw_bytes, "rb"))
    return obj
""", "CWE-502_InsecureDeser")

add("""
def parse_config(user_input):
    config = eval(user_input)
    return config
""", "CWE-502_InsecureDeser")

add("""
def load_cache(cache_str):
    return yaml.load(cache_str)
""", "CWE-502_InsecureDeser")

add("""
def execute_payload(data):
    exec(data)
""", "CWE-502_InsecureDeser")

add("""
def deserialize_obj(blob):
    return pickle.loads(base64.b64decode(blob))
""", "CWE-502_InsecureDeser")

add("""
def load_user_pref(json_like_str):
    prefs = eval(json_like_str)
    return prefs
""", "CWE-502_InsecureDeser")

add("""
def run_expression(expr):
    result = eval(expr)
    return result
""", "CWE-502_InsecureDeser")

# ---------------- CWE-798: Hardcoded Credentials ----------------
add("""
DB_PASSWORD = "SuperSecret123!"

def connect():
    return mysql.connect(user="admin", password=DB_PASSWORD)
""", "CWE-798_HardcodedCreds")

add("""
API_KEY = "sk_live_51H8s9aKJ2mN..."

def call_api():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    return requests.get(url, headers=headers)
""", "CWE-798_HardcodedCreds")

add("""
def get_admin_token():
    token = "admin-token-9f8e7d6c"
    return token
""", "CWE-798_HardcodedCreds")

add("""
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCY"

def upload_to_s3(file):
    client = boto3.client("s3", aws_secret_access_key=AWS_SECRET)
""", "CWE-798_HardcodedCreds")

add("""
def connect_ftp():
    ftp = FTP("ftp.example.com")
    ftp.login("root", "toor1234")
""", "CWE-798_HardcodedCreds")

add("""
SECRET_KEY = "django-insecure-8x!v9z2n"

def get_secret():
    return SECRET_KEY
""", "CWE-798_HardcodedCreds")

add("""
def smtp_connect():
    server = smtplib.SMTP("smtp.gmail.com")
    server.login("myemail@gmail.com", "mypassword123")
""", "CWE-798_HardcodedCreds")

add("""
JWT_SECRET = "myjwtsecretkey12345"

def sign_token(payload):
    return jwt.encode(payload, JWT_SECRET)
""", "CWE-798_HardcodedCreds")

# ---------------- CWE-79: XSS (in Python web frameworks) ----------------
add("""
def render_comment(comment):
    return f"<div>{comment}</div>"
""", "CWE-79_XSS")

add("""
@app.route("/greet")
def greet():
    name = request.args.get("name")
    return "<h1>Hello " + name + "</h1>"
""", "CWE-79_XSS")

add("""
def build_page(user_bio):
    html = "<p>" + user_bio + "</p>"
    return mark_safe(html)
""", "CWE-79_XSS")

add("""
@app.route("/search")
def search():
    q = request.args.get("q")
    return render_template_string("<p>Results for: " + q + "</p>")
""", "CWE-79_XSS")

add("""
def show_message(msg):
    return HttpResponse("<div class='msg'>" + msg + "</div>")
""", "CWE-79_XSS")

add("""
def profile_page(username):
    return f"<title>{username}'s profile</title>"
""", "CWE-79_XSS")

add("""
def render_error(err_msg):
    return "<span style='color:red'>" + err_msg + "</span>"
""", "CWE-79_XSS")

add("""
def echo_input(user_text):
    return mark_safe("<p>" + user_text + "</p>")
""", "CWE-79_XSS")

# ---------------- Safe code ----------------
add("""
def get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchone()
""", "Safe")

add("""
def ping_host(host):
    if not re.match(r"^[a-zA-Z0-9.-]+$", host):
        raise ValueError("Invalid host")
    subprocess.run(["ping", "-c", "1", host], check=True)
""", "Safe")

add("""
def load_session(data):
    return json.loads(data)
""", "Safe")

add("""
DB_PASSWORD = os.environ.get("DB_PASSWORD")

def connect():
    return mysql.connect(user="admin", password=DB_PASSWORD)
""", "Safe")

add("""
def render_comment(comment):
    return f"<div>{escape(comment)}</div>"
""", "Safe")

add("""
def add_numbers(a, b):
    return a + b
""", "Safe")

add("""
def compute_average(values):
    if not values:
        return 0
    return sum(values) / len(values)
""", "Safe")

add("""
def read_config(path):
    with open(path, "r") as f:
        return json.load(f)
""", "Safe")

add("""
def get_order(order_id):
    sql = "SELECT * FROM orders WHERE id = %s"
    return db.execute(sql, (order_id,)).fetchall()
""", "Safe")

add("""
def resolve_dns(domain):
    if not re.match(r"^[a-zA-Z0-9.-]+$", domain):
        raise ValueError("bad domain")
    return subprocess.run(["nslookup", domain], capture_output=True)
""", "Safe")

add("""
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item, qty=1):
        self.items.append((item, qty))

    def total_items(self):
        return sum(qty for _, qty in self.items)
""", "Safe")

add("""
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
""", "Safe")

os.makedirs("../processed", exist_ok=True)
df = pd.DataFrame(samples)
out_path = os.path.join(os.path.dirname(__file__), "..", "processed", "seed_snippets.csv")
df.to_csv(out_path, index=False)
print(f"Wrote {len(df)} labeled snippets to {out_path}")
print(df["label"].value_counts())