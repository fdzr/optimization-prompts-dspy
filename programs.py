from typing import Union, Literal, List

import dspy
from dspy.primitives.assertions import assert_transform_module, backtrack_handler
from dspy.predict import Retry
import pandas as pd
from scipy.stats import spearmanr


def check_answer_for_semantic_proximity(answer):
    return int(answer) in [1, 2, 3, 4]


def check_answer_for_wic(answer):
    return answer in [0, 1]


def evaluate_answer(example, pred, trace=None):
    return example.answer == int(pred.answer)


def evaluate_spr_lscd(examples, preds, trace=True):
    y_pred = list(map(lambda x: x.answer, preds))
    y_gold_score = list(map(lambda x: x.answer, examples.examples))

    data = pd.DataFrame({"y_gold_score": y_gold_score, "pred": y_pred})
    data = data.dropna()

    return spearmanr(data["y_gold_score"].tolist(), data["pred"].tolist())[0]


class ScoreEnglishSPT(dspy.Signature):
    """You are a highly trained text data annotation tool capable of
    providing subjective responses. Rate the semantic similarity of the target word in these sentences 1 and 2. Consider
    only the objects/concepts the word forms refer to: ignore any common etymology and
    metaphorical similarity! Ignore case! Ignore number (cat/Cats = identical meaning). Homonyms (like bat the animal vs
    bat in baseball) count as unrelated. Output numeric rating: 1 is unrelated; 2 is distantly
    related; 3 is closely related; 4 is identical meaning. Your response should align with a
    human’s succinct judgment."""

    # fix space between . and Your

    sentence1: str = dspy.InputField()
    sentence2: str = dspy.InputField()
    target_word: str = dspy.InputField()
    answer: Union[int, float] = dspy.OutputField()


class WrapperEnglishSPT(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generate_answer = dspy.ChainOfThought(ScoreEnglishSPT)

    def forward(self, sentence1, sentence2, target_word):
        pred = self.generate_answer(
            sentence1=sentence1,
            sentence2=sentence2,
            target_word=target_word,
        )
        answer = int(pred.answer)
        pred.answer = answer

        if not (1.0 <= answer <= 4.0):
            dspy.Suggest(
                check_answer_for_semantic_proximity(answer),
                "The output shoulb be 1 or 2 or 3 or 4. Please revise accordingly.",  # typo (should)
                target_module=self.generate_answer,
            )
        return pred


program_spt_prompt_en = assert_transform_module(
    WrapperEnglishSPT().map_named_predictors(Retry), backtrack_handler
)


class ScoreSpanishSPT(dspy.Signature):
    """
    Eres una herramienta de anotación de datos textuales altamente entrenada, capaz de proporcionar respuestas
    subjetivas. Evalúa la similitud semántica de la palabra objetivo en estas oraciones 1 y 2. Considera solo los objetos/conceptos
    a los que se refieren las palabras: ¡Ignora cualquier etimología común y similitud metafórica! ¡Ignora mayúsculas!
    ¡Ignora número (gato/Gatos = significado idéntico)! Los homónimos (como murciélago el animal vs murciélago en béisbol)
    se consideran no relacionados. De como salida una calificación numérica: 1 es no relacionado; 2 es lejanamente relacionado; 3 es
    estrechamente relacionado; 4 es significado idéntico. Tu respuesta debe alinearse con el juicio sucinto de un humano.
    """

    sentence1: str = dspy.InputField()
    sentence2: str = dspy.InputField()
    target_word: str = dspy.InputField()
    answer: Union[int, float] = dspy.OutputField()


class WrapperSpanishSPT(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generate_answer = dspy.ChainOfThought(ScoreSpanishSPT)

    def forward(self, sentence1, sentence2, target_word):
        pred = self.generate_answer(
            sentence1=sentence1,
            sentence2=sentence2,
            target_word=target_word,
        )
        answer = int(pred.answer)
        pred.answer = answer

        if not (1.0 <= answer <= 4.0):
            dspy.Suggest(
                check_answer_for_semantic_proximity(answer),
                "La salida deberia ser 1 o 2 o 3 o 4. Por favor, revise en consecuencia.",
                target_module=self.generate_answer,
            )

        return pred


program_spt_prompt_es = assert_transform_module(
    WrapperSpanishSPT().map_named_predictors(Retry), backtrack_handler
)


class ScoreSpanishWiC(dspy.Signature):
    """Dado un par de oraciones y una palabra objetivo, su tarea es clasificar el par de oraciones
    con 1 si el significado de la palabra objetivo es el mismo en ambas oraciones o con 0
    si el significado es completamente diferente."""

    sentence1: str = dspy.InputField()
    sentence2: str = dspy.InputField()
    target_word: str = dspy.InputField()
    answer: Union[Literal["1", "0"], Literal[1, 0]] = dspy.OutputField()


class WrapperSpanishWiC(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generate_answer = dspy.ChainOfThought(ScoreSpanishWiC)

    def forward(self, sentence1, sentence2, target_word):
        pred = self.generate_answer(
            sentence1=sentence1,
            sentence2=sentence2,
            target_word=target_word,
        )
        answer = int(pred.answer)
        pred.answer = answer
        if not (answer == 0 or answer == 1):
            dspy.Suggest(
                check_answer_for_wic(answer),
                "La salida deberia ser 0 o 1. Por favor, revise en consecuencia.",
                target_module=self.generate_answer,
            )

        return pred


program_wic_prompt_es = assert_transform_module(
    WrapperSpanishWiC().map_named_predictors(Retry), backtrack_handler
)


class ScoreEnglishWiC(dspy.Signature):
    """Given a sentence pair and a target word, your task is to classify
    the sentence pair with 1 is the meaning of the target word is the same in both sentences
    or with 0 if the meaning is completely different.
    """

    sentence1: str = dspy.InputField()
    sentence2: str = dspy.InputField()
    target_word: str = dspy.InputField()
    answer: Union[Literal["1", "0"], Literal[1, 0]] = dspy.OutputField()


class WrapperEnglishWiC(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generate_answer = dspy.ChainOfThought(ScoreEnglishWiC)

    def forward(self, sentence1, sentence2, target_word):
        pred = self.generate_answer(
            sentence1=sentence1,
            sentence2=sentence2,
            target_word=target_word,
        )
        answer = int(pred.answer)
        pred.answer = answer
        if not (answer == 0 or answer == 1):
            dspy.Suggest(
                check_answer_for_wic(answer),
                "The output should be 1 or 0. Please revise accordingly.",
                target_module=self.generate_answer,
            )

        return pred


program_wic_prompt_en = assert_transform_module(
    WrapperEnglishWiC().map_named_predictors(Retry), backtrack_handler
)


class WrapperEnglishForSprLSCD(dspy.Module):
    def __init__(self, callbacks=None):
        super().__init__(callbacks)

        self.generate_answer = dspy.ChainOfThought(ScoreEnglishSPT)

    def forward(self, examples: List[dspy.Example]):
        y_pred = []

        for example in examples:
            pred = self.generate_answer(
                sentence1=example.sentence1,
                sentence2=example.sentence2,
                target_word=example.target_word,
            )
            answer = int(pred.answer)
            pred.answer = answer

            if not (1.0 <= answer <= 4.0):
                dspy.Suggest(
                    check_answer_for_semantic_proximity(answer),
                    "The output shoulb be 1 or 2 or 3 or 4. Please revise accordingly.",
                    target_module=self.generate_answer,
                )

            y_pred.append(pred)

        return y_pred


class WrapperSpanishForSprLSCD(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generate_answer = dspy.ChainOfThought(ScoreSpanishSPT)

    def forward(self, examples: List[dspy.Example]):
        y_pred = []

        for example in examples:
            pred = self.generate_answer(
                sentence1=example.sentence1,
                sentence2=example.sentence2,
                target_word=example.target_word,
            )
            answer = int(pred.answer)
            pred.answer = answer

            if not (1.0 <= answer <= 4.0):
                dspy.Suggest(
                    check_answer_for_semantic_proximity(answer),
                    "La salida deberia ser 1 o 2 o 3 o 4. Por favor, revise en consecuencia.",
                    target_module=self.generate_answer,
                )

            y_pred.append(pred)

        return y_pred


class ScoreSpanishWiCCustomize(dspy.Signature):
    """Dado un par de oraciones y una palabra objetivo, su tarea es clasificar el par de oraciones
    con 4 si el significado de la palabra objetivo es el mismo en ambas oraciones o con 1
    si el significado es completamente diferente."""

    sentence1: str = dspy.InputField()
    sentence2: str = dspy.InputField()
    target_word: str = dspy.InputField()
    answer: Literal[1, 4] = dspy.OutputField()


class WrapperSpanishWiCCustomize(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generate_answer = dspy.ChainOfThought(ScoreSpanishWiCCustomize)

    def forward(self, sentence1, sentence2, target_word):
        pred = self.generate_answer(
            sentence1=sentence1,
            sentence2=sentence2,
            target_word=target_word,
        )
        answer = int(pred.answer)
        pred.answer = answer
        if not (answer == 1 or answer == 4):
            dspy.Suggest(
                answer in [1, 4],
                "La salida deberia ser 1 o 4. Por favor, revise en consecuencia.",
                target_module=self.generate_answer,
            )

        return pred


class ScoreEnglishWiCCustomize(dspy.Signature):
    """Given a sentence pair and a target word, your task is to classify
    the sentence pair with 4 is the meaning of the target word is the same in both sentences
    or with 1 if the meaning is completely different.
    """

    sentence1: str = dspy.InputField()
    sentence2: str = dspy.InputField()
    target_word: str = dspy.InputField()
    answer: Literal[1, 4] = dspy.OutputField()


class WrapperEnglishWiCCustomize(dspy.Module):
    def __init__(self):
        super().__init__()

        self.generate_answer = dspy.ChainOfThought(ScoreEnglishWiCCustomize)

    def forward(self, sentence1, sentence2, target_word):
        pred = self.generate_answer(
            sentence1=sentence1,
            sentence2=sentence2,
            target_word=target_word,
        )
        answer = int(pred.answer)
        pred.answer = answer
        if not (answer == 1 or answer == 4):
            dspy.Suggest(
                answer in [1, 4],
                "The output should be 1 or 4. Please revise accordingly.",
                target_module=self.generate_answer,
            )

        return pred
