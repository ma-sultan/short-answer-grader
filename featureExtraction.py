from __future__ import division

from config import *
from align import *
from scipy import spatial
import numpy as np

embeddings = {}

def load_embeddings(file_name):

    embeddings = {}

    input_file = open(file_name, 'r')
    for line in input_file:
        tokens = line.split('\t')
        tokens[-1] = tokens[-1].strip()
        for i in xrange(1, len(tokens)):
            tokens[i] = float(tokens[i])
        embeddings[tokens[0]] = tokens[1:-1]

    return embeddings


def vector_sum(vectors):

    n = len(vectors)
    d = len(vectors[0])

    s = []
    for i in xrange(d):
        s.append(0)
    s = np.array(s)

    for vector in vectors:
        s = s + np.array(vector)

    return list(s)


def cosine_similarity(vector1, vector2):
    return 1 - spatial.distance.cosine(vector1, vector2)


def sts_alignment(sentence1, sentence2,
                  parse_results=None,
                  sentence_for_demoting=None):
                      
    if parse_results == None:
        sentence1_parse_result = parseText(sentence1)
        sentence2_parse_result = parseText(sentence2)
        parse_results = []
        parse_results.append(sentence1_parse_result)
        parse_results.append(sentence2_parse_result)
    else:
        sentence1_parse_result = parse_results[0]
        sentence2_parse_result = parse_results[1]
        

    sentence1_lemmatized = lemmatize(sentence1_parse_result)
    sentence2_lemmatized = lemmatize(sentence2_parse_result)

    lemmas_to_be_demoted = []
    if sentence_for_demoting != None:
        if len(parse_results) == 2:
            sentence_for_demoting_parse_result = \
                                parseText(sentence_for_demoting)
            parse_results.append(sentence_for_demoting_parse_result)
        else:
            sentence_for_demoting_parse_result = parse_results[2]


        sentence_for_demoting_lemmatized = \
                            lemmatize(sentence_for_demoting_parse_result)
    
        sentence_for_demoting_lemmas = \
                        [item[3] for item in sentence_for_demoting_lemmatized]
    
        lemmas_to_be_demoted = \
    			[item.lower() for item in sentence_for_demoting_lemmas \
        					if item.lower() not in stop_words+punctuations]
    
    alignments = align(sentence1, sentence2, 
                       sentence1_parse_result, sentence2_parse_result)[0]
    
    sentence1_lemmas = [item[3] for item in sentence1_lemmatized]
    sentence2_lemmas = [item[3] for item in sentence2_lemmatized]

    sentence1_content_lemmas = \
            [item for item in sentence1_lemmas \
                      if item.lower() not in \
                            stop_words+punctuations+lemmas_to_be_demoted]

    sentence2_content_lemmas = \
            [item for item in sentence2_lemmas \
					if item.lower() not in \
                             stop_words+punctuations+lemmas_to_be_demoted]

    if sentence1_content_lemmas == [] or sentence2_content_lemmas == []:
        return (0, 0, parse_results)
    
    sentence1_aligned_content_word_indexes = \
		[item[0] for item in alignments if \
				sentence1_lemmas[item[0]-1].lower() not in \
                                stop_words+punctuations+lemmas_to_be_demoted]

    sentence2_aligned_content_word_indexes = \
		[item[1] for item in alignments if \
				sentence2_lemmas[item[1]-1].lower() not in \
                                stop_words+punctuations+lemmas_to_be_demoted]
    
    sim_score = (len(sentence1_aligned_content_word_indexes) + \
	             len(sentence2_aligned_content_word_indexes)) / \
                        				(len(sentence1_content_lemmas) + \
                        	              len(sentence2_content_lemmas))

    coverage = len(sentence1_aligned_content_word_indexes) / \
                                           len(sentence1_content_lemmas) 

    return (sim_score, coverage, parse_results)


def sts_cvm(sentence1, sentence2,
            parse_results,
            sentence_for_demoting=None,):

    global embeddings
    
    if embeddings == {}:
        print 'loading embeddings...'
        embeddings = \
           load_embeddings('Resources/EN-wform.w.5.cbow.neg10.400.subsmpl.txt')
        print 'done'    

    sentence1_parse_result = parse_results[0]
    sentence2_parse_result = parse_results[1]
    
    sentence1_lemmatized = lemmatize(sentence1_parse_result)
    sentence2_lemmatized = lemmatize(sentence2_parse_result)

    lemmas_to_be_demoted = []
    if sentence_for_demoting != None:
        sentence_for_demoting_parse_result = parse_results[2]

        sentence_for_demoting_lemmatized = \
                            lemmatize(sentence_for_demoting_parse_result)
    
        sentence_for_demoting_lemmas = \
                        [item[3] for item in sentence_for_demoting_lemmatized]
    
        lemmas_to_be_demoted = \
    			[item.lower() for item in sentence_for_demoting_lemmas \
        					if item.lower() not in stop_words+punctuations]

    sentence1_lemmas = [item[3].lower() for item in sentence1_lemmatized]
    sentence2_lemmas = [item[3].lower() for item in sentence2_lemmatized]

    #sentence1_lemmas[:] = sorted(sentence1_lemmas)
    #sentence2_lemmas[:] = sorted(sentence2_lemmas)
    
    if sentence1_lemmas == sentence2_lemmas:
        return 1

    sentence1_content_lemma_embeddings = []
    for lemma in sentence1_lemmas:
        if lemma.lower() in stop_words+punctuations+lemmas_to_be_demoted:
            continue
        if lemma.lower() in embeddings:
            sentence1_content_lemma_embeddings.append(
                                            embeddings[lemma.lower()])

    
    sentence2_content_lemma_embeddings = []
    for lemma in sentence2_lemmas:
        if lemma.lower() in stop_words+punctuations+lemmas_to_be_demoted:
            continue
        if lemma.lower() in embeddings:
            sentence2_content_lemma_embeddings.append(
                                            embeddings[lemma.lower()])

    if sentence1_content_lemma_embeddings == \
                       sentence2_content_lemma_embeddings:
        return 1
    elif sentence1_content_lemma_embeddings == [] or \
         sentence2_content_lemma_embeddings == []:
        return 0
    
    sentence1_embedding = vector_sum(sentence1_content_lemma_embeddings)
    sentence2_embedding = vector_sum(sentence2_content_lemma_embeddings)
    
    return cosine_similarity(sentence1_embedding, sentence2_embedding)
    
    
def length_ratio(sentence1, sentence2, parse_results):
    
    sentence1_parse_result = parse_results[0]
    sentence2_parse_result = parse_results[1]
        
    sentence1_lemmatized = lemmatize(sentence1_parse_result)
    sentence2_lemmatized = lemmatize(sentence2_parse_result)
    
    sentence1_lemmas = [item[3] for item in sentence1_lemmatized]
    sentence2_lemmas = [item[3] for item in sentence2_lemmatized]

    sentence1_content_lemmas = \
            [item for item in sentence1_lemmas \
                      if item.lower() not in \
                            stop_words+punctuations]

    sentence2_content_lemmas = \
            [item for item in sentence2_lemmas \
					if item.lower() not in \
                             stop_words+punctuations]
    
    if sentence2_content_lemmas == []:
        return len(sentence1_lemmas) / len(sentence2_lemmas)

    return len(sentence1_content_lemmas) / len(sentence2_content_lemmas)
