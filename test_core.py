import unittest

from core.query_engine import QueryEngine
from evaluation.failure_analyzer import FailureAnalyzer
from evaluation.retrieval_evaluator import RetrievalEvaluator, RetrievalMetrics
from retrieval.retriever import Retriever


class RetrieverTests(unittest.TestCase):
    def test_retrieve_returns_ranked_chunks(self) -> None:
        retriever = Retriever()
        chunks = retriever.retrieve("Product X pricing in 2025")
        self.assertEqual(len(chunks), 3)
        self.assertGreaterEqual(chunks[0].score, chunks[1].score)

    def test_retrieve_with_non_positive_k_returns_empty(self) -> None:
        retriever = Retriever()
        self.assertEqual(retriever.retrieve("query", k=0), [])


class EvaluatorTests(unittest.TestCase):
    def test_evaluate_includes_overall_score(self) -> None:
        retriever = Retriever()
        evaluator = RetrievalEvaluator()
        chunks = retriever.retrieve("What is Product X pricing trend?")
        metrics = evaluator.evaluate("What is Product X pricing trend?", chunks, current_year=2026)
        self.assertGreater(metrics.overall_score, 0)
        self.assertLessEqual(metrics.overall_score, 1)


class FailureAnalyzerTests(unittest.TestCase):
    def test_no_retrieval_maps_to_low_quality(self) -> None:
        analyzer = FailureAnalyzer()
        metrics = RetrievalMetrics(0, 0, 0, 0, 0)
        quality, reason, confidence = analyzer.analyze(metrics, had_retrieval=False)
        self.assertEqual(quality, "low")
        self.assertEqual(reason, "no retrieval")
        self.assertLess(confidence, 0.2)

    def test_backward_compatible_analyze_path(self) -> None:
        analyzer = FailureAnalyzer()
        metrics = RetrievalMetrics(0.8, 0.8, 0.8, 0.8, 0.8)
        quality, _, _ = analyzer.analyze(metrics, retrieved_chunks=["doc"])
        self.assertEqual(quality, "high")


class QueryEngineTests(unittest.TestCase):
    def test_run_returns_debug_payload(self) -> None:
        engine = QueryEngine()
        result = engine.run("What happened to Product X pricing?")
        self.assertIn("overall_score", result.debug)
        self.assertEqual(len(result.retrieved_chunks), 3)


if __name__ == "__main__":
    unittest.main()
