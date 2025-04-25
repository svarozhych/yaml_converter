import yaml
from ollama import generate
from docx import Document
import glob
from log_conf import logger 
from docx.shared import Pt


def convert_yaml_files(dir):
    document = Document()
    yaml_files = glob.glob(dir+'/**/*.y*ml', recursive=True)
    success = True
    if not yaml_files:
        logger.error(f"No YAML files found in directory: {dir}")
        success = False
        
    logger.info(f'Found {len(yaml_files)} files, processing...')

    rule_count = 1

    for file in yaml_files[0:2]:
        try:
            data = parse_yaml_data(file)
            logger.info(f'Parsed file: {file}')
            output = analyze_with_ai(data)
            logger.info(f'Finished analyzing with ollama: {file}')
            add_formatted_text_to_document(document, output, rule_count)
            logger.info(f'Added to .docx: {file}')
            rule_count += 1
        except Exception as e:
            logger.error(f"Error processing YAML files: {str(e)}")
            success = False
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {str(e)}")
            success = False

    document.save('final.docx')
    return success

def convert_single_file(path):
    document = Document()
    yaml_file = path
    success = True

    if not yaml_file:
        logger.error("YAML file does not exist")
        success = False
    try:
        data = parse_yaml_data(yaml_file)
        logger.info(f'Parsed file: {yaml_file}')
        output = analyze_with_ai(data)
        logger.info(f'Finished analyzing with ollama: {yaml_file}')
        add_formatted_text_to_document(document, output)
        logger.info(f'Added to .docx: {yaml_file}')
        document.save('converted_yaml.docx')
        success = True
    except Exception as e:
            logger.error(f"Error processing YAML files: {str(e)}")
            success = False
    except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {str(e)}")
            success = False

    return success

def parse_yaml_data(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.full_load(f)

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

Make the output concise and understandable while preserving all important security information. DO NOT add any links to resources.

Here's the rule to convert:
    {parsed_data}''')

    return(response['response'])

def add_formatted_text_to_document(document, text, rule_number=None):
    lines = text.split('\n')
    for style in document.styles:
        if hasattr(style, 'paragraph_format'):
            style.paragraph_format.line_spacing = 1.0
            style.paragraph_format.space_before = Pt(0)
            style.paragraph_format.space_after = Pt(3)

    for i, line in enumerate(lines):
        if line.startswith('**') and i == 0:
            title_text = line.strip('**')
            p = document.add_paragraph()
            if rule_number is not None:
                run = p.add_run(f"{rule_number}. {title_text}")
            else:
                run = p.add_run(title_text)
            run.bold = True
        elif line.startswith('Description:'):
            document.add_paragraph(line)
        elif line.startswith('- '):
            document.add_paragraph(line)
        elif line.startswith('  • '):
            p = document.add_paragraph(line.strip('  • '), style='List Bullet')
        else:
            if line.strip():
                document.add_paragraph(line)

        if 'p' in locals():
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(3)

    if rule_number is not None:
        p = document.add_paragraph('_' * 105)
        p.paragraph_format.space_after = Pt(9)
        p.alignment = 1  
