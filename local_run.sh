sam build -u -t templates/template-aws-sam-kv.yaml
sam build -u -t templates/template-scrape-main-info.yaml
sam build -u -t templates/template-update_table_with_yesterday.yaml


sam local invoke -e test/e.json  
sam local invoke  -e test/details.json 
sam local invoke  -e test/e.json  
