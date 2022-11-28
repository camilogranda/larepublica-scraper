import requests
import lxml.html as html
import os
import datetime 


HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]//span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/descendant-or-self::text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[1]
                title = title.replace('\"', '')
                title = title.replace('\n', '')
                #remove the quotes from the title
                title.replace('\'', '')
                #remove the tabs from the title
                title = title.replace('\t', '')
                #remove the carriage returns from the title
                title = title.replace('\r', '')
                #remove white spaces from the title
                title = title.strip()
                # Note: title is for .txt file and final_title for processing html title
                final_title = title
                #replace the accents from the title
                title = title.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                #replace the accents from the title
                title = title.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
                #remove the question marks and exclamation marks from the title
                title = title.replace('?', '').replace('¿', '').replace('!', '').replace('¡', '')
                #remove the colons, semicolons, commas, dots, parentheses and spaces from the title
                title = title.replace(':', '').replace(';', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
                #remove the special characters from the title 
                title = title.replace('%', '').replace('$', '').replace('#', '').replace('@', '').replace('&', '').replace('*', '').replace('+', '').replace('=', '').replace('-', '').replace('_', '').replace('/', '').replace('\\', '').replace('|', '').replace('<', '').replace('>', '').replace('"', '').replace('\'', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            try:
                with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                    f.write(final_title)
                    f.write('\n\n')
                    f.write(summary)
                    f.write('\n\n')
                    for p in body:
                        f.write(p)
                        f.write('\n')
            except:
                print('No se pudo escribir el archivo')
        else:
            raise ValueError(f'Error:', {response.status_code})
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices, '\n', 'length:', len(links_to_notices))

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error:', response.status_code)
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()

