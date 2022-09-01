from collections import defaultdict
from heapq import nlargest
from string import punctuation
from nltk.corpus import stopwords

from nltk.tokenize import sent_tokenize, word_tokenize


class Frequency:
    def __init__(self):
        self.stopwords = set(stopwords.words('english') + list(punctuation))
        self.stopwords.update(['We', 'experience', 'team', 'new', 'etc', 'amp', 'following', 'candidates', 'big', 'background','developing', 'characteristics',  'strong', 'project', 
                    'solution', 'technology', 'knowledge','skill', 'work', 'build', 'will', 'knowledge', 'application','gender', 'identity', 'equal',
                    'opportunity','related','field', 'without', 'regard', 'national', 'origin', 'religion', 'sex', 'race', 'color', 'veteran', 'status','sexual',
                    'orientation','opportunity', 'employer', 'qualified','applicant','skills', 'job', 'summary', 'advanced', 'system', 'applicants', 'receive', 'large', 'best', 'practice', 'problem'
                    ,'processing', 'affirmative', 'action', 'employment', 'consideration', 'receive', 'united', 'state', 'programming', 'computer', 'working', 'saying', 
                    'preferred', 'qualification', 'disability', 'protected', 'structured', 'unstructured', 'problems', 'technical', 'internal', 'external', 'non',
                    'subject', 'matter', 'please', 'apply', 'using', 'dental', 'reasonable', 'accomodation', 'join', 'us', 'tools', 'individuals', 'disabilities'
                    ,'type', 'full', 'wide', 'range', 'duties', 'responsibilities', 'stakeholder', 'you', 'oral', 'written', 'ideal', 'candidate', 'ability', 'qualifications', 'well',
                    'must', 'able', 'unit', 'member', 'posted', 'today', 'service', 'clearance', 'days', 'ago', 'high', 'quality', 'level', 'every', 'use', 'case', 'additional',
                     '!','"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';','<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '.', '|', '}', '~', ',', '`',
                     'customer', 'help', 'role', 'support', 'including', 'understanding', 'A' ,'You',  ','
             ])        
      

    def compute_freq(self, token_sent):
        """
        Compute the frequency of each of word.
        Input: 
        token_sent, a list of sentences already tokenized.
        Output: 
        freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for sent in token_sent:
            for word in sent:
                if word not in self.stopwords:
                    freq[word] += 1
        return freq
    
    def summarize(self, text, n):
        """
        Return a list of n sentences 
        which represent the summary of text
        """
        sents = sent_tokenize(text)
        
        try:
            assert n <= len(sents)
        except AssertionError:
            return ""
        
        token_sent = [word_tokenize(s.lower()) for s in sents]
        self.freq = self.compute_freq(token_sent)
        ranking = defaultdict(int)
        
        for i,sent in enumerate(token_sent):
            for w in sent:
                if w in self.freq:
                    ranking[i] += self.freq[w]
        
        sents_idx = self.rank(ranking, n)
        return [sents[j] for j in sents_idx]
    
    def rank(self, ranking, n):
        """ return the first n sentences with highest ranking """
        return nlargest(n, ranking, key=ranking.get)