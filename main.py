import pdb
import matplotlib.pyplot as plt
import numpy as np

class CollectionPreprocessor:
    def __init__(self, args):
        self.collection = args

    def preprocess_word(self, word):
        alphanumeric = ''
        for character in word:
            if character.isalnum():
                alphanumeric += character
        return alphanumeric.lower()


    def extract_articles(self):
        collection_list = self.collection.splitlines()
        article_indexes = []
        i = 0
        for line in collection_list:
            if line == "<doc>":
                article_indexes.append(i)
            elif line == "</doc>":
                article_indexes.append(i)
            i += 1
        
        
        articles = []
        l = 0
        for index in article_indexes:
            k = 0
            if ((article_indexes.index(index) % 2) != 0):
                continue
            articles.append([])
            for line in collection_list:
                if k >= index and k <= article_indexes[(article_indexes.index(index) + 1)]:
                    if not line.startswith("<") and not line.endswith(">"):
                        articles[l].append(line)
                k += 1
            l += 1
        
        new_articles_list = []
        m = 0
        for article in articles:
            new_articles_list.append([])
            for element in article:
                if not new_articles_list[m]:
                     new_articles_list[m].append('')
                new_articles_list[m][0] += element
            m += 1
        
        self.all_words_dict = {}
        i=0
        for article in new_articles_list:
            for word in article[0].split():
                proprocessed_word = self.preprocess_word(word)
                if proprocessed_word not in self.all_words_dict.keys():
                    self.all_words_dict[proprocessed_word] = {}
                    for counter in range(len(new_articles_list)):
                        if counter == i:
                            self.all_words_dict[proprocessed_word][counter + 1] = 1
                        else:
                            self.all_words_dict[proprocessed_word][counter + 1] = 0
                else:
                    self.all_words_dict[proprocessed_word][i + 1] += 1
            i += 1
        print(self.all_words_dict)
        
    def create_histogram(self):
        self.total_word_count = []
        for key, value in self.all_words_dict.items():
            total_value = 0
            number_of_times_counted = sum(list(value.values())[0:3]) 
            self.total_word_count.append(number_of_times_counted)

        self.total_word_count.sort()
        bins = np.arange(max(self.total_word_count)) - 0.5
        plt.hist(self.total_word_count, bins, alpha=0.75, color='g', linewidth=0.75, edgecolor='black')
        x1,x2,y1,y2 = plt.axis()
        plt.axis((1,21,y1,y2))
        plt.xticks(np.arange(1, 20, 2))
        plt.xlim([0.5, 20.5])
        plt.show()


collection_file = open(r"txt-for-assignment-data-science.txt", "r") 
collection_string = collection_file.read()
test = CollectionPreprocessor(collection_string)

test.extract_articles()
test.create_histogram()