import argparse, json, os, re, requests
from prompt_toolkit.completion import Completer, Completion
from questionary import Style as QuestionaryStyle
import questionary
from rich.box import SIMPLE, SQUARE
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from threading import Thread, Event
from time import sleep
from PIL import Image
from io import BytesIO
from rich.layout import Layout
from rich_pixels import Pixels
from rich.align import Align

session = requests.session()
session.headers.update({
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Dest': 'document', 'User-Agent': 'Mozilla/5.0'
})

RICH_THEME = Theme({
    'heading1': 'bold #bd93f9', 'success': 'bold #50fa7b', 'warning': 'bold #FFB86C', 'url': 'italic #287bde', 'comment': 'dim #6272a4'
})

EXPLOIT_DB_URL = "https://www.exploit-db.com/google-hacking-database"
IMG_URL = "https://raw.githubusercontent.com/nestoris/Win98SE/main/SE98/status/48/image-loading.png"
stop_animation_event = Event()
delimiter = '\n\n'

def set_questionary_params(func, params):
    default_style = {
        "question": "bold fg:#f8f8f2", "qmark": "fg:#FF5555",
        "pointer": "fg:#FF5555 bold", "highlighted": "bg:#6272A4 bold",
        "instruction": "fg:#f8f8f2 bold", "answer": "fg:#50fa7b"
    }
    params['style'] = QuestionaryStyle([("answer", "fg:#50fa7b")]) if func == 'autocomplete' else \
                      QuestionaryStyle(list({**default_style, **dict(params.pop('style', []))}.items()))
    params.setdefault('qmark', u"\u25B9")
    params.setdefault('pointer', u"\u2718")
    params.setdefault('instruction', '\n')
    return params

def dynamic_questionary_func(func_name, params):
    params = set_questionary_params(func_name, params)

    if func_name in ('autocomplete', 'confirm', 'path', 'text', 'press_any_key_to_continue'):
        params.pop('pointer')
        params.pop('instruction')
        if func_name == 'press_any_key_to_continue':
            params.pop('qmark')

    func = getattr(questionary, func_name, None)
    if func: return func(**params).ask()


def display_error_msg(console, message):
    console.print(Panel.fit(Text.from_markup(f'{message} Quitting ... :waving_hand:'), style='bold red'), justify='center')
    return False

def display_main_menu(options):
    answer = dynamic_questionary_func('select', params={'message': 'What do you want to do?', 'choices': options})
    return options.index(answer)

def fetch_dork_suggestions(term):
    session.headers.update({'X-Requested-With': 'XMLHttpRequest'})
    try:
        response = session.get('https://dorksearch.com/autocomplete.php', params={'term': term}, timeout=5)
        return response.json() if response.ok else []
    except Exception:
        return []

def ask_to_provide_query():
    class InlineCompleter(Completer):
        def get_completions(self, document, complete_event):
            term = document.text
            yield from (Completion(s, start_position=-len(term)) for s in fetch_dork_suggestions(term))

    return dynamic_questionary_func('text', params={'message': "Start typing your dork: ", 'completer': InlineCompleter()})

def fetch_exploit_db_categories():
    html_content = session.get(EXPLOIT_DB_URL).content.decode()
    match = re.search(r'<select id="categorySelect">(.*?)</select>', html_content, re.DOTALL)
    return [opt.strip() for opt in re.findall(r'<option\s*(?:value="\d+")?\s*>(.*?)</option>', match.group(1), re.DOTALL) if opt.strip()]

def fetch_dorks_by_category(category_idx):
    params = {'draw': 1, 'length': 100000, 'category': category_idx}
    headers = {'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
    data = session.get(EXPLOIT_DB_URL, params=params, headers=headers).json().get('data', [])
    return [re.search(r'>(.*?)<', item['url_title']).group(1) for item in data if 'url_title' in item]

def display_categories_menu():
    choices = fetch_exploit_db_categories()
    answer = dynamic_questionary_func('select', params={'message': "Choose a category of dorks from Exploit DB:", 'choices': choices})
    return choices.index(answer) + 1

def display_dorks_menu(dorks_list):
    return str(dynamic_questionary_func('select', params={
        'message': "Choose one of the dorks from list fetched:",
        'use_arrow_keys': True,
        'use_jk_keys': False,
        'use_shortcuts': False,
        'use_search_filter': True,
        'choices': dorks_list
    }))

def fetch_google_results(query, language='en', region='us', timeout=10):
    from googlesearch import search
    results, index = [], 0
    while True:
        try:
            batch = search(term=query, lang=language, advanced=True, timeout=timeout, unique=True, num_results=100, start_num=index, region=region)
            valid = [dict(title=r.title, url=r.url, snippet=r.description) for r in batch if not r.url.startswith("/search")]
            if all(item['url'] == '' for item in valid): break
            results.extend(valid)
            index += 100
        except Exception as e:
            return e
    return {'results': results}

def display_references(console):
    console.clear()
    console.print(Panel(Text.from_markup('\n'.join([
        ':link: Link to my [link=https://t.me/]Telegram[/link] channel',
        '',
        ':link: View my project on GitHub [link=https://github.com]GitHub[/link]'
    ])), box=SIMPLE))

def display_set_language_prompt(content):
    langs = {code: name for code, name in re.findall(r'<option value="lang_([^"]+)">([^<]+)</option>', content)}
    return str(dynamic_questionary_func('autocomplete', params={
        'message': "Select language from the list:",
        'choices': list(langs.keys()),
        'meta_information': langs,
        'default': 'en'
    }))

def display_set_region_prompt(content):
    regions = {code: name for code, name in re.findall(r'<option value="country([^"]+)">([^<]+)</option>', content)}
    return str(dynamic_questionary_func('autocomplete', params={
        'message': "Select region from the list:",
        'choices': list(regions.keys()),
        'meta_information': regions,
        'default': 'us'
    }))

def print_results(console, results):
    width = os.get_terminal_size().columns
    for item in results.get('results', []):
        url = item.get('url', '').strip()
        if not url: continue
        title = f'[heading1][link={url}]{item.get("title", "").strip() or "No Title"}[/link][/heading1]'
        url_text = Text.from_markup(url)
        url_text.truncate(width - 20, overflow='ellipsis', pad=False)
        link = f'[url]:link: [link={url}]{url_text}[/link][/url]'
        snippet = item.get('snippet', '').strip()
        if not snippet:
            console.print(Panel(delimiter.join([title, link]), box=SQUARE))
            return
        snippet_text = Text.from_markup(snippet)
        snippet_text.truncate(width * 3, overflow='ellipsis', pad=False)
        console.print(Panel(delimiter.join([title, link, f'[comment]{snippet_text}[/comment]']), box=SQUARE))

def ask_if_output(): return dynamic_questionary_func('confirm', params={'message': 'Do you want to save results?'})
def ask_filepath(): return dynamic_questionary_func('path', params={'message': 'Set output file path:'})
def ask_if_save_results(): return dynamic_questionary_func('confirm', params={'message': 'Do you want to save results to JSON file?', 'style': [('instruction', 'ansigray')]})

def save_to_file(data, filepath):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f)
            return True
    except Exception as e:
        return e

def build_layout():
    img_data = BytesIO(requests.get(IMG_URL).content)
    img = Image.open(img_data).resize((32, 32)).convert('RGBA')
    img = img.crop(img.getbbox())
    rotated = [Pixels.from_image(img.rotate(90 * i, expand=True)) for i in range(4)]
    layout, i = Layout(), 0
    while not stop_animation_event.is_set():
        layout.update(Align.center(rotated[i % 4], vertical='middle'))
        yield layout
        i += 1
        sleep(0.1)


def display_help(console):
    console.clear()
    for s in (
        '[heading1]UI Mode:[/heading1]\nâ â arrows  navigate\nâ¤¶ enter     select\n/ or typing search\n'
        f'Dorks from [link={EXPLOIT_DB_URL}]exploit.db[/link] only in UI mode.',
        '[heading1]CLI Flags:[/heading1]\n-h --help          show help\n-q --query <dork>  set Google query\n'
        '-l --language=xx   language code\n-r --region=xx     region code\n-o --output <file> save output\n'
        '-s --silent        suppress console output\nOutput is JSON.',
        '[heading1]Examples:[/heading1]\n`python dd0rks.py -l en -r us -o test.json -q "intitle:admin ext:sql"`\n'
        '`python dd0rks.py -l en -r us -q intitle:admin`\n`python dd0rks.py -q intitle:admin`'
    ): console.print(s + '\n', new_line_start=True)


def ask_to_run(): dynamic_questionary_func('press_any_key_to_continue', {
    'message': 'Hit [Enter] to run ...',
    'style': [('question', 'fg:#50fa7b bold')]
})

def escape_double_quotes(s): return s.replace('"', '\\"')

def run_tui_flow(console, dork):
    try:
        indent = '  '
        args = [f'{indent}--query "{escape_double_quotes(dork)}"']
        content = requests.get('https://www.google.com/advanced_search').text
        language = display_set_language_prompt(content)
        region = display_set_region_prompt(content)
        args += [f'{indent}--language {language}', f'{indent}--region {region}']
        filepath = ask_filepath().strip() if ask_if_output() else ''
        if filepath:
            args.append(f'  --output "{filepath}"')
        else:
            console.print(f'\n{indent}[warning][blink]â ï¸[/blink]  Caution! Output file path not set. Results wont be saved.[/warning]', new_line_start=True)

        console.print(f'\n{indent}[#ff5555][blink]:floppy_disk:[/blink] Generated command. Save it if you want to run it again later:')
        console.print(f"\n[dim] python dd0rks.py \\\n" + '  \\\n'.join(args) + '[/dim]\n')
        ask_to_run()

        layout = build_layout()
        from rich.live import Live
        with Live(next(layout), console=console, refresh_per_second=10, screen=True) as live:
            Thread(target=lambda: [live.update(f) for f in layout if not stop_animation_event.is_set()]).start()
            results = fetch_google_results(query=dork, language=language, region=region)
            stop_animation_event.set()

        console.clear()
        if not results: return display_error_msg(console, 'Did not get any results.')
        if isinstance(results, Exception): return display_error_msg(console, str(results))
        print_results(console, results)
        if filepath:
            status = save_to_file(results, filepath)
            if isinstance(status, Exception): return display_error_msg(console, str(status))
            console.print(Panel.fit('[success]Results successfully saved[/success] ð¥', box=SIMPLE))
    except Exception as e:
        return display_error_msg(console, e)

def run_cli_flow(args):
    results = fetch_google_results(query=str(args.query), language=str(args.language), region=str(args.region))
    if not results: return print('\033[31m{"error": "Did not get any results"}\x1b[0m')
    if isinstance(results, Exception): return print(f'\033[31m{{"error": "{results}"}}\x1b[0m')
    if not args.silent:
        from rich import print_json
        print_json(json.dumps(results))
    if args.output:
        status = save_to_file(results, args.output)
        if isinstance(status, Exception): return print(f'Error: {status}')
    return True

def parse_args():
    parser = argparse.ArgumentParser(description="Search google")
    parser.add_argument('-q', '--query', type=str)
    parser.add_argument('-l', '--language', type=str, default='en')
    parser.add_argument('-r', '--region', type=str, default='us')
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-s', '--silent', type=bool)
    return parser.parse_args()

def run():
    args = parse_args()
    from rich.console import Console
    console = Console(force_terminal=True, force_interactive=True, highlight=False, theme=RICH_THEME)
    console.clear()
    if args.query: return run_cli_flow(args)
    menu_options = ['Load dorks from exploit.db', 'Proceed with your own query', 'View help docs', 'View references', 'Quit']
    match display_main_menu(menu_options):
        case 0: run_tui_flow(console, display_dorks_menu(fetch_dorks_by_category(display_categories_menu())))
        case 1: run_tui_flow(console, ask_to_provide_query())
        case 2: display_help(console)
        case 3: display_references(console)
        case _: return

run()
