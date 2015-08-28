import boto, os, csv
from boto.s3.key import Key
from config import *

acc_key = AWS_ACCESS_KEY
acc_sec = AWS_SECRET_KEY
bucket = AWS_BUCKET

class CSVRecorder(object):

    def __init__(self):
        # self.script_dir = os.path.abspath(os.path.dirname(__file__))
        self.rel_path = "app/static/csv"
        self.csv_file = "/test_results.csv"
        self.path = os.path.join(self.rel_path, self.csv_file)

    def record_answer(self, row):
        try:
            fp = open("app/static/csv/test_results.csv", "a")
            c = csv.writer(fp)
            c.writerow(row)
            fp.close()
        except IOError:
            return

class S3Connector(object):

    def __init__(self):
        self.c = boto.connect_s3(acc_key, acc_sec)
        self.b = self.c.get_bucket(bucket)
        self.key = "test_results.csv"
        self.filename = "app/static/csv/test_results.csv"

    def upload(self):
        bucket_key = Key(self.b)
        bucket_key.key = self.key
        bucket_key.set_contents_from_filename(self.filename)
        self.b.set_acl("public-read", self.key)
