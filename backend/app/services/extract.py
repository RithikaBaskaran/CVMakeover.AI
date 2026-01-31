import re
from typing import List

STOP = set("""
a an the and or to of in for with on at from by as is are be this that you we they
""".split())

def tokenize(text: str) -> List[str]:
  words = re.findall(r"[A-Za-z][A-Za-z\+\#\.]{1,}", text.lower())
  return [w for w in words if w not in STOP and len(w) > 2]

def extract_keywords(jd: str, top_k: int = 30) -> List[str]:
  toks = tokenize(jd)
  freq = {}
  for t in toks:
    freq[t] = freq.get(t, 0) + 1
  # simple frequency ranking
  ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
  return [w for w, _ in ranked[:top_k]]
