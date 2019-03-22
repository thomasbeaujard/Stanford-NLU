from collections import Counter
import os
import sst
from torch_rnn_classifier import TorchRNNClassifier
import pytest

__author__ = "Christopher Potts"
__version__ = "CS224u, Stanford, Spring 2019"


sst_home = os.path.join('data', 'trees')


@pytest.mark.parametrize("reader, count", [
    [sst.train_reader(sst_home, class_func=None), 8544],
    [sst.train_reader(sst_home, class_func=sst.binary_class_func), 6920],
    [sst.train_reader(sst_home, class_func=sst.ternary_class_func), 8544],
    [sst.dev_reader(sst_home, class_func=None), 1101],
    [sst.dev_reader(sst_home, class_func=sst.binary_class_func), 872],
    [sst.dev_reader(sst_home, class_func=sst.ternary_class_func), 1101],

])
def test_readers(reader, count):
    result = len(list(reader))
    assert result == count


@pytest.mark.parametrize("X, n_words, expected", [
    [
        [["a", "b", "c"], ["b", "c", "d"]],
        None,
        ["$UNK", "a", "b", "c", "d"]
    ],
    [
        [["a", "b", "c"], ["b", "c", "d"]],
        2,
        ["$UNK", "b", "c"]
    ],
    [
        [],
        2,
        ["$UNK"]
    ]
])
def test_get_vocab(X, n_words, expected):
    result = sst.get_vocab(X, n_words=n_words)
    assert result == expected


def test_build_dataset_vectorizing():
    phi = lambda tree: Counter(tree.leaves())
    class_func = None
    reader = sst.train_reader
    dataset = sst.build_dataset(
        sst_home,
        reader,
        phi,
        class_func,
        vectorizer=None,
        vectorize=True)
    assert len(dataset['X']) == len(list(reader(sst_home)))
    assert len(dataset['y']) == len(dataset['X'])
    assert len(dataset['raw_examples']) == len(dataset['X'])


def test_build_dataset_not_vectorizing():
    phi = lambda tree: tree
    class_func = None
    reader = sst.train_reader
    dataset = sst.build_dataset(
        sst_home,
        reader,
        phi,
        class_func,
        vectorizer=None,
        vectorize=False)
    assert len(dataset['X']) == len(list(reader(sst_home)))
    assert dataset['X'] == dataset['raw_examples']
    assert len(dataset['y']) == len(dataset['X'])


def test_build_binary_rnn_dataset():
    X, y = sst.build_binary_rnn_dataset(sst_home, sst.train_reader)
    assert len(X) == 6920
    assert len(y) == 6920