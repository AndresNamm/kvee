source prod-env.sh
ENVIRONMENT=$1
sam build
#Step 3 - Package your application
sam package --output-template packaged.yaml --s3-bucket andresmb
#Step 4 - Deploy your application
sam deploy --template-file packaged.yaml --region eu-west-1 --capabilities CAPABILITY_IAM --stack-name $ENVIRONMENT-aws-sam-kv --parameter-overrides "EnvironmentParameter=$ENVIRONMENT"
echo "Finished Depoloy"