from progress.bar import IncrementalBar


def save_html_page(file_path, text_result):
    bar = IncrementalBar("Downloading page", max=1, suffix='%(percent)d%%')
    with open(file_path, 'w+') as fp:
        fp.write(text_result)
    bar.next()
    bar.finish()
