import re
import sys

def migrate_field_metadata(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex som matcher Field(...) med mulighet for multiline innhold (non-greedy)
    pattern = re.compile(
        r'Field\(\s*(.*?)\s*\)',  # alt mellom Field( og )
        re.DOTALL
    )

    def replacer(match):
        inside = match.group(1)

        # Finn title og description med mulighet for multiline og enkelt/dobbelt anførselstegn
        title_match = re.search(r'title\s*=\s*(?P<quote>[\'"])(.*?)\1', inside, re.DOTALL)
        desc_match = re.search(r'description\s*=\s*(?P<quote>[\'"])(.*?)\1', inside, re.DOTALL)

        if title_match and desc_match:
            title_val = title_match.group(2).replace('\n', ' ').strip()
            desc_val = desc_match.group(2).replace('\n', ' ').strip()

            # Fjern title og description (inkl. eventuelle kommaer og whitespace rundt)
            inside_clean = re.sub(r',?\s*title\s*=\s*(?P<quote>[\'"]).*?(?P=quote)', '', inside, flags=re.DOTALL)
            inside_clean = re.sub(r',?\s*description\s*=\s*(?P<quote>[\'"]).*?(?P=quote)', '', inside_clean, flags=re.DOTALL)

            # Rydd opp kommaer, f.eks. hvis det blir komma i starten eller slutten
            inside_clean = inside_clean.strip()
            if inside_clean.endswith(','):
                inside_clean = inside_clean[:-1].rstrip()
            if inside_clean.startswith(','):
                inside_clean = inside_clean[1:].lstrip()

            # Sett inn json_schema_extra på slutten, legg til komma hvis nødvendig
            if inside_clean:
                new_inside = f"{inside_clean}, json_schema_extra={{\"title\": \"{title_val}\", \"description\": \"{desc_val}\"}}"
            else:
                new_inside = f"json_schema_extra={{\"title\": \"{title_val}\", \"description\": \"{desc_val}\"}}"

            return f"Field({new_inside})"
        else:
            return match.group(0)

    new_content = pattern.sub(replacer, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Oppdatert {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Bruk: python migrate_field_metadata.py <filnavn.py>")
        sys.exit(1)

    migrate_field_metadata(sys.argv[1])
