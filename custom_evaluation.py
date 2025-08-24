from datetime import datetime
from typing import List, Any

import dspy
from scipy.stats import spearmanr
import pandas as pd


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

    acc_reported = None
    try:
        acc_reported = acc * 100 / (len(dataset) - bad_format)
    except Exception as e:
        print("Accurary: 0, all the answers are bad formatted")
        acc_reported = 0

    with open(name_file, "w") as f_out:
        f_out.write(f"Stats for {k} items - {mode_prompt} \n")
        f_out.write(f"  Accuracy: {acc_reported}\n")
        f_out.write(f"  Bad-formatted examples: {bad_format}")
        f_out.write("\n\n")

        f_out.write("=== Inspection History (last 10) ===\n")
        try:
            history_str = str(dspy.inspect_history(10))
            f_out.write(history_str + "\n\n")
        except Exception as e:
            f_out.write(f"Failed to save inspection history: {e}\n\n")

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


def save_results(data: pd.DataFrame, result, set_of_examples, name_file: str):
    reasoning = [item.reasoning if item else None for item in result]
    pred = [item.answer if item else None for item in result]

    annotated_data = pd.DataFrame()

    annotated_data["sentence1"] = data["context_x"].tolist()
    annotated_data["sentence2"] = data["context_y"].tolist()
    annotated_data["gold_label"] = [item.answer for item in set_of_examples]
    annotated_data["prediction"] = pred
    annotated_data["reasoning"] = reasoning
    annotated_data["grouping1"] = data["grouping_x"].tolist()
    annotated_data["grouping2"] = data["grouping_y"].tolist()
    annotated_data["identifier1"] = data["identifier1"].tolist()
    annotated_data["identifier2"] = data["identifier2"].tolist()
    annotated_data["word"] = data["lemma"].tolist()
    annotated_data["judgment"] = data["judgment"].tolist()

    annotated_data.to_csv(f"{name_file}.csv", index=False)
