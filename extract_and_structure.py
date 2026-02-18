import pypdf
import json
import re

def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if not line.strip(): continue
        # Collapse "S P A C E D" text
        if len(line) > 3 and line.count(' ') > len(line) / 2.5:
             if '  ' in line:
                 line = line.replace('  ', '###').replace(' ', '').replace('###', ' ')
             else:
                 line = line.replace(' ', '')
        cleaned_lines.append(line.strip())
    return cleaned_lines

def parse_resume(lines):
    data = {
        "name": "DEBASRIYA PANIGRAHY", # Found previously
        "contact": {
            "phone": "",
            "email": "",
            "address": "",
            "links": []
        },
        "summary": "",
        "education": [],
        "projects": [],
        "skills": [],
        "languages": ["English", "French"], # Found in raw text
        "strengths": []
    }
    
    full_text = "\n".join(lines)
    
    # regex for contact
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', full_text)
    if email_match: data["contact"]["email"] = email_match.group(0)
    
    phone_match = re.search(r'\b7\d{9}\b', full_text) # Starts with 7 based on previous run
    if phone_match: data["contact"]["phone"] = phone_match.group(0)
    
    # Address heuristic
    if "Berhampur" in full_text:
        # Find line with Berhampur
        for line in lines:
            if "Berhampur" in line:
                data["contact"]["address"] = line
                break

    # Summary: Look for the long paragraph
    summary_parts = []
    capture_summary = False
    for line in lines:
        if "I am a B.Tech" in line:
            capture_summary = True
        if capture_summary:
            summary_parts.append(line)
            if line.endswith("."): # End of paragraph?
                pass
            if "Subjects of Interest" in line or "Technical Skills" in line:
                capture_summary = False
                break
    
    data["summary"] = " ".join(summary_parts).replace("Subjects of Interest", "").strip()

    # Education: Look for "Bachelor"
    for i, line in enumerate(lines):
        if "Bachelor of Technology" in line:
            data["education"].append({
                "degree": line,
                "school": lines[i+1] if i+1 < len(lines) else "",
                "year": lines[i+2] if i+2 < len(lines) else ""
            })
            break

    # Skills sections
    capture_skills = False
    for line in lines:
        if "Technical Skills" in line:
            capture_skills = True
            continue
        if "ACADEMIC PROJECTS" in line:
            capture_skills = False
        
        if capture_skills:
            if ":" in line:
                 parts = line.split(":", 1)
                 data["skills"].append({"category": parts[0].strip(), "items": parts[1].strip()})
            elif "Core Concepts" in line:
                pass
            elif line.strip() and len(line) > 3:
                # Add as generic skill or sub-item
                 if not any(s["category"] == "Other" for s in data["skills"] if isinstance(s, dict)):
                      data["skills"].append({"category": "Other", "items": line})
                 else:
                      # append to last
                      pass

    # Projects
    capture_projects = False
    current_project = {}
    for line in lines:
        if "ACADEMIC PROJECTS" in line:
            capture_projects = True
            continue
        if "STRENGTHS" in line:
            capture_projects = False
            
        if capture_projects:
            if line.isupper() and len(line) > 10:
                # New project title?
                if current_project:
                    data["projects"].append(current_project)
                current_project = {"title": line, "description": ""}
            elif current_project:
                current_project["description"] += line + " "
    
    if current_project:
        data["projects"].append(current_project)

    # Strengths
    capture_strengths = False
    for line in lines:
        if "STRENGTHS" in line:
            capture_strengths = True
            continue
        if capture_strengths:
            if line.isupper(): # Strengths seem to be uppercase
                data["strengths"].append(line)

    return data

def main():
    try:
        # Re-read raw text if possible or just parse content we know
        import pypdf
        reader = pypdf.PdfReader("Black White Minimalist CV Resume.pdf")
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        cleaned = clean_text(text)
        data = parse_resume(cleaned)
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("Done")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
