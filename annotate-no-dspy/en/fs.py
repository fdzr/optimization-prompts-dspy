PROMPT = """
    You are a highly trained text data annotation tool capable of
    providing subjective responses. Rate the semantic similarity of the target word in these sentences 1 and 2. Consider
    only the objects/concepts the word forms refer to: ignore any common etymology and
    metaphorical similarity! Ignore case! Ignore number (cat/Cats = identical meaning). Homonyms (like bat the animal vs
    bat in baseball) count as unrelated. Output numeric rating: 1 is unrelated; 2 is distantly
    related; 3 is closely related; 4 is identical meaning.Your response should align with a
    human’s succinct judgment.
    
    Examples of sentences for each possible annotation:

    Example:
        target word: bank
        first sentence: His parents had left a lot of money in the bank and now it was all Measle's, but a judge had said that 
            Measle was too young to get it.
        second sentence: Sherrell, it is said, was sitting on the bank of the river close by, and as soon as the men had disappeared
            from sight he jumped on board the schooner.
        Score: 1

    Example:
        target word: crossroad
        first sentence: He came to a crossroad and read the signs; to the south, 
            Kenniston, 20 m.
        second sentence: As a result we are at a crossroad; either school integration efforts will
            be abandoned in the South, or they will be pursued in the Nort as well.
        Score: 2

    Example:
        target word: child
        first sentence: He agreed and began practicing his sleight of hand tricks to the great pleasure of some children,
            the same ones, I suspect, who had plagued me when I was a child.
        second sentence: The daylight had long faded; her child lay camly sleeping by her side; a candle was burning dimly
            on the stand.
        Score: 3

    Example:
        target word: eat
        first sentence: Speaking of bread and butter reminds me that we'd better eat ours before the coffee get quite cold.
        second sentence: When the meal was over and they had finished their tea after they ate, Wang the Second took the trusty
            man to his elder brother's gate.
        Score: 4
            
        
    Given the following sentence pair score according the explained, give
    only a numeric value as answer and do not explain why the chosen score:
    
    target word: {target_word}
    first sentence: {sentence1}
    second sentence: {sentence2}
    score:

"""
