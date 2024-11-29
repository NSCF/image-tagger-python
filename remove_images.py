import os

dir = r'E:\Type specimen imaging\Evolutionary Studies Institute\ESI Karoo Vertebrates\TIFF'

to_remove = [
'BP1-164_LA',
'BP1-164_LC',
'BP1-164_LD',
'BP1-164_LLL',
'BP1-164_LRL',
'BP1-164_LV',
'BP1-174_LC',
'BP1-174_LD',
'BP1-2109_CA',
'BP1-2109_CC',
'BP1-2109_CD',
'BP1-2109_CLL',
'BP1-2109_CRL',
'BP1-2109_CV',
'BP1-2109_MA',
'BP1-2109_MLL',
'BP1-2109_MO',
'BP1-2109_MRL',
'BP1-2109_MV',
'BP1-215_LA',
'BP1-215_LC',
'BP1-215_LD',
'BP1-215_LLL',
'BP1-215_LRL',
'BP1-215_LV',
'BP1-223_KD',
'BP1-223_KLL',
'BP1-223_KV',
'BP1-31_CA',
'BP1-31_CLL',
'BP1-31_CV',
'BP1-31_MO',
'BP1-31_MRL',
'BP1-31_MV',
'BP1-484_CA',
'BP1-484_CC',
'BP1-484_CD',
'BP1-484_CLL',
'BP1-484_CV',
'BP1-499_LA',
'BP1-499_LLL',
'BP1-499_LRL',
'BP1-499_LV',
'BP1-512_LA',
'BP1-512_LC',
'BP1-512_LD',
'BP1-512_LLL',
'BP1-512_LV',
'BP1-81_LA',
'BP1-81_LC',
'BP1-81_LD',
'BP1-81_LLL',
'BP1-81_LRL',
'BP1-81_LV',
'BP1-81_PD',
'BP1-81_PV'
]

print('removing files')
errors = []
for file in to_remove:
  try:
    os.remove(os.path.join(dir, file + '.tif'))
  except Exception as ex:
    errors.append(file)

if len(errors):
  print('the following files were not removed:')
  for file in errors:
    print(file)

print('all done...')
