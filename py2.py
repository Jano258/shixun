import os
import docx
import pandas as pd
import pdfplumber
from collections import defaultdict
import re

class DocumentReader:
    def __init__(self, directory):
        self.directory = directory
        self.index = defaultdict(list)  # 倒排索引
        self.documents = {}  # 存储文档内容
        self.build_index()

    def read_docx(self, file_path):
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])

    def read_pdf(self, file_path):
        with pdfplumber.open(file_path) as pdf:
            return '\n'.join([page.extract_text() for page in pdf.pages])

    def read_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def read_excel(self, file_path):
        df = pd.read_excel(file_path)
        return df.to_string()

    def build_index(self):
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if filename.endswith('.docx'):
                content = self.read_docx(file_path)
            elif filename.endswith('.pdf'):
                content = self.read_pdf(file_path)
            elif filename.endswith('.txt'):
                content = self.read_text(file_path)
            elif filename.endswith('.xlsx'):
                content = self.read_excel(file_path)
            else:
                continue
            self.documents[filename] = content
            self.index_document(filename, content)

    def index_document(self, filename, content):
        words = re.findall(r'\w+', content.lower())
        for word in set(words):
            self.index[word].append(filename)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class DocumentSearch:
    def __init__(self, document_reader):
        self.document_reader = document_reader
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(document_reader.documents.values())

    def search(self, query, n=5):
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_n_indices = np.argsort(scores)[::-1][:n]
        results = [(list(self.document_reader.documents.keys())[i], scores[i]) for i in top_n_indices]
        return results


import tkinter as tk


class DocumentSearchApp:
    def __init__(self, root, document_search):
        self.document_search = document_search
        self.root = root
        self.root.title("202158334055宋永康")

        self.query_label = tk.Label(root, text="请输入关键词:")
        self.query_label.pack()

        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack()

        self.n_label = tk.Label(root, text="搜索数量:")
        self.n_label.pack()

        self.n_entry = tk.Entry(root, width=10)
        self.n_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.search)
        self.search_button.pack()

        self.results_text = tk.Text(root, wrap='word', height=20, width=80)
        self.results_text.pack()

    def search(self):
        query = self.query_entry.get()
        n = int(self.n_entry.get())
        results = self.document_search.search(query, n)
        self.results_text.delete(1.0, tk.END)
        for filename, score in results:
            self.results_text.insert(tk.END, f"{filename}: {score:.4f}\n\n")


# 实例化各类并启动应用
if __name__ == "__main__":
    directory = './data'  # 替换为实际的文件夹路径
    document_reader = DocumentReader(directory)
    document_search = DocumentSearch(document_reader)

    root = tk.Tk()
    app = DocumentSearchApp(root, document_search)
    root.mainloop()


