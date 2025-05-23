from datetime import datetime
from typing import List

import dspy
from scipy.stats import spearmanr


def custom_evaluate(dataset, metric, model, report_result=False, debug=False):
    acc = 0
    cont = 1
    bad_format = 0

    if report_result is True:
        result = []

    print(f"Evaluating: {len(dataset)} examples")

    for item in dataset:
        try:
            pred = model(
                sentence1=item.sentence1,
                sentence2=item.sentence2,
                target_word=item.target_word,
            )
        except Exception as e:
            bad_format += 1

            if report_result is True:
                result.append(None)

            continue

        try:
            int(pred.answer)
        except Exception as e:
            bad_format += 1
            print("bad formaat")

            if report_result is True:
                result.append(None)

            continue

        if pred.answer == item.answer:
            acc += 1

        if report_result is True:
            result.append(pred)

        if debug is True:
            print("Prediction: ", pred.answer)

    print(f"Accurate examples: {acc}")
    print(f"Bad-formatted examples: {bad_format}")

    print(f"Accuracy: {acc * 100 / (len(dataset) - bad_format)}")

    if report_result is True:
        return result


def custom_evaluate_for_spr_lscd(
    dataset: List[dspy.Example],
    model: dspy.Module,
    report_result: bool = False,
    debug: bool = False,
):
    bad_format = 0
    v1, v2 = [], []

    if report_result is True:
        result = []

    print(f"Evaluating: {len(dataset)} examples")

    for item in dataset:
        try:
            pred = model(
                sentence1=item.sentence1,
                sentence2=item.sentence2,
                target_word=item.target_word,
            )
        except Exception as e:
            bad_format += 1

            if report_result is True:
                result.append(None)

            continue

        try:
            int(pred.answer)
        except Exception as e:
            bad_format += 1

            if report_result is True:
                result.append(None)

            continue

        v1.append(item.answer)
        v2.append(pred.answer)

        if report_result is True:
            result.append(pred)

        if debug is True:
            print(f"Prediction: {pred.answer}")

    print(f"Bad-formatted examples: {bad_format}")
    print(f"Spearman correlation: {spearmanr(v1, v2)[0]}")

    if report_result is True:
        return result
