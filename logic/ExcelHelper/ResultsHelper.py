import os
import datetime


def create_results_path():
    start_time = datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S')
    cur_path = os.path.dirname(os.path.dirname(__file__))
    project_path = os.path.dirname(cur_path)
    results_path = os.path.join(project_path, "results", str(start_time))
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    return results_path


if __name__ == "__main__":
    create_results_path()
