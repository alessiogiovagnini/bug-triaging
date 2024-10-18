from scipy.special import softmax
from src.string_cleaning import clean_markdown_string, remove_emoji


def predict_assignee(title, body, tokenizer, device, model, labels):
    # Concatenate title and body
    cleaned_title = clean_markdown_string(title)
    cleaned_body = remove_emoji(clean_markdown_string(body))
    # combined_input = title + " " + body  # TODO which works better???
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
        acc = round(a[1].item(), 2)
        tmp = {"name": name, "acc": acc}
        result.append(tmp)
    return result


