import re
from sklearn.feature_extraction.text import TfidfVectorizer

Code_pattern = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")

def code_tokenizer(code:str):
    return Code_pattern.findall(code)

class CodeTfidVectorizer(TfidfVectorizer):
    def __init__(self,max_features = 500, ngram_range = (1,2), min_df = 1,stop_words = None):
        super().__init__(
            tokenizer=code_tokenizer,
            token_pattern=None,
            lowercase=False,
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            stop_words = stop_words
            )

if __name__ == "__main__":
    vec = CodeTfidVectorizer()
    X = vec.fit_transform([
        'os.system("ping " + host)',
        'cursor.execute("SELECT * FROM users WHERE id = " + uid)',
        'a = 1 + 2'
    ])
    print(vec.get_feature_names_out())