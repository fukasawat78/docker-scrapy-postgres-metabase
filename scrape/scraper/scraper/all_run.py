import subprocess
import multiprocessing


def get_crawler_list():
    process = subprocess.Popen('scrapy list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = process.communicate()
    if process.returncode == 0:
        strings = stdout_data.decode('utf-8').split('\n')
        return list(filter(None, strings))
    else:
        raise RuntimeError()


def execute_scraping(crawler_name):
    cmd = 'scrapy crawl %s --loglevel=INFO' % (crawler_name,)
    subprocess.call(cmd.split())


def main():
    jobs = []
    for crawler_name in get_crawler_list():
        job = multiprocessing.Process(target=execute_scraping, args=(crawler_name,))
        jobs.append(job)
        job.start()

    [job.join() for job in jobs]

    print('finish !!!!')


if __name__ == '__main__':
    main()
