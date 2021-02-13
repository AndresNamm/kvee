import util_functions.yaml_utils as yml
import util_functions.templater as tm 

import json







template_script='''aws events put-rule --name '..{RULENAME}..' --schedule-expression '..{Schedule}..'
aws events put-targets --rule ..{RULENAME}.. --targets '{"Input": "{\\"city_name\\":\\"..{city_name}..\\",\\"deal_type\\":..{deal_type}..,\\"room_nr\\":..{room_nr}..}" , "Id" : "1", "Arn" : "arn:aws:states:eu-west-1:237864522271:stateMachine:MyStateMachine","RoleArn":"arn:aws:iam::237864522271:role/service-role/AWS_Events_Invoke_Step_Functions_2092982095"}'
'''




data = yml.read_in()


deploy_scripts=[]

for k,v in data.items():
  tm_dict = {**v['Properties'], "RULENAME":k, **json.loads(v["Properties"]["Input"])}
  print(tm_dict)
  configured=tm.render_template(template_script,params=tm_dict)
  deploy_scripts.append(configured)

with open("deploy_all_cloudwatch_rules.sh","w") as f:
  for dp in deploy_scripts:
    f.write(f"{dp}\n")