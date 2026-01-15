def clean_text(text: str) -> str:

    if text is None:
        return ""

    if not isinstance(text, str):
        try:
            text = str(text)
        except:
            return ""

    text = text.replace("\t", " ").replace("\n", " ")

    words = text.split()
    return " ".join(words)
