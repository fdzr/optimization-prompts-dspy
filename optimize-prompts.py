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
    "--train-data",
    help="name of the train dataset [train_en.csv or train_es.csv]",
)
parser.add_argument(
    "--dev-data",
    help="name of the dev dataset [dev_en.csv or dev_es.csv]",
)
parser.add_argument(
    "--number-items-dev-set",
    help="number of items in the dev set",
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

name_train_dataset = args.train_data
name_dev_dataset = args.dev_data
number_items_dev_set = int(args.number_items_dev_set)
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


def make_examples(df: pd.DataFrame):
    return [
        dspy.Example(
            sentence1=row["context_x"],
            sentence2=row["context_y"],
            target_word=row["lemma"],
            answer=int(row["judgment"]),
        ).with_inputs("sentence1", "sentence2", "target_word")
        for _, row in df.iterrows()
    ]


def sample_class_balanced(examples, k):
    if k <= len(examples):
        return random.sample(examples, k)
    else:
        return random.choices(examples, k=k)


def dev_class_balanced(examples, k):
    if len(examples) >= k:
        return examples[:k]
    else:
        return examples + random.choices(examples, k=k - len(examples))


train_data = pd.read_csv(name_train_dataset)
dev_data = pd.read_csv(name_dev_dataset)

print(train_data.shape)
print(dev_data.shape)

training_set = make_examples(train_data)
dev_set = make_examples(dev_data)


classes_train = {i: [ex for ex in training_set if ex.answer == i] for i in [1, 2, 3, 4]}
classes_dev = {i: [ex for ex in dev_set if ex.answer == i] for i in [1, 2, 3, 4]}

print("Train sizes: ", {k: len(v) for k, v in classes_train.items()})
print("Dev sizes: ", {k: len(v) for k, v in classes_dev.items()})

dev_subset = (
    dev_class_balanced(classes_dev[1], number_items_dev_set)
    + dev_class_balanced(classes_dev[2], number_items_dev_set)
    + dev_class_balanced(classes_dev[3], number_items_dev_set)
    + dev_class_balanced(classes_dev[4], number_items_dev_set)
)

for quantity in number_items:

    train_subset = (
        sample_class_balanced(classes_train[1], quantity)
        + sample_class_balanced(classes_train[2], quantity)
        + sample_class_balanced(classes_train[3], quantity)
        + sample_class_balanced(classes_train[4], quantity)
    )

    custom_evaluate(
        train_subset,
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
        trainset=train_subset,
        valset=dev_subset,
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
        train_subset,
        program_spt_prompt_with_assertions,
        f"optimized - {name_of_dataset} - prompt-{prompt_idiom}",
        "accuracy-report.txt",
        quantity,
        debug=False,
    )

print(f"ELAPSED TIME: {datetime.now() - start_time}")
