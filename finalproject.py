#
# name: Tina Wang
# email: twang39@bu.edu
#

import math

# helper functions
def clean_text(txt):
        """ takes a string of text (txt) as a parameter and returns a list containing
            the words in txt after it has been "cleaned"
        """        
        txt = txt.replace('.','').replace('?','').replace('!','').replace('"','')\
              .replace(';','').replace(':','').replace(',','').replace('-','')\
              .lower()
        txt = txt.split()
        
        return txt

def stem(s):
    """ takes a string s and returns the stem of s """

    # check for suffixes
    if s[-4:] == 'able' or s[-4:] == 'ible' or s[-4:] == 'tion' or s[-4:] == 'ment' or \
         s[-4:] == 'ness' or s[-4:] == 'less':
        rest = s[:-4]
    elif s[-3:] == 'ing' or s[-3:] == 'ful' or s[-3:] == 'ary' or s[-3:] == 'ity' or \
         s[-3:] == 'ise' or s[-3:] == 'ize':
        rest = s[:-3]
    elif s[-2:] == 'es' or s[-2:] == 'ed' or s[-2:] == 'er' or s[-2:] == 'ly' or \
       s[-2:] == 'ic' or s[-2:] == 'al':
        rest = s[:-2]
    elif s[-1] == 's':
        rest = s[:-1]
    else:
        rest = s

    # check for prefixes
    if rest[:5] == 'under' and len(rest) > 5:
        rest = rest[5:]
    elif rest[:5] == 'trans' or rest[:5] == 'super' or rest[:5] == 'multi':
        rest = rest[5:]
    elif rest[:4] == 'anti' or rest[:4] == 'auto':
        rest = rest[4:]
    elif rest[:2] == 'un' and rest[:5] != 'under':
        rest = rest[2:]
    elif rest[:2] == 're':
        rest = rest[2:]
    else:
        rest = rest
        
    # revisions
        # add e (ex: taking)
    if rest[-2:] == 'at' or rest[-2:] == 'is' or rest[-2:] == 'ur' or \
         rest[-2:] == 'ad' or rest[-2:] == 'ag' or rest[-2:] == 'ak' or \
         rest[-1:] == 'v' or rest[-2:] == 'ac' or rest[-2:] == 'go' or \
         rest[-2:] == 'be' or rest[-2:] == 'ag' or rest[-2:] == 'id' or\
         rest[-2:] == 'gl' or rest[-2:] == 'az':
        rest += 'e'
        # take off last letter (ex: beginning)
    elif len(rest) > 1 and rest[-1] == rest[-2] and rest[-1] != 'z':
        rest = rest[:-1]
        # replace i with y (ex: parties)
    elif len(rest) > 1 and rest[-1] == 'i':
        rest = rest[:-1] + 'y'
    else:
        rest = rest
        
    return rest

def compare_dictionaries(d1, d2):
    """ take two feature dictionaries (d1 and d2) as inputs, and return
        their log similarity score
    """
    score = 0

    lc = [d1[word] for word in d1]
    total = sum(lc)

    for word in d2:
        occurrences = d2[word]
        if word in d1:
            prob = d1[word] / total
            score += occurrences * math.log(prob)
        else:
            prob = 0.5 / total
            score += occurrences * math.log(prob)
            
    return score

        
# class TextModel and its methods        
class TextModel:
    """ blueprint for objects that model a body of text
    """
    def __init__(self, model_name):
        """ constructs new TextModel object by accepting a string model_name
            as parameter and initializing the following 3 attributes:
            - name, string that is a label for this text model
            - words, dictionary that records the number of times each word appears
            - word_lengths, dictionary that records the number of times each word
            length appears
            - stems, dictionary that records the number of times each word stem
            appears
            - sentence_lengths, dictionary that records the number of times each
            sentence length appears
            - common_words, dictionary that records the number of times 30 common words
            appears
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.common_words = {}

    def __repr__(self):
        """ returns a string that includes the name of model as well as the sizes
            dictionaries of each feature of text
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of common words: ' + str(len(self.common_words))
        
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
        
        # sentence_length dictionary
        word_list = s.replace('?', '.').replace('!','.')
        word_list = word_list.split('.')
        for sent in word_list:
            num_words = sent.split()
            if len(num_words) == 0:
                empty = 1
            elif len(num_words) in self.sentence_lengths:
                self.sentence_lengths[len(num_words)] += 1
            else:
                self.sentence_lengths[len(num_words)] = 1

        # clean & split text
        word_list = clean_text(s)

        # words dictionary
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1

        # word_length dictionary
        for w in word_list:
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1

        # stems dictionary
        for w in word_list:
            if stem(w) in self.stems:
                self.stems[stem(w)] += 1
            else:
                self.stems[stem(w)] = 1

        # common_words dictionary
        common_words_list = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', \
                             'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', \
                             'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', \
                             'from', 'they', 'we', 'say', 'her', 'she']

        for w in word_list:
            if w in common_words_list:
                if w in self.common_words:
                    self.common_words[w] += 1
                else:
                    self.common_words[w] = 1
                
        
    def add_file(self, filename):
        """ Adds all of the text in file identified by filename to the model."""

        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()

        self.add_string(text)

    def save_model(self):
        """ Saves the TextModel object self by writing its various feature
            dictionaries to files."""

        fname1 = self.name + '_words.txt'
        f1 = open(fname1, 'w+')
        f1.write(str(self.words))
        f1.close()
        
        fname2 = self.name + '_word_lengths.txt'
        f2 = open(fname2, 'w+')
        f2.write(str(self.word_lengths))
        f2.close()

        fname3 = self.name + '_stems.txt'
        f3 = open(fname3, 'w+')
        f3.write(str(self.stems))
        f3.close()

        fname4 = self.name + '_sentence_lengths.txt'
        f4 = open(fname4, 'w+')
        f4.write(str(self.sentence_lengths))
        f4.close()

        fname5 = self.name + '_common_words.txt'
        f5 = open(fname5, 'w+')
        f5.write(str(self.common_words))
        f5.close()
 
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object
            from their files and assigns them to the attributes of the called
            TextModel
        """
        f1 = open(self.name + '_words.txt', 'r')
        d_str1 = f1.read()
        f1.close()
        self.words = dict(eval(d_str1))

        f2 = open(self.name + '_word_lengths.txt', 'r')
        d_str2 = f2.read()
        f2.close()
        self.word_lengths = dict(eval(d_str2))

        f3 = open(self.name + '_stems.txt', 'r')
        d_str3 = f3.read()
        f3.close()
        self.stems = dict(eval(d_str3))

        f4 = open(self.name + '_sentence_lengths.txt','r')
        d_str4 = f4.read()
        f4.close()
        self.sentence_lengths = dict(eval(d_str4))

        f5 = open(self.name + '_common_words.txt','r')
        d_str5 = f5.read()
        f5.close()
        self.common_words = dict(eval(d_str5))    

    def similarity_scores(self, other):
        """ returns a list of log similarity scores measuring the similiarity
            of self and other (one score for each feature)
        """
        words_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths,\
                                                  self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths,\
                                                      self.sentence_lengths)
        common_words_score = compare_dictionaries(other.common_words, \
                                                  self.common_words)

        scores_list = [round(words_score,3), round(word_lengths_score,3),\
                       round(stems_score,3), round(sentence_lengths_score,3),\
                       round(common_words_score,3)]

        return scores_list
                                                  
    def classify(self, source1, source2):
        """ compares the class TextModel object (self) to two other source
            TextModel objects (source1 and source2) and determine which of
            these other Textmodels is the more likely source
        """
        
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print('scores for', source1.name + ':', scores1)
        print('scores for', source2.name + ':', scores2)

        i = 0
        likely1 = 0
        likely2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                likely1 += 1
            else:
                likely2 += 1

        if likely1 > likely2:
            print(self.name, 'is more likely to have come from', source1.name)
        else:
            print(self.name, 'is more likely to have come from', source2.name)


        
def test():
    """ test TextModel """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ test four new text files with sources """
    source1 = TextModel('New York Times')
    source1.add_file('NYTimes.txt')

    source2 = TextModel('Boston Globe')
    source2.add_file('BostonGlobe.txt')

    new1 = TextModel('NYT article')
    new1.add_file('Test_doc_NYT.txt')
    new1.classify(source1, source2)

        # BG = Boston Globe
    new1 = TextModel('BG article')
    new1.add_file('Test_doc_BG.txt')
    new1.classify(source1, source2)

    new1 = TextModel('CNN article')
    new1.add_file('Test_doc_CNN.txt')
    new1.classify(source1, source2)

        # WP = Washington Post
    new1 = TextModel('WP article')
    new1.add_file('Test_doc_WP.txt')
    new1.classify(source1, source2)

    


