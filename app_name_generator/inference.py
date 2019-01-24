#-*- coding: utf-8 -*-

import os 
import json
import pickle
import argparse
import numpy as np
import tensorflow as tf
from SEQ2SEQ import SEQ2SEQ  
from preprocess import convert_to_integer, load_vocab 
from utils import corpus_bleu_score
from config import args, options
from log_util import g_log_inst as logger


class Inference(object):

    def __init__(self):
        self.vocabulary, self.vocabulary_reverse = load_vocab(args.data_path)
        tf.reset_default_graph()
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.allow_growth = True
        session = tf.Session(config=tf_config)

        with tf.name_scope("Train"):
            with tf.variable_scope("Model"):
                self.model = SEQ2SEQ(session, options, "predict")
        self.model.restore(os.path.join(args.root_path, args.restore_path))


    def do_inference(self, keywords):
        enc_x, dec_x, dec_y, enc_x_lens, dec_x_lens = convert_to_integer(
            [[keywords, []]], self.vocabulary) 
        result, _ = self.model.predict_step(
            enc_x, dec_x, dec_y, enc_x_lens, dec_x_lens) 
        result = result[0] 
        num = result.shape[-1]
        predicts = []
        for i in range(num):
            predict = []
            for idx in result[:, i].tolist():
                if idx == self.vocabulary["<eos>"]:
                    break
                predict.append(self.vocabulary_reverse[idx])
            uniq_predict = []
            predict_len = len(predict)
            for i in range(predict_len):
                if i > 0 and predict[i] == predict[i - 1]:
                    continue
                uniq_predict.append(predict[i])
            if uniq_predict:
                predicts.append(uniq_predict)
        return predicts


class InferenceApiHanler(object):
    
    @classmethod
    def init(cls):
        cls.inference_inst = Inference() 
        logger.get().info("Enable inference model done.")

    @classmethod
    def predict_app_name(cls, params):
        keywords = params["query"].strip().split("|")
        predicts = cls.inference_inst.do_inference(keywords)
        names = [" ".join(p) for p in predicts]
        ret_info = {"names": names}
        return (200, ret_info)


if __name__ == "__main__":
    inference_inst = Inference() 
    keywords = ["music", "player", "mp3"] 
    result = inference_inst.do_inference(keywords)
    print ("Input={}, Output={}".format(keywords, result))
