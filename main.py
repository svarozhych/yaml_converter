import yaml
from ollama import generate
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def parse_yaml_data():
    with open('file_event_win_adsi_cache_creation_by_uncommon_tool.yml', 'r') as f:
        data = yaml.full_load(f)
        #whole_file = yaml.load(f, Loader=yaml.SafeLoader)

    output = {
        'title': data.get('title'),
        'description': data.get('description'),
        'severity': data.get('level'),
        'logsources': data.get('logsource'),
        'detection': data.get('detection')
    }
    
    return(output)


def analyze_with_ai(parsed_data):
    response = generate('gemma3', f'''
            Convert the following Sigma SIEM rule information into a clear, human-readable format:

Input: A single YAML rule with components including name, description, trigger conditions, severity level, response actions, log source requirements, and additional notes.

Output: Format the rule as follows:

[Rule Name]
Description: [Brief explanation of what the rule detects]

- Trigger Conditions:
  • [List the specific conditions that activate this rule]
  
- Severity Level: [The severity rating]

- Response Actions:
  1. [First recommended response step]
  2. [Second recommended response step]
  3. [Continue with all listed response steps]
  
- Log Source Requirements:
  • [List the required log sources]
  
- Additional Notes: [Include context about the attack technique]

Make the output concise and understandable while preserving all important security information.

Here's the rule to convert:
    {parsed_data}''')

    return(response['response'])




yaml_output = parse_yaml_data()
ai_result = analyze_with_ai(yaml_output)
document = Document()
document.add_paragraph(ai_result)
document.save('final.docx')