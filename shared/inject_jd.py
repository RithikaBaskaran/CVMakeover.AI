import json

with open("shared/jd.example.txt", "r", encoding="utf-8") as f:
    jd = f.read()

with open("shared/test_payload.json", "r", encoding="utf-8") as f:
    data = json.load(f)

data["job_description"] = jd

with open("shared/test_payload.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ job_description successfully injected")
