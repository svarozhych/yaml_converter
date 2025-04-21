import yaml
from ollama import generate
from docx import Document
import glob
from log_conf import logger 


def convert_yaml_files(dir):
    document = Document()
    yaml_files = glob.glob(dir+'/**/*.y*ml', recursive=True)
    if not yaml_files:
        logger.error(f"No YAML files found in directory: {dir}")
        return
        
    logger.info(f'Found {len(yaml_files)} files, processing...')

    for file in yaml_files[0:2]:
        try:
            data = parse_yaml_data(file)
            logger.info(f'Parsed file: {file}')
            output = analyze_with_ai(data)
            logger.info(f'Finished analyzing with ollama: {file}')
            document.add_paragraph(output)
            logger.info(f'Added to .docx: {file}')
        except Exception as e:
            logger.error(f"Error processing YAML files: {str(e)}")
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {str(e)}")

    document.save('final.docx')

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

Make the output concise and understandable while preserving all important security information.

Here's the rule to convert:
    {parsed_data}''')

    return(response['response'])


convert_yaml_files('./sigma/rules/windows')