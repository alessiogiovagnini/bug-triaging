import json
from pathlib import Path
from scipy.special import softmax
from src.string_cleaning import clean_markdown_string, remove_emoji
import os

root_dir: Path = Path(os.path.realpath(__file__)).parent.parent

user_commits_path: Path = Path(root_dir, "labels", "label-commits#.json")
user_commits_map: dict[str, int] = {}
with open(user_commits_path) as f:
    user_commits = json.load(f)
    for user in user_commits:
        user_commits_map[user[0]] = user[1]


def predict_assignee(title, body, tokenizer, device, model, labels):
    # Concatenate title and body
    cleaned_title = clean_markdown_string(title)
    cleaned_body = remove_emoji(clean_markdown_string(body))
    combined_input = f"<#TITLE-START#> {cleaned_title} <#TITLE-END#> <#BODY-START#> {cleaned_body} <#BODY-END#>"

    # Tokenize the input
    inputs = tokenizer(combined_input, return_tensors='pt', padding=True, truncation=True, max_length=128)

    # Move input tensors to the correct device
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Get model output
    outputs = model(**inputs)

    # Get logits
    logits = outputs.logits.detach().cpu().numpy()[0]

    # Get probabilities using softmax
    probabilities = softmax(logits)

    # Create a list of (assignee, probability) pairs
    assignee_probs = list(zip(labels, probabilities))

    # Sort by probability in descending order
    ranked_assignees = sorted(assignee_probs, key=lambda x: x[1], reverse=True)

    first_five_assignee = ranked_assignees[:5]  # get first 5 elements

    result: list[dict] = []
    for a in first_five_assignee:
        name = a[0]
        acc = round(a[1].item(), 2) * 100
        tmp = {"name": name, "acc": acc, "commit": user_commits_map.get(name, 0)}
        result.append(tmp)
    return result


