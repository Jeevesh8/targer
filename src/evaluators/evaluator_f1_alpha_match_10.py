"""f1-micro averaging evaluator for tag components, alpha = 1.0 (strict)"""
from src.evaluators.evaluator_f1_alpha_match_base import EvaluatorF1AlphaMatchBase


class EvaluatorF1AlphaMatch10(EvaluatorF1AlphaMatchBase):
    """
    EvaluatorF1AlphaMatch10 is f1-micro averaging evaluator for tag components, alpha = 1.0 (strict)
    Isaac Persing and Vincent Ng. End-to-end argumentation mining in student essays. NAACL 2016.
    http://www.aclweb.org/anthology/N16-1164.
    """
    def __init__(self):
        super(EvaluatorF1AlphaMatch10, self).__init__(match_alpha_ratio=0.999)
