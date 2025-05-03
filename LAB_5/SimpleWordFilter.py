def filter_word(text):
    return text.replace("stupid", "*" * len("stupid"))

input_text = "That was a stupid decision."
filtered_text = filter_word(input_text)
print(filtered_text)
