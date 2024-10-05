from celery import Celery

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def process_file(file_path):
    pass
