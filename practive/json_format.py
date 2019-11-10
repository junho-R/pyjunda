import json

cities = [{'rank':1, 'city':'상하이','ewew':'test'},
          {'rank':2, 'city':'상하이','ewew':'test'},
          {'rank':2, 'city':'상하이','ewew':'test'}]


cities2 = {'rank':1, 'city':'상하이','ewew':'test',
          'rank1':2, 'city1':'상하이','ewew1':'test',
          'rank2':2, 'city2':'상하이','ewew2':'test'}

print(json.dumps(cities2, ensure_ascii=False, indent=2))
