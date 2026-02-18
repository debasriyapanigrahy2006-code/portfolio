import re

def clean_text(text):
    # Replace double spaces with a unique placeholder
    # We use a placeholder that differs from single space
    # The pattern suggests that words are separated by double spaces
    # and characters within words are separated by single spaces.
    
    # First, handle newlines - preserve them
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        if not line.strip():
            cleaned_lines.append('')
            continue
            
        # Replace double spaces (word separators) with a placeholder
        # Note: sometimes there might be more than 2 spaces, so let's normalize
        # But looking at the file, it seems consistent.
        # Let's try to replace 2 or more spaces with a generic placeholder
        temp_line = re.sub(r'\s{2,}', ' [SEP] ', line)
        
        # Now remove all single spaces that are NOT part of the placeholder
        # Since we added [SEP], we can just remove all spaces now, 
        # but [SEP] has spaces in it? No, let's use a placeholder without spaces.
        temp_line = re.sub(r'\s{2,}', '[SEP]', line)
        
        # Remove all remaining spaces (which are between letters)
        temp_line = temp_line.replace(' ', '')
        
        # Now replace valid word separators [SEP] with a single space
        cleaned_line = temp_line.replace('[SEP]', ' ')
        
        cleaned_lines.append(cleaned_line)
        
    return '\n'.join(cleaned_lines)

if __name__ == '__main__':
    input_path = 'raw_text.txt'
    output_path = 'cleaned_resume.txt'
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_data = f.read()
        
        cleaned_data = clean_text(raw_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_data)
            
        print(f"Successfully cleaned text and saved to {output_path}")
        print("Preview of cleaned text:")
        print(cleaned_data[:500])
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
