from util_functions.templater import  render_template

import json
env = "prod"

text = """
        Update..{CITYEXPRESSION}..:
          Properties:
            Schedule: ..{CRON}..
            Input: '..{INPUT}..'
          Type: Schedule"""

remote_run = """
start=`date +%s`
echo "..{CITYEXPRESSION}.."
echo ..{INPUT}..
aws lambda invoke --cli-read-timeout 900 --cli-binary-format raw-in-base64-out --function-name "..{ENV}..-kv-ee-scraper"  --payload '..{INPUT}..' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.
"""


# remote_run = """
# aws lambda invoke --cli-read-timeout 900 --cli-binary-format raw-in-base64-out --function-name "..{ENV}..-kv-ee-scraper"  --payload '..{INPUT}..' outfile.txt
# """



cities=['rakvere','tallinn','tartu']



minute = 200

with open('schedules.txt','w') as f:
    for city in cities:
        for deal in range(1,3):
            for room_nr in range(1,6):
            
                hour = int(minute / 60) % 24
                current_minute = minute % 60
                #print(f"{10:02d}")
                minute = minute + 20

                cron = f'cron({current_minute:02d} {hour:02d} * * ? *)'
                #print(cron)
                params = {'CITYEXPRESSION':f"{city.capitalize()}{deal}{room_nr}",'CRON': cron, 'ENV':env,'INPUT':json.dumps({"city_name":f"{city}","deal_type":f"{deal}","room_nr":f"{room_nr}"})}
                res = render_template(text,params)

                run = render_template(remote_run,params)

                #print(res.lstrip("\n"))
                f.write(res)




with open('run.sh','w') as f:
    for city in cities:
        for deal in range(1,3):
            for room_nr in range(1,6):
            
                hour = int(minute / 60) % 24
                current_minute = minute % 60
                #print(f"{10:02d}")
                minute = minute + 20

                cron = f'cron({current_minute:02d} {hour:02d} * * ? *)'
                #print(cron)
                params = {'CITYEXPRESSION':f"{city.capitalize()}{deal}{room_nr}",'CRON': cron, 'ENV':env, 'INPUT':json.dumps({"city_name":f"{city}","deal_type":f"{deal}","room_nr":f"{room_nr}"})}
                res = render_template(text,params)

                run = render_template(remote_run,params)

                #print(res.lstrip("\n"))
                f.write(run)

