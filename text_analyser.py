import os
import time
import logging

from threading import Thread
from multiprocessing import Process, Queue
from typing import Dict, List

# Логування
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(threadName)s/%(processName)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger()

# Дані
NUM_FILES = 10
KEYWORDS = [
    "queue",
    "timeout",
    "process",
    "thread",
    "pipe",
    "semaphore",
    "spawn",
    "children",
    "task",
    "python",  # додано для показу kw без збігів
]
FILES = [f"file{i}.txt" for i in range(1, NUM_FILES + 1)]


# Створення файлів
def create_test_files():
    content = [
        "It is a simplified Queue type, very close to a locked Pipe.",
        "Join the background thread.",
        "Indicate that no more data will be put on this queue by the current process.",
        "It blocks at most timeout seconds.",
        "No keywords here.",
        "Return the approximate size of the queue.",
        "This class requires a functioning shared Semaphore implementation",
        "Indicate that a formerly enqueued task is complete.",
        "Return list of all live children of the current process.",
        "The possible start methods are 'fork', 'spawn' and 'forkserver'.",
    ]
    for i, text in enumerate(content):
        with open(FILES[i], "w", encoding="utf-8") as f:
            f.write(text)


# Пошук
def search_in_file(filepath: str, keywords: List[str]) -> Dict[str, List[str]]:
    result = {kw: [] for kw in keywords}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().lower()
            for kw in keywords:
                if kw.lower() in text:
                    result[kw].append(filepath)
    except FileNotFoundError:
        logger.error(f"Файл не знайдено: {filepath}")
    except Exception as e:
        logger.error(f"Помилка читання {filepath}: {e}")
    return result


# Об'єднання
def merge_results(results_list: List[Dict[str, List[str]]]) -> Dict[str, List[str]]:
    merged = {kw: [] for kw in KEYWORDS}
    for res in results_list:
        for kw, files in res.items():
            merged[kw].extend(files)
    for kw in merged:
        merged[kw] = sorted(set(merged[kw]))
    return merged


# Threading
def threading_search(file_chunks: List[List[str]]) -> Dict[str, List[str]]:
    results = []
    threads = []

    def worker(chunk):
        local_res = {kw: [] for kw in KEYWORDS}
        for file in chunk:
            res = search_in_file(file, KEYWORDS)
            for kw, files in res.items():
                local_res[kw].extend(files)
        results.append(local_res)

    for chunk in file_chunks:
        t = Thread(target=worker, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return merge_results(results)


# Multiprocessing
def process_worker(chunk: List[str], queue: Queue):
    local_res = {kw: [] for kw in KEYWORDS}
    for file in chunk:
        res = search_in_file(file, KEYWORDS)
        for kw, files in res.items():
            local_res[kw].extend(files)
    queue.put(local_res)


def multiprocessing_search(file_chunks: List[List[str]]) -> Dict[str, List[str]]:
    queue = Queue()
    processes = []

    for chunk in file_chunks:
        p = Process(target=process_worker, args=(chunk, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = []
    for _ in processes:
        results.append(queue.get())

    return merge_results(results)


def chunk_files(file_list: List[str], num_chunks: int) -> List[List[str]]:
    chunk_size = len(file_list) // num_chunks
    return [
        file_list[i : i + chunk_size] for i in range(0, len(file_list), chunk_size)
    ] or [file_list]


def main():
    create_test_files()
    logger.info("Тестові файли створено.")

    num_workers = 4
    chunks = chunk_files(FILES, num_workers)

    # Threading
    logger.info("=== Threading ===")
    start = time.time()
    result_thread = threading_search(chunks)
    logger.info("Час виконання: %.4f сек", time.time() - start)
    logger.info("%s", result_thread)
    logger.info("")

    # Multiprocessing
    logger.info("=== Multiprocessing ===")
    start = time.time()
    result_mp = multiprocessing_search(chunks)
    logger.info("Час виконання: %.4f сек", time.time() - start)
    logger.info("%s", result_mp)

    # Очистка
    for f in FILES:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    main()

# Результати виконання
"""
[20:53:37] [MainThread/MainProcess] Тестові файли створено.

=== Threading ===
[20:53:37] [MainThread/MainProcess] Час виконання: 0.0020 сек
[20:53:37] [MainThread/MainProcess] {'queue': ['file1.txt', 'file3.txt', 'file6.txt', 'file8.txt'], 'timeout': ['file4.txt'], 'process': ['file3.txt', 'file9.txt'], 'thread': ['file2.txt'], 'pipe': ['file1.txt'], 'semaphore': ['file7.txt'], 'spawn': ['file10.txt'], 'children': ['file9.txt'], 'task': ['file8.txt'], 'python': []}

=== Multiprocessing ===
[20:53:37] [MainThread/MainProcess] Час виконання: 0.2190 сек
[20:53:37] [MainThread/MainProcess] {'queue': ['file1.txt', 'file3.txt', 'file6.txt', 'file8.txt'], 'timeout': ['file4.txt'], 'process': ['file3.txt', 'file9.txt'], 'thread': ['file2.txt'], 'pipe': ['file1.txt'], 'semaphore': ['file7.txt'], 'spawn': ['file10.txt'], 'children': ['file9.txt'], 'task': ['file8.txt'], 'python': []}
"""
