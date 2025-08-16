from datetime import datetime
from typing import List, Any

import dspy
from scipy.stats import spearmanr


def custom_evaluate(
    dataset: List[dspy.Example],
    model: Any,
    mode_prompt: str,
    name_file: str,
    k: int,
    report_result: bool = False,
    debug: bool = False,
):
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

    try:
        print(f"Accuracy: {acc * 100 / (len(dataset) - bad_format)}")
    except Exception as e:
        print("Accurary: 0, all the answers re bad formatted")

    with open(name_file, "a") as f_out:
        f_out.write(f"Stats for {k} items - {mode_prompt} \n")
        f_out.write(f"  Accuracy: {acc * 100 / (len(dataset) - bad_format)}\n")
        f_out.write(f"  Bad-formatted examples: {bad_format}")
        f_out.write("\n\n")

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
