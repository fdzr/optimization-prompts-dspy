from argparse import ArgumentParser
from datetime import datetime
import random

import pandas as pd
import dspy
from dspy.evaluate import Evaluate
from dspy.teleprompt import MIPROv2
from sklearn.model_selection import train_test_split

from programs import WrapperEnglishSPT, WrapperSpanishSPT, evaluate_answer
from custom_evaluation import custom_evaluate

random.seed(1334)

start_time = datetime.now()

parser = ArgumentParser(description="script to optimize prompts")
parser.add_argument(
    "--port",
    help="ollama port",
)
parser.add_argument(
    "--dataset",
    help="name of the dataset [dev_dwug_en_resampled.csv or dev_dwug_es.csv]",
)

parser.add_argument(
    "--number-items",
    nargs="+",
    help="number of items per class",
)
parser.add_argument(
    "--language-dataset",
    help="en or es",
)
parser.add_argument(
    "--prompt-idiom",
    help="values=[en or es]",
)

args = parser.parse_args()

dataset = args.dataset
language_dataset = args.language_dataset
prompt_idiom = args.prompt_idiom
number_items = list(map(int, args.number_items))


lm = dspy.LM(
    "ollama_chat/deepseek-r1:70b",
    api_base=f"http://localhost:{int(args.port)}",
)
dspy.settings.configure(lm=lm)

program_spt_prompt_with_assertions = None

if prompt_idiom == "en":
    program_spt_prompt_with_assertions = WrapperEnglishSPT().activate_assertions()
else:
    program_spt_prompt_with_assertions = WrapperSpanishSPT().activate_assertions()

name_of_dataset = None

if language_dataset == "en":
    name_of_dataset = "dwug_en"
else:
    name_of_dataset = "dwug_es"


data = pd.read_csv(dataset)
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
        f"non-optimized - {name_of_dataset} - prompt-{prompt_idiom}",
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
        f"compile-models/sp/{language_dataset}_spt_mipro_optimized_prompt_{prompt_idiom}_deepseek-70b-q4-{quantity}-items-per-class"
    )

    program_spt_prompt_with_assertions.load(
        f"compile-models/sp/{language_dataset}_spt_mipro_optimized_prompt_{prompt_idiom}_deepseek-70b-q4-{quantity}-items-per-class"
    )

    custom_evaluate(
        random.choices(classes_1_train, k=quantity)
        + random.choices(classes_2_train, k=quantity)
        + random.choices(classes_3_train, k=quantity)
        + random.choices(classes_4_train, k=quantity),
        program_spt_prompt_with_assertions,
        f"optimized - {name_of_dataset} - prompt-{prompt_idiom}",
        "accuracy-report.txt",
        quantity,
        debug=False,
    )

print(f"ELAPSED TIME: {datetime.now() - start_time}")
