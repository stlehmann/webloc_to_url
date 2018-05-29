"""
Quick converter for weblink files from Macs *webloc format to
Windows *.url format.

:author: Stefan Lehmann <stlm@posteo.de>
:license: MIT, see license file or https://opensource.org/licenses/MIT

:created on 2018-05-29 14:09:52
:last modified by:   Lehmann
:last modified time: 2018-05-29 15:47:14

"""
import os
import logging
import click


logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger('webloc_to_url')



@click.command()
@click.option('--recursive', default=False, is_flag=True, help='Recurse over subdirectories.')
@click.option('--delete', default=False, is_flag=True, help='Remove weblock files after conversion.')
@click.argument('filepath')
def main(recursive, delete, filepath):
    import validators
    import xml.etree.ElementTree as ET
    import glob

    """Convert *.webloc files to *.url files."""

    # Change to filepath
    if os.path.isdir(filepath):
        os.chdir(filepath)

    if os.path.isfile(filepath):
        webloc_files = [filepath]
    else:
        # Get all webloc files in the current directory or in all subdirectories
        # depending on *recursive* flag
        if recursive:
            webloc_files = glob.glob('**/*.webloc', recursive=recursive)
        else:
            webloc_files = glob.glob('*.webloc')


    for webloc_file in webloc_files:
        # Webloc is XML format. Try to parse it.
        xml_tree = ET.parse(webloc_file)
        root = xml_tree.getroot()

        # Check for dict element
        dict_ = root.find('dict')
        if dict_ is None:
            logger.error(
                f'Could not find "dict" element in webloc file "{webloc_file}".'
            )
            continue

        # Check if key element is there
        key = dict_.find('key')
        if key is None:
            logger.error(
                f'No "key" element in webloc file "{webloc_file}.'
            )
            continue

        # Check if key is URL
        if not (key.text == 'URL'):
            logger.error(
                f'"Key" element should contain string "URL" in file "{webloc_file}".'
            )
            continue

        # Check for string element
        string = dict_.find('string')
        if string is None:
            logger.error(
                f'No element "string" in webloc file "{webloc_file}.'
            )
            continue

        url = string.text

        # Check if url is valid
        if not validators.url(url):
            logger.error(
                f'Invalid url "{url}" in webloc file "{webloc_file}.'
            )
            continue

        url_file_name = os.path.splitext(webloc_file)[0] + '.url'
        with open(url_file_name, 'w', encoding='utf-8') as f:
            f.writelines([
                '[InternetShortcut]\n',
                f'URL={url}\n',
                'IDList=\n',
                'HotKey=0\n',
                'IconFile=\n',
                'IconIndex=0\n',
            ])
        logger.info(f'Created file: {url_file_name}')

        if delete:
            os.remove(webloc_file)
main()
