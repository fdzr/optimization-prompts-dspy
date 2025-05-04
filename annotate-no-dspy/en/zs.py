PROMPT = """
    You are a highly trained text data annotation tool capable of
    providing subjective responses. Rate the semantic similarity of the target word in these sentences 1 and 2. Consider
    only the objects/concepts the word forms refer to: ignore any common etymology and
    metaphorical similarity! Ignore case! Ignore number (cat/Cats = identical meaning). Homonyms (like bat the animal vs
    bat in baseball) count as unrelated. Output numeric rating: 1 is unrelated; 2 is distantly
    related; 3 is closely related; 4 is identical meaning.Your response should align with a
    human’s succinct judgment.

    Given the following sentence pair score according the explained, give
    only a numeric value as answer and do not explain why the chosen score:
    
    first sentence: {sentence1}
    second sentence: {sentence2}
    target word: {target_word}
    score:

"""
