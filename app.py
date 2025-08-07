from flask import Flask, request, jsonify
from markdown import markdown

app = Flask(__name__, static_folder='static', static_url_path='')

def markdown_to_trac_wiki(md_text):
    # This function performs a simplified conversion from Markdown to Trac Wiki syntax.
    # A full-featured conversion would require a more robust parsing approach (e.g., AST transformation)
    # as Trac Wiki and Markdown have different syntax and capabilities.
    # This implementation focuses on common elements using regular expressions.

    import re

    # 1. Convert bold: **text** or __text__ to '''text'''
    # Using a regex to handle cases where bold markers might be adjacent to other characters.
    # This regex ensures that the markers are not part of a larger word.
    md_text = re.sub(r'\*\*(.+?)\*\*', r"'''\1'''", md_text)
    md_text = re.sub(r'__(.+?)__', r"'''\1'''", md_text)

    # 2. Convert italic: *text* or _text_ to ''text''
    # Similar to bold, using regex for more precise matching.
    md_text = re.sub(r'\*(.+?)\*', r"''\1''", md_text)
    md_text = re.sub(r'_(.+?)_', r"''\1''", md_text)

    # 3. Convert links: [text](url) to [url text]
    # This regex captures the link text and URL, then reorders them for Trac Wiki.
    # It's a basic conversion and might not cover all edge cases (e.g., nested brackets).
    md_text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'[\2 \1]', md_text)

    # 4. Convert headers: # Header to = Header =
    # Iterating through header levels for conversion.
    for i in range(6, 0, -1): # Process from H6 to H1 to avoid conflicts
        md_text = re.sub(r'^{}{}\s*(.*)$'.format('#' * i, ' ' if i > 0 else ''), r'{} \1 {}'.format('=' * i, '=' * i), md_text, flags=re.MULTILINE)

    # 5. Convert unordered lists: - Item to  * Item
    # Ensures that only lines starting with '- ' are converted to Trac Wiki list items.
    md_text = re.sub(r'^- (.*)$', r' * \1', md_text, flags=re.MULTILINE)

    # 6. Convert ordered lists: 1. Item to  1. Item (Trac uses similar syntax)
    # This assumes simple ordered lists. More complex nested lists would require advanced parsing.
    md_text = re.sub(r'^\d+\. (.*)$', r' 1. \1', md_text, flags=re.MULTILINE)

    # 7. Convert code blocks: ```code``` to {{{\ncode\n}}}
    # Handles multi-line code blocks. The `re.DOTALL` flag allows '.' to match newlines.
    md_text = re.sub(r'```(.*?)```', r'{{{\n\1\n}}}', md_text, flags=re.DOTALL)

    # 8. Convert tables: | to ||
    # This handles basic Markdown tables by converting single pipes to double pipes
    # Note: This is a simple conversion and doesn't handle complex table formatting
    # Fix for re.PatternError: look-behind requires fixed-width pattern
    # The new regex matches a single '|' that is not part of '||'
    md_text = re.sub(r'(?<!\|)\|(?!\|)', r'||', md_text)
    
    # 9. Process table headers: make first row bold and remove separator row
    lines = md_text.split('\n')
    processed_lines = []
    in_table = False
    
    for i, line in enumerate(lines):
        # Check if this line is a table row (starts and ends with ||)
        if line.strip().startswith('||') and line.strip().endswith('||'):
            if not in_table:
                # First row of table - make it bold
                cells = [cell.strip() for cell in line.strip()[2:-2].split('||')]
                bold_cells = [f"'''{cell}'''" if cell.strip() else "" for cell in cells]
                processed_line = '||' + '||'.join(bold_cells) + '||'
                processed_lines.append(processed_line)
                in_table = True
            else:
                # Check if this is a separator row (contains only - and |)
                if not re.match(r'^\|\|[-\|\s]*\|\|$', line.strip()):
                    # Regular table row - keep it
                    processed_lines.append(line)
                # If it's a separator row, skip it (remove it)
        else:
            # Not a table row - keep as is
            processed_lines.append(line)
            in_table = False
    
    md_text = '\n'.join(processed_lines)

    # Further improvements could include:
    # - Handling inline code (``code`` to `code`)
    # - Blockquotes (> text to {{{#!wiki markdown\ntext\n}}}
    # - More advanced table handling (alignment, colspan, etc.)
    # - Images (![alt](url) to {{{\n[[Image(url, alt)]]\n}}}
    # - Definition lists, footnotes, etc.
    # - A more robust Markdown parser library (e.g., `mistune` or `markdown-it-py`) combined with
    #   a custom renderer or AST transformer for Trac Wiki output.

    return md_text

    return md_text

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    markdown_text = data.get('markdown_text', '')
    trac_wiki_text = markdown_to_trac_wiki(markdown_text)
    return jsonify({'trac_wiki_text': trac_wiki_text})

@app.route('/')
def index():
    # Serve the index.html file
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)