# Google NER with Spacy

A simple spaCy pipeline to perform NER with the Google Language API.

Make sure you have followed the steps at [Quickstart: Setup the Natural Language API](https://cloud.google.com/natural-language/docs/setup).

## Example:

```python
import spacy
import google_ner_with_spacy

text = "Major Zeerleder, gutsbesizzer zu Steinegg in Thurgau, der\n" \
    "seit mer als 20. iaren, unter meinem dache das gastrecht genoss,\n" \
    "kam vor 3. wochen zu mir auf besuch."

nlp = spacy.load("de_core_news_sm", disable = ['ner'])
nlp.add_pipe("google_ner")
doc = nlp(text)

spacy.displacy.serve(doc, style="ent")
```
