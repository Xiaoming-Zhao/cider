# Filename: ciderD.py
#
# Description: Describes the class to compute the CIDEr-D (Consensus-Based Image Description Evaluation) Metric
#               by Vedantam, Zitnick, and Parikh (http://arxiv.org/abs/1411.5726)
#
# Creation Date: Sun Feb  8 14:16:54 2015
#
# Authors: Ramakrishna Vedantam <vrama91@vt.edu> and Tsung-Yi Lin <tl483@cornell.edu>
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .ciderD_scorer import CiderDScorer
import pdb
import numpy as np


class CiderD:
    """
    Main Class to compute the CIDEr metric

    """

    def __init__(self, n=4, sigma=6.0, df="corpus", df_dir=None,
                 pre_computed_gt_cnts2vec_flag=0):
        # set cider to sum over 1 to 4-grams
        self._n = n
        # set the standard deviation parameter for gaussian penalty
        self._sigma = sigma
        # set which where to compute document frequencies from
        self._df = df
        self.df_dir = df_dir
        self.is_pre_computed_gt_cnts2vec = pre_computed_gt_cnts2vec_flag
        self.ciderD_scorer = CiderDScorer(n=self._n, df_mode=self._df, df_dir=df_dir,
                                          pre_computed_gt_cnts2vec_flag=pre_computed_gt_cnts2vec_flag)

    def compute_score(self, gts, res, pre_computed_gt_cnts2vec=None):
        """
        Main function to compute CIDEr score
        :param  hypo_for_image (dict) : dictionary with key <image> and value <tokenized hypothesis / candidate sentence>
                ref_for_image (dict)  : dictionary with key <image> and value <tokenized reference sentence>
        :return: cider (float) : computed CIDEr score for the corpus
        """

        # clear all the previous hypos and refs
        tmp_cider_scorer = self.ciderD_scorer.copy_empty()
        tmp_cider_scorer.clear()

        for res_id in res:

            hypo = res_id['caption']
            ref = gts[res_id['image_id']]

            # Sanity check.
            assert(type(hypo) is list)
            assert(len(hypo) == 1)
            assert(type(ref) is list)
            assert(len(ref) > 0)

            tmp_cider_scorer += (hypo[0], ref)

        (score, scores) = tmp_cider_scorer.compute_score(pre_computed_gt_cnts2vec=pre_computed_gt_cnts2vec)
        ctest_ngram_cnts = [len(_) for _ in tmp_cider_scorer.ctest]

        return score, scores, np.mean(ctest_ngram_cnts), ctest_ngram_cnts

    def method(self):
        return "CIDEr-D"
