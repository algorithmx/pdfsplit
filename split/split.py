import PyPDF2
import re
import subprocess
import sys
import os
    

def find_chapter_starters(pdf_reader):
    chapter = 0
    chapter_starters = []
    if pdf_reader.is_encrypted:
        pdf_reader.decrypt('')
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        content = page.extract_text()
        if is_chapter_start_page(content, chapter): 
            print('Page:', page_num, 'Content:', content[:60])
            chapter_starters.append(page_num)
            chapter+=1
    return chapter_starters


def is_chapter_start_page(content, prev_ch):
    if 'Chapter' in content:
        # finer criteria
        if re.match(r'^\s*Chapter\s+\d+', content, re.IGNORECASE):
            return True
        else:
            return False
    else:
        return False

def split_pdf_into_chapters(input_file):
    with open(input_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        chapter_starters = find_chapter_starters(pdf_reader)
        chapter_starters.append(len(pdf_reader.pages))
        if chapter_starters[0] != 0:
            chapter_starters.insert(0, 0)
        print(f'Found {len(chapter_starters) - 1} chapters in the PDF file.')
        print('Chapter start pages:', chapter_starters)
        print('Splitting PDF into chapters...')
        if pdf_reader.is_encrypted:
            pdf_reader.decrypt('')
        for i in range(0, len(chapter_starters) - 1):
            start_page = chapter_starters[i]
            end_page = chapter_starters[i + 1] - 1
            output_file_name = input_file.replace('.pdf', f'_ch_{i:02}.pdf')
            if os.path.isfile(output_file_name):
                continue
            try:
                subprocess.run(['pdftk', input_file, 'cat', f'{start_page + 1}-{end_page + 1}', 'output', output_file_name])
            except Exception as e:
                print(f'Error: {str(e)}')

    print('PDF split into chapters successfully!')

