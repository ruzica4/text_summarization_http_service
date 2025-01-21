# Reference: https://github.com/LunaticPrakash/Text-Summarization
import math
import nltk
from nltk.stem import WordNetLemmatizer
import spacy

nltk.download("wordnet")

# Initialize spaCy and NLTK components
nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()


def create_summary_from_given_text(input_text, threshold_multiplier=1.3):
    """
    Summarize the given text using Tf-Idf scoring.
    """
    # Convert the text into a spaCy Doc object
    text_doc = nlp(input_text)

    # Extract sentences from the text
    sentences = list(text_doc.sents)
    total_sentences = len(sentences)

    # Frequency matrix
    freq_matrix = {}
    stop_words = nlp.Defaults.stop_words
    for sent in sentences:
        freq_table = {}
        words = [word.text.lower() for word in sent if word.text.isalnum()]
        for word in words:
            word = lemmatizer.lemmatize(word)
            if word not in stop_words:
                freq_table[word] = freq_table.get(word, 0) + 1
        freq_matrix[sent[:15]] = freq_table

    # Term frequency matrix
    tf_matrix = {
        sent: {word: count / len(freq_table) for word, count in freq_table.items()}
        for sent, freq_table in freq_matrix.items()
    }

    # Number of sentences containing each word
    sent_per_words = {}
    for freq_table in freq_matrix.values():
        for word in freq_table:
            sent_per_words[word] = sent_per_words.get(word, 0) + 1

    # Inverse document frequency matrix
    idf_matrix = {
        sent: {
            word: math.log10(total_sentences / sent_per_words[word])
            for word in freq_table
        }
        for sent, freq_table in freq_matrix.items()
    }

    # Tf-Idf matrix
    tf_idf_matrix = {
        sent: {
            word: tf_matrix[sent][word] * idf_matrix[sent][word] for word in freq_table
        }
        for sent, freq_table in freq_matrix.items()
    }

    # Sentence scores
    sentence_scores = {
        sent: sum(f_table.values()) / len(f_table)
        for sent, f_table in tf_idf_matrix.items()
        if f_table
    }

    # Threshold for important sentences
    avg_score = sum(sentence_scores.values()) / len(sentence_scores)
    threshold = threshold_multiplier * avg_score

    # Create summary
    summary = " ".join(
        sentence.text
        for sentence in sentences
        if sentence[:15] in sentence_scores
        and sentence_scores[sentence[:15]] >= threshold
    )

    return summary
