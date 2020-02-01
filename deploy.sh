
sam build
#Step 3 - Package your application
sam package --output-template packaged.yaml --s3-bucket andresmb
#Step 4 - Deploy your application
sam deploy --template-file packaged.yaml --region eu-west-1 --capabilities CAPABILITY_IAM --stack-name $ENV-aws-sam-kv --parameter-overrides "EnvironmentParameter=$ENV"
echo "Finished Depoloy"