from datetime import datetime
import csv
import copy

import pandas as pd
import litellm
litellm.disable_cache()

import dspy

from programs import WrapperSpanishSPT, WrapperEnglishSPT, evaluate_answer
from custom_evaluation import custom_evaluate

import random
from tqdm import tqdm
from fire import Fire
import re

def annotate(port, lm_name, fprompt, ftest, shuffle=False):
    prompt_lang = re.findall(r'_(en|es)_', fprompt)[-1] if fprompt else re.findall(r'_(en|es)', ftest)[-1]
    wrapper_cls = {'en':WrapperEnglishSPT,'es':WrapperSpanishSPT}[prompt_lang]
    print(port, lm_name, fprompt, ftest, wrapper_cls)

    lm = dspy.LM(
        f"ollama_chat/{lm_name}",
        api_base=f"http://localhost:{port}",
        cache=False
    )
    dspy.settings.configure(lm=lm)
    print(lm('who are you?'))
    data = pd.read_csv(ftest)
    examples = []
    
    for _, row in data.iterrows():
        examples.append(
            dspy.Example(
                sentence1=row["context_x"],
                sentence2=row["context_y"],
                target_word=row["lemma"].split("_")[0],
                answer=row["judgment"],
            ).with_inputs("sentence1", "sentence2", "target_word")
        )
    
    program_spt_prompt_en_assertions = wrapper_cls().activate_assertions()
    if fprompt:
        program_spt_prompt_en_assertions.load(fprompt)
    
    if shuffle:
        random.shuffle(examples)
    
    start_time = datetime.now()
    
    result = custom_evaluate(
        tqdm(examples),
        evaluate_answer,
        program_spt_prompt_en_assertions,
        report_result=True,
        debug=False,
    )
#    print(dspy.inspect_history(10)) 
    print(f"Elapsed time: {datetime.now() - start_time}")
    
    reasoning = [item.reasoning if item else None for item in result]
    pred = [item.answer if item else None for item in result]
    
    annotated_data = pd.DataFrame()
    
    annotated_data["sentence1"] = data["context_x"].tolist()
    annotated_data["sentence2"] = data["context_y"].tolist()
    annotated_data["gold_label"] = [item.answer for item in examples]
    annotated_data["prediction"] = pred
    annotated_data["reasoning"] = reasoning
    annotated_data["grouping1"] = data["grouping_x"].tolist()
    annotated_data["grouping2"] = data["grouping_y"].tolist()
    annotated_data["identifier1"] = data["identifier1"].tolist()
    annotated_data["identifier2"] = data["identifier2"].tolist()
    annotated_data["word"] = data["lemma"].tolist()
    annotated_data["judgment"] = data["judgment"].tolist()
    
    annotated_data.to_csv(f"sp-{ftest}-{lm_name}.csv", index=False)


Fire(annotate)
