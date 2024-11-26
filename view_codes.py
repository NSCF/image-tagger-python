import re

structures = {
  'H': 'head',
  'S': 'skin',
  'L': 'skull',
  'C': 'cranium',
  'M': 'mandible',
  'P': 'postcranium',
  'B': 'long bone',
  'K': 'skeleton',
  'W': 'whole specimen'
}

sides = {
  'L': 'left',
  'R': 'right',
}

views = {
  'D': 'dorsal',
  'V': 'ventral',
  'L': 'lateral',
  'O': 'occlusional',
  'C': 'occipital',
  'A': 'anterior',
  'P': 'posterior',
  'R': 'proximal',
  'S': 'distal',
  'M': 'medial',
  'U': 'unspecified'
}

descriptors = {
'G': 'group', 
'V': 'view', 
'S': 'section', 
'I': 'image'
}

def make_view(code):
  '''make a full view description from the code'''
  if code and code.strip():
    code = code.upper().strip()
    view = []

    if code == "LABEL":
      view.append('label')
    elif len(code) == 3: #we have a side
      try:
        view.append(structures[code[0]])
        view.append(sides[code[1]])
        view.append(views[code[2]])
      except:
        raise Exception('invalid code')
    elif len(code) == 2:
      if any(char.isdigit() for char in code):
        try:
          view.append(descriptors[code[0]])
          view.append(re.search(r'\d+', code)[0])
        except:
          raise Exception('invalid code')
      else:

        try:
          view.append(structures[code[0]])
          view.append(views[code[1]])
        except:
          raise Exception('invalid code')
    elif len(code) == 1:
      try:
        view.append(structures[code[0]])
      except:
        raise Exception('invalid code')

    else:
      raise Exception('invalid code')

    return ' '.join(view).strip()