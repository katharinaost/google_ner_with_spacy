from spacy.language import Language
from spacy.tokens import Doc
from google.cloud import language_v2

@Language.factory("google_ner")
def google_ner(nlp: Language, name: str):
    return GoogleNERComponent(nlp)

class GoogleNERComponent:
    def __init__(self, nlp: Language):
        self.language = nlp.lang
        
    def span_exists(self, span, spans):
        for s in spans:
           if max(s.start, span.start) <= min(s.end, span.end):
               return True
        return False
        
    def __call__(self, doc: Doc) -> Doc:
        spans = []
        client = language_v2.LanguageServiceClient()
        document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT
        document = {
            "content": doc.text,
            "type_": document_type_in_plain_text,
            "language_code": self.language,
        }
        encoding_type = language_v2.EncodingType.UTF32
        response = client.analyze_entities(
            request={"document": document, "encoding_type": encoding_type}
        )
 
        for entity in response.entities:
            for mention in entity.mentions:                
                # Type.UNKNOWN are mostly numbers
                if mention.type_ != mention.Type.COMMON:
                    ent_start = mention.text.begin_offset
                    ent_end = ent_start+len(mention.text.content)
                    span = doc.char_span(ent_start, ent_end, label=language_v2.Entity.Type(entity.type_).name, alignment_mode='expand')
                    # with 'expand' alignment we have to be careful about duplicates
                    if not self.span_exists(span, spans):
                        spans.append(span)
        doc.ents = spans
        return doc