import pandas as pd
import time
from sklearn.metrics import precision_recall_fscore_support

from py2 import DocumentReader, DocumentSearch


class DocumentSearchEvaluator:
    def __init__(self, document_search, ground_truth_file):
        self.document_search = document_search
        self.ground_truth = self.load_ground_truth(ground_truth_file)

    def load_ground_truth(self, file_path):
        ground_truth = {}
        df = pd.read_csv(file_path)
        print("CSV columns:", df.columns)
        for _, row in df.iterrows():
            query = row['query']
            relevant_documents = row['relevant_documents'].split(', ')
            ground_truth[query] = relevant_documents
        return ground_truth

    def evaluate(self, query, n=5):
        start_time = time.time()
        results = self.document_search.search(query, n)
        response_time = time.time() - start_time

        retrieved_documents = [filename for filename, _ in results]
        relevant_documents = self.ground_truth.get(query, [])

        y_true = [1 if doc in relevant_documents else 0 for doc in retrieved_documents]
        y_pred = [1] * len(retrieved_documents)

        # Extend y_true and y_pred to have the same length as relevant_documents
        y_true.extend([1] * (len(relevant_documents) - len(y_true)))
        y_pred.extend([0] * (len(relevant_documents) - len(y_pred)))

        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='binary', zero_division=0
        )

        false_positive_rate = sum(1 for doc in retrieved_documents if doc not in relevant_documents) / len(retrieved_documents) if retrieved_documents else 0

        return precision, recall, f1, response_time, false_positive_rate

    def evaluate_all(self, n=5):
        results = []
        for query in self.ground_truth.keys():
            precision, recall, f1, response_time, false_positive_rate = self.evaluate(query, n)
            results.append((query, precision, recall, f1, response_time, false_positive_rate))
        return results

# 实例化评估类并评估所有查询
if __name__ == "__main__":
    directory = './data'  # 替换为实际的文件夹路径
    document_reader = DocumentReader(directory)
    document_search = DocumentSearch(document_reader)

    evaluator = DocumentSearchEvaluator(document_search, 'ground_truth.csv')
    evaluation_results = evaluator.evaluate_all(n=5)

    for result in evaluation_results:
        query, precision, recall, f1, response_time, false_positive_rate = result
        print(f"查询: {query}")
        print(f"精度: {precision:.4f}, 召回率: {recall:.4f}, F1: {f1:.4f}, 响应时间: {response_time:.4f},误报率: {false_positive_rate:.4f}")
        print()
