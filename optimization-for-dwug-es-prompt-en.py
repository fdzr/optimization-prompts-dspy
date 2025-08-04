from datetime import datetime
import random

import pandas as pd
import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import MIPROv2
from sklearn.model_selection import train_test_split

from programs import WrapperEnglishSPT, evaluate_answer
from custom_evaluation import custom_evaluate

random.seed(1334)

start_time = datetime.now()


lm = dspy.LM(
    "ollama_chat/deepseek-r1:70b",
    api_base="http://localhost:11434",
)
dspy.settings.configure(lm=lm)

program_spt_prompt_with_assertions = WrapperEnglishSPT().activate_assertions()


data = pd.read_csv("dev_dwug_es.csv")
print(data.shape)

training_set = []

for _, row in data.iterrows():
    training_set.append(
        dspy.Example(
            sentence1=row["context_x"],
            sentence2=row["context_y"],
            target_word=row["lemma"],
            answer=int(row["judgment"]),
        ).with_inputs("sentence1", "sentence2", "target_word")
    )

classes_1 = [item for item in training_set if item.answer == 1]
classes_2 = [item for item in training_set if item.answer == 2]
classes_3 = [item for item in training_set if item.answer == 3]
classes_4 = [item for item in training_set if item.answer == 4]

classes_1_train, classes_1_test = train_test_split(
    classes_1,
    test_size=0.2,
    random_state=42,
)
classes_1_train, classes_1_dev = train_test_split(
    classes_1_train,
    test_size=0.25,
    random_state=42,
)


classes_2_train, classes_2_test = train_test_split(
    classes_2,
    test_size=0.2,
    random_state=42,
)
classes_2_train, classes_2_dev = train_test_split(
    classes_2_train,
    test_size=0.25,
    random_state=42,
)


classes_3_train, classes_3_test = train_test_split(
    classes_3,
    test_size=0.2,
    random_state=42,
)
classes_3_train, classes_3_dev = train_test_split(
    classes_3_train,
    test_size=0.25,
    random_state=42,
)


classes_4_train, classes_4_test = train_test_split(
    classes_4,
    test_size=0.2,
    random_state=42,
)
classes_4_train, classes_4_dev = train_test_split(
    classes_4_train,
    test_size=0.25,
    random_state=42,
)

print(len(classes_1_train), len(classes_1_dev), len(classes_1_test))
print(len(classes_2_train), len(classes_2_dev), len(classes_2_test))
print(len(classes_3_train), len(classes_3_dev), len(classes_3_test))
print(len(classes_4_train), len(classes_4_dev), len(classes_4_test))


number_items = [5, 10, 15, 20, 50, 100]

for quantity in number_items:

    random.shuffle(classes_1_train)
    random.shuffle(classes_2_train)
    random.shuffle(classes_3_train)
    random.shuffle(classes_4_train)

    custom_evaluate(
        random.choices(classes_1_train, k=quantity)
        + random.choices(classes_2_train, k=quantity)
        + random.choices(classes_3_train, k=quantity)
        + random.choices(classes_4_train, k=quantity),
        program_spt_prompt_with_assertions,
        "non-optimized - dwug-es - prompt-en",
        "accuracy-report.txt",
        quantity,
        debug=False,
    )

    teleprompter = MIPROv2(
        metric=evaluate_answer,
        task_model=lm,
        num_candidates=10,
        init_temperature=0.7,
        max_bootstrapped_demos=3,
        max_labeled_demos=4,
        verbose=False,
    )

    print("Optimizing program with MIPRO...")
    optimized_program = teleprompter.compile(
        program_spt_prompt_with_assertions.deepcopy(),
        trainset=random.choices(classes_1_train, k=quantity)
        + random.choices(classes_2_train, k=quantity)
        + random.choices(classes_3_train, k=quantity)
        + random.choices(classes_4_train, k=quantity),
        valset=random.choices(classes_1_dev, k=quantity)
        + random.choices(classes_2_dev, k=quantity)
        + random.choices(classes_3_dev, k=quantity)
        + random.choices(classes_4_dev, k=quantity),
        num_trials=15,
        minibatch_size=25,
        minibatch_full_eval_steps=10,
        minibatch=True,
        requires_permission_to_run=False,
    )

    optimized_program.save(
        f"compile-models/sp/es_spt_mipro_optimized_prompt_en_deepseek-70b-q4-{quantity}-items-per-class"
    )

    program_spt_prompt_with_assertions.load(
        f"compile-models/sp/es_spt_mipro_optimized_prompt_en_deepseek-70b-q4-{quantity}-items-per-class"
    )

    custom_evaluate(
        random.choices(classes_1_train, k=quantity)
        + random.choices(classes_2_train, k=quantity)
        + random.choices(classes_3_train, k=quantity)
        + random.choices(classes_4_train, k=quantity),
        program_spt_prompt_with_assertions,
        "optimized - dwug-es - prompt-en",
        "accuracy-report.txt",
        quantity,
        debug=False,
    )

print(f"ELAPSED TIME: {datetime.now() - start_time}")
