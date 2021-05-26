import eng_to_ipa as ipa
import re

replace_map = {
    '’': "'",
    '‘': "'",
    '‛': "'",
    '“': '"',
    '”': '"',
    '‟': '"',
    '–': ' ',
    '-': ' '
}

ipa_encoding_map = {
    "eɪ": "1",
    "aʊ": "2",
    "aɪ": "3",
    "ər": "4",
    "oʊ": "5",
    "ɔɪ": "6"
}

def select_ipa(ipa_candidates):
    if len(ipa_candidates) == 1:
        return ipa_candidates[0]
    for ipa in ipa_candidates:
        if "hˈw" in ipa or 'hw' in ipa:  
            if ipa.replace('hˈw', 'ˈw').replace('hw', 'w') in ipa_candidates:
                ipa_candidates.remove(ipa)
    return ipa_candidates[0]

def validate_label(label):
    for a, b in replace_map.items():
        label = label.replace(a, b)
    ipa_list = ipa.ipa_list(label, keep_punct=False)
    label = ' '.join([select_ipa(ipa_candidates) for ipa_candidates in ipa_list]).strip()
    if "*" in label:
        return None
    if re.search(r"[0-9]|[(<\[\]&*{]", label) is not None:
        return None
    for origin_ipa, code in ipa_encoding_map.items():
        label = label.replace(origin_ipa, code)
    for i, char in enumerate(label):
        if i == len(label)-1:
            break
        if char == "ˈ" or char == 'ˌ':
            label = label[:i] + label[i:i+2][::-1] + label[i+2:]
    return label

def validate_label2(label):
    for a, b in replace_map.items():
        label = label.replace(a, b)
    ipa_list = ipa.ipa_list(label, keep_punct=False)
    label = ' '.join([word_list[0] for word_list in ipa_list]).strip()
    if "*" in label:
        return None
    if re.search(r"[0-9]|[(<\[\]&*{]", label) is not None:
        return None
    return label

def validate_label_ignore(label):
    for a, b in replace_map.items():
        label = label.replace(a, b)
    ipa_list = ipa.ipa_list(label, keep_punct=False)
    label = ' '.join([word_list[0] for word_list in ipa_list]).strip()
    return label

def validate(label):
    for a, b in replace_map.items():
        label = label.replace(a, b)
    ipa_list = ipa.ipa_list(label, keep_punct=False)
    if max(map(lambda ipas: len(ipas), ipa_list)) > 1:
        return None
    label = ' '.join([word_list[0] for word_list in ipa_list]).strip()
    if "*" in label:
        return None
    if re.search(r"[0-9]|[(<\[\]&*{]", label) is not None:
        return None
    
    return label



