map_names = {'id': 'id',
 'Müüa korter': 'title',
 'Tube': 'room_nr',
 'Üldpind': 'total_size',
 'Korrus/Korruseid': 'floor_inf',
 'Ehitusaasta': 'build_year',
 'Seisukord': 'status',
 'Omandivorm': 'ownership_form',
 'Energiamärgis': 'energy',
 'raw_data': 'raw',
 'Katastrinumber': 'cataster',
 'Anda üürile korter': 'title',
 'Kulud suvel/talvel': 'expenses_summer_winter',
 'Müüa korter, Vahetuse võimalus': 'title',
 'Müüa korter (Broneeritud)': 'title',
 'Anda üürile korter (Broneeritud)': 'title',
 'Kinnistu number': 'property_nr',
 'Korruseid': 'total_floors'}

for k,v in map_names.items():
    print(f"{v} STRING,")