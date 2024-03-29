from gensim import matutils
import numpy as np
from gensim.corpora import Dictionary

from Orange.data import StringVariable, ContinuousVariable, Domain
from Orange.data.table import Table
from orangecontrib.text.corpus import Corpus
from orangecontrib.text.util import chunkable


MAX_WORDS = 1000


class Topic(Table):
    """ Dummy wrapper for Table so signals can distinguish Topic from Data.
    """

    def __new__(cls, *args, **kwargs):
        """ Bypass Table.__new__. """
        return object.__new__(Topic)


class GensimWrapper:
    name = NotImplemented
    Model = NotImplemented
    num_topics = 1000

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.kwargs = kwargs
        self.model = None
        self.topic_names = []
        self.running = False

    def fit(self, corpus, **kwargs):
        """ Train the model with the corpus.

        Args:
            corpus (Corpus): A corpus to learn topics from.
        """
        if not len(corpus.dictionary):
            return None
        self.reset_model(corpus)
        self.running = True
        self.update(corpus.ngrams_corpus, **kwargs)
        self.topic_names = ['Topic{} ({})'.format(i, ', '.join(words))
                            for i, words in enumerate(self._topics_words(3), 1)]
        self.running = False

    def dummy_method(self, *args, **kwargs):
        pass

    def reset_model(self, corpus):
        # prevent model from updating
        _update = self.Model.update
        self.Model.update = self.dummy_method
        self.id2word = Dictionary(corpus.ngrams, prune_at=None)
        self.model = self.Model(corpus=corpus,
                                id2word=self.id2word, **self.kwargs)
        print(type(self.model))
        self.Model.update = _update

    @chunkable
    def update(self, documents):
        self.model.update(documents)

    def transform(self, corpus, num_topics):
        """ Create a table with topics representation. """
        topics = self.model[corpus.ngrams_corpus]
        self.num_topics = num_topics
        matrix = matutils.corpus2dense(topics, num_terms = self.num_topics, 
                                                num_docs=len(corpus)).T

        corpus.extend_attributes(matrix[:, :len(self.topic_names)], self.topic_names)
        return corpus

    def fit_transform(self, corpus, **kwargs):
        self.fit(corpus, **kwargs)
        return self.transform(corpus)

    def get_topics_table_by_id(self, topic_id):
        """ Transform topics from gensim model to table. """
        words = self._topics_words(MAX_WORDS)
        weights = self._topics_weights(MAX_WORDS)
        if topic_id >= len(words):
            raise ValueError("Too large topic ID.")

        num_words = len(words[topic_id])

        data = np.zeros((num_words, 2), dtype=object)
        data[:, 0] = words[topic_id]
        data[:, 1] = weights[topic_id]

        metas = [StringVariable(self.topic_names[topic_id]),
                 ContinuousVariable("Topic{}_weights".format(topic_id + 1))]
        metas[-1]._out_format = '%.2e'

        domain = Domain([], metas=metas)
        t = Topic.from_numpy(domain,
                             X=np.zeros((num_words, 0)),
                             metas=data)
        t.W = data[:, 1]
        t.name = 'Topic_{}'.format(topic_id + 1)
        return t

    def get_top_words_by_id(self, topic_id, num_of_words=10):
        topics = self._topics_words(num_of_words=num_of_words)
        if not 0 <= topic_id < self.num_topics:
            raise ValueError("Invalid {}".format(topic_id))
        elif topic_id >= len(topics):
            return []
        return topics[topic_id]

    def _topics_words(self, num_of_words):
        """ Returns list of list of topic words. """
        x = self.model.show_topics(-1, num_of_words, formatted=False)
        # `show_topics` method return a list of `(topic_number, topic)` tuples,
        # where `topic` is a list of `(word, probability)` tuples.
        return [[i[0] for i in topic[1]] for topic in x]

    def _topics_weights(self, num_of_words):
        """ Returns list of list of topic weights. """
        topics = self.model.show_topics(-1, num_of_words, formatted=False)
        # `show_topics` method return a list of `(topic_number, topic)` tuples,
        # where `topic` is a list of `(word, probability)` tuples.
        return [[i[1] for i in t[1]] for t in topics]
