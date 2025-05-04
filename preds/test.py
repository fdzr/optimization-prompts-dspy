import dspy
lm = 'deepseek-r1:1.5b'
lm = dspy.LM(f"ollama_chat/{lm}", api_base="http://127.0.0.1:8081")
print(lm('who are you?'))
