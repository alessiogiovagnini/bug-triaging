from scipy.special import softmax


def predict_assignee(title, body, tokenizer, device, model, labels):
    # Concatenate title and body
    combined_input = title + " " + body  # TODO which works better???
    # combined_input = f"<#TITLE-START#> {title} <#TITLE-END#> <#BODY-START#> {body} <#BODY-END#>"

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

    return ranked_assignees


