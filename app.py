import os
from flask import Flask, request, abort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

app = Flask(__name__)


def file_reader(file):
    with open(file) as f:
        counter = 0
        while True:
            try:
                line = next(f)
            except StopIteration:
                break
            yield line
            counter += 1


def filter_func(log_arg, content: str):
    return filter(lambda log_item: content in log_item, log_arg)


def map_func(log_arg, col: int):
    return map(lambda log_item: log_item.split(' ')[col], log_arg)


def unique_func(log_arg):
    return set(log_arg)


def sort_func(log_arg, direction: str):
    return sorted(log_arg, reverse=True if direction == 'desc' else False)


def limit_func(log_arg, quantity: int):
    return [x for i, x in enumerate(log_arg) if i < quantity]


@app.route("/perform_query", methods=["POST"])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    if not all((request.form.get("cmd1", ""), request.form.get("value1", ""), request.form.get("file_name", ""))):
        abort(400)

    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    data_file_name = os.path.join(DATA_DIR, "apache_logs.txt")
    if not os.path.exists(data_file_name):
        abort(400)

    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    log = file_reader(data_file_name)
    args = dict(zip({v: '' for k, v in request.form.to_dict().items() if k[:3] == 'cmd'},
                    {v: '' for k, v in request.form.to_dict().items() if k[:3] == 'val'}))
    for k, v in args.items():
        match (k):
            case 'filter':
                log = filter_func(log, v)
            case 'map':
                try:
                    log = map_func(log, int(v))
                except ValueError:
                    abort(400)
            case 'unique':
                log = unique_func(log)
            case 'sort':
                log = sort_func(log, v)
            case 'limit':
                try:
                    log = limit_func(log, int(v))
                except ValueError:
                    abort(400)

    return app.response_class("\n".join(list(log)), content_type="text/plain")


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
